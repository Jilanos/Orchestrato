from orchestrato.cost import aggregate_cost_of_pass
from orchestrato.models import UsageRecord


def test_usage_normalizes_cached_and_reasoning_details() -> None:
    usage = UsageRecord.from_payload({
        "input_tokens": 150,
        "input_tokens_details": {"cached_tokens": 100, "cache_write_tokens": 25},
        "output_tokens": 40,
        "output_tokens_details": {"reasoning_tokens": 12},
        "total_tokens": 190,
    })
    assert usage.input_tokens == 150
    assert usage.cached_input_tokens == 100
    assert usage.new_input_tokens == 50
    assert usage.cache_write_tokens == 25
    assert usage.reasoning_tokens == 12
    assert usage.total_tokens == 190


def test_cost_of_pass_uses_successes_as_denominator() -> None:
    report = aggregate_cost_of_pass([
        {"route": "direct", "passed": True, "usage": UsageRecord(total_tokens=100).to_dict()},
        {"route": "direct", "passed": False, "usage": UsageRecord(total_tokens=200).to_dict()},
    ])[0]
    assert report["pass_rate"] == 0.5
    assert report["cost_of_pass_tokens"] == 300


def test_cost_of_pass_is_undefined_without_success() -> None:
    report = aggregate_cost_of_pass([
        {"route": "chain", "passed": False, "usage": UsageRecord(total_tokens=200).to_dict()},
    ])[0]
    assert report["cost_of_pass_tokens"] is None
