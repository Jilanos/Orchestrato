from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .application import Orchestrator, database_for
from .policy import PolicyRouter, load_config
from .observability import LiveReporter
from .store import EventStore
from .supervisor import Supervisor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="orchestrato", description="Local conversational agent supervisor")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument("--config", type=Path, default=None, help="Optional TOML policy file")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("plan", "route"):
        command = sub.add_parser(name, help=f"{name.capitalize()} a development objective")
        command.add_argument("objective")
        command.add_argument("--role")
        command.add_argument("--effort", choices=("low", "medium", "high"))

    run = sub.add_parser("run", help="Start an approved objective execution")
    run.add_argument("objective")
    run.add_argument("--yes", action="store_true", help="Approve the route when it mutates the repository")
    run.add_argument("--execute", action="store_true", help="Invoke cdx-manager after approval")
    run.add_argument("--live", action="store_true", help="Print execution events as they occur to stderr")
    run.add_argument("--role")
    run.add_argument("--effort", choices=("low", "medium", "high"))

    status = sub.add_parser("status", help="List recent objectives")
    status.add_argument("--limit", type=int, default=20)

    inspect = sub.add_parser("inspect", help="Inspect one objective and its events")
    inspect.add_argument("objective_id")

    approve = sub.add_parser("approve", help="Approve a planned objective")
    approve.add_argument("objective_id")
    cancel = sub.add_parser("cancel", help="Cancel a non-terminal objective")
    cancel.add_argument("objective_id")

    sub.add_parser("logics-status", help="Read Logics Manager status as JSON")
    validate = sub.add_parser("validate", help="Validate Logics refs")
    validate.add_argument("refs", nargs="+", help="Logics refs to validate")
    sub.add_parser("repl", help="Start the compact interactive operator loop")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    config = load_config(args.config or (root / "orchestrato.toml"))
    store = EventStore(database_for(root, config))
    try:
        router = PolicyRouter(config)
        orchestrator = Orchestrator(store, router)
        supervisor = Supervisor(orchestrator, int(config.get("policy", {}).get("max_attempts", 2)))
        if args.command == "route":
            route = router.route(args.objective, role=args.role, effort=args.effort)
            return emit(route.to_dict(), args.json)
        if args.command == "plan":
            objective = orchestrator.plan(args.objective, role=args.role, effort=args.effort)
            return emit(orchestrator.render_plan(objective), args.json)
        if args.command == "run":
            reporter = LiveReporter() if args.live else None
            if reporter:
                reporter.start()
            objective = orchestrator.plan(args.objective, role=args.role, effort=args.effort)
            route_payload = {
                "role": objective.route.profile.role if objective.route else "unknown",
                "provider": objective.route.profile.provider if objective.route else "unknown",
                "effort": objective.route.effort if objective.route else "unknown",
                "permission": objective.route.profile.permission if objective.route else "unknown",
            }
            orchestrator.publish(objective.objective_id, "route_selected", route_payload, reporter)
            if objective.route and objective.route.approval_required and not args.yes:
                if reporter:
                    reporter.close()
                return emit({"ok": False, "error": "approval_required", **orchestrator.render_plan(objective)}, args.json, 2)
            started = orchestrator.approve_and_start(objective.objective_id)
            orchestrator.publish(objective.objective_id, "approval_granted", {"state": started.state}, reporter)
            if args.execute:
                completed = supervisor.execute(objective.objective_id, root=root, observer=reporter)
                if reporter:
                    reporter.close()
                return emit({"ok": True, **orchestrator.render_plan(completed)}, args.json)
            if reporter:
                reporter.close()
            return emit({"ok": True, **orchestrator.render_plan(started), "next": "execute via cdx adapter"}, args.json)
        if args.command == "status":
            return emit({"objectives": [orchestrator.render_plan(item) for item in store.list(args.limit)]}, args.json)
        if args.command == "inspect":
            objective = store.get(args.objective_id)
            return emit({"objective": orchestrator.render_plan(objective), "events": store.events(args.objective_id)}, args.json)
        if args.command == "approve":
            started = orchestrator.approve_and_start(args.objective_id)
            return emit({"ok": True, **orchestrator.render_plan(started)}, args.json)
        if args.command == "cancel":
            cancelled = orchestrator.cancel(args.objective_id)
            return emit({"ok": True, **orchestrator.render_plan(cancelled)}, args.json)
        if args.command in {"logics-status", "validate"}:
            from .adapters.logics import LogicsAdapter
            adapter = LogicsAdapter()
            payload = adapter.status(cwd=root) if args.command == "logics-status" else adapter.validate(args.refs, cwd=root)
            return emit(payload, args.json)
        if args.command == "repl":
            return repl(orchestrator)
    except (KeyError, ValueError, RuntimeError) as exc:
        return emit({"ok": False, "error": str(exc)}, args.json, 1)
    finally:
        store.close()
    return 0


def repl(orchestrator: Orchestrator) -> int:
    print("Orchestrato REPL. Enter an objective, or /status, /quit.")
    while True:
        try:
            line = input("orch> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not line:
            continue
        if line in {"/quit", "/exit"}:
            return 0
        if line == "/status":
            for item in orchestrator.store.list():
                print(f"{item.objective_id} [{item.state}] {item.text}")
            continue
        if line.startswith("/route "):
            route = orchestrator.router.route(line[7:])
            print(f"{route.profile.label} / {route.effort}: {route.reason}")
            continue
        try:
            objective = orchestrator.plan(line)
            print(f"{objective.objective_id}: planned -> {objective.route.profile.label if objective.route else 'unknown'}")
        except ValueError as exc:
            print(f"error: {exc}")


def emit(payload: dict, machine: bool, exit_code: int = 0) -> int:
    if machine:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if "route" in payload and payload.get("route"):
            route = payload["route"]
            print(f"{payload.get('objective_id', 'route')}: {payload.get('state', 'ready')} -> {route['profile']['label']} ({route['effort']})")
            print(route["reason"])
            if route["approval_required"]:
                print("Approval required before repository or external mutation.")
        elif "objectives" in payload:
            for item in payload["objectives"]:
                print(f"{item['objective_id']} [{item['state']}] {item['text']}")
        elif "objective" in payload:
            print(json.dumps(payload, indent=2))
        else:
            print(json.dumps(payload, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
