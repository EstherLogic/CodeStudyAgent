
from dataclasses import dataclass, asdict


# Example prices in USD per million tokens.
# Verify the actual model pricing before reporting results.
DEFAULT_INPUT_PRICE_PER_MILLION = 3.00
DEFAULT_OUTPUT_PRICE_PER_MILLION = 15.00


@dataclass
class TokenUsage:
    input_tokens: int = 0
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0
    output_tokens: int = 0

    def estimated_cost(
        self,
        input_price_per_million: float = DEFAULT_INPUT_PRICE_PER_MILLION,
        output_price_per_million: float = DEFAULT_OUTPUT_PRICE_PER_MILLION,
    ) -> float:
        """Estimate cost; cached-token pricing is not included."""
        billable_input = (
            self.input_tokens
            + self.cache_creation_input_tokens
        )

        return (
            billable_input * input_price_per_million
            + self.output_tokens * output_price_per_million
        ) / 1_000_000

    def to_dict(self) -> dict:
        result = asdict(self)
        result["estimated_cost_usd"] = self.estimated_cost()
        return result


def usage_from_response(response) -> TokenUsage:
    """Extract usage values from an Anthropic API response."""
    usage = getattr(response, "usage", None)

    if usage is None:
        return TokenUsage()

    return TokenUsage(
        input_tokens=getattr(usage, "input_tokens", 0),
        cache_read_input_tokens=getattr(
            usage, "cache_read_input_tokens", 0
        ),
        cache_creation_input_tokens=getattr(
            usage, "cache_creation_input_tokens", 0
        ),
        output_tokens=getattr(usage, "output_tokens", 0),
    )

import time


class RunMetrics:
    """Collect per-turn metrics and save them to a JSON file."""

    def __init__(self):
        self.turns = []

    def start_timer(self) -> float:
        return time.perf_counter()

    def record_turn(
        self,
        started_at: float,
        result: dict,
    ) -> dict:
        elapsed_seconds = time.perf_counter() - started_at

        usage_records = result.get("usage", [])
        totals = {
            "input_tokens": sum(
                item.get("input_tokens", 0) for item in usage_records
            ),
            "cache_read_input_tokens": sum(
                item.get("cache_read_input_tokens", 0)
                for item in usage_records
            ),
            "cache_creation_input_tokens": sum(
                item.get("cache_creation_input_tokens", 0)
                for item in usage_records
            ),
            "output_tokens": sum(
                item.get("output_tokens", 0)
                for item in usage_records
            ),
        }

        turn = {
            "duration_seconds": round(elapsed_seconds, 4),
            "model_calls": result.get("model_calls", 0),
            "tool_calls": result.get("tool_calls", 0),
            "usage": usage_records,
            "usage_totals": totals,
        }

        self.turns.append(turn)
        return turn

    def save(self, file_path: str) -> None:
        import json
        from pathlib import Path

        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            json.dump(
                {"turns": self.turns},
                file,
                ensure_ascii=False,
                indent=2,
            )
