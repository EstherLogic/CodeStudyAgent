
import hashlib
import json


def create_cache_key(content: str) -> str:
    """Create a stable hash for reusable prompt content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def get_cache_control() -> dict:
    """Return the ephemeral prompt-caching configuration."""
    return {"type": "ephemeral"}


def build_cacheable_text(content: str) -> dict:
    """Build a text block that can be used in a cacheable prompt."""
    return {
        "type": "text",
        "text": content,
        "cache_control": get_cache_control(),
    }


def cache_key_for_tools(tools: list[dict]) -> str:
    """Create a stable key for a tool definition list."""
    serialized = json.dumps(
        tools,
        sort_keys=True,
        ensure_ascii=False,
    )
    return create_cache_key(serialized)
