from orchestrato.context import build_handoff_packet


def test_context_packet_is_role_specific() -> None:
    packet = build_handoff_packet(
        role="reviewer", objective="Review the change",
        context_pack={"acceptance_criteria": ["tests pass"], "diff_summary": "small diff", "relevant_files": ["plan.md"], "failure": "omit"},
    )
    assert "diff_summary" in packet.fields
    assert "failure" not in packet.fields
    assert "relevant_files" not in packet.fields


def test_context_packet_reduces_oversized_context_with_reason() -> None:
    packet = build_handoff_packet(
        role="executor", objective="Implement the task",
        context_pack={"summary": "important summary", "relevant_files": ["file.py"] * 1000}, max_chars=300,
    )
    assert packet.truncated is True
    assert packet.truncation_reason == "max_chars_exceeded"
    assert len(packet.render()) <= 300
