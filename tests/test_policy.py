from orchestrato.policy import PolicyRouter, classify


def test_classifies_planning_and_defaults_to_medium() -> None:
    route = PolicyRouter().route("Design the architecture for the MVP")
    assert route.intent.kind == "planning"
    assert route.profile.role == "planner"
    assert route.effort == "medium"
    assert route.approval_required is False


def test_classifies_push_as_low_effort_external_operation() -> None:
    route = PolicyRouter().route("git push the release branch")
    assert route.intent.kind == "operations"
    assert route.effort == "low"
    assert route.approval_required is True


def test_high_effort_recovery_is_explicit() -> None:
    route = PolicyRouter().route("The build is stuck and failing after retries")
    assert route.profile.role == "recovery"
    assert route.effort == "high"


def test_operator_can_override_role_and_effort() -> None:
    route = PolicyRouter().route("Implement the parser", role="specialist", effort="low")
    assert route.profile.role == "specialist"
    assert route.effort == "low"
