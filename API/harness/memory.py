
from shared.tools import save_preference, get_preferences


class AgentMemory:
    """Persistent memory for user preferences."""

    def remember(self, key: str, value: str) -> dict:
        """Save a preference to persistent storage."""
        return save_preference(key, value)

    def recall(self) -> dict:
        """Load all saved preferences."""
        return get_preferences()

    def recall_one(self, key: str) -> dict | None:
        """Load one preference by its key."""
        preferences = self.recall()
        return preferences.get(key)
