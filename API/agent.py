
from anthropic import Anthropic

from API.harness.loop import run_agent


class CodeStudyAgent:
    def __init__(self, client=None):
        # Allow a mock client for offline tests.
        self.client = client if client is not None else Anthropic()
        self.history = []

    def chat(self, user_message: str) -> dict:
        """Process one user message and preserve conversation history."""
        result = run_agent(
            client=self.client,
            user_message=user_message,
            history=self.history,
        )

        self.history = result["messages"]

        return result
