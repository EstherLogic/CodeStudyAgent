
import json

from API.harness.context import build_context
from API.harness.tools import execute_tool, get_tool_definitions
from API.harness.tokens import usage_from_response


SYSTEM_PROMPT = """
You are CodeStudyAgent, a helpful programming study assistant.
Help the user understand programming concepts and organize study tasks.
Use tools when you need to create, list, or complete tasks, or save preferences.
Use the supplied user context when it is relevant.
Be clear, practical, and concise.
"""


def run_agent(client, user_message: str, history: list | None = None) -> dict:
    """Run one conversation turn and collect usage metrics."""

    if history is None:
        history = []

    messages = history + [
        {
            "role": "user",
            "content": (
                f"{build_context()}\n\n"
                f"User message: {user_message}"
            ),
        }
    ]

    model_calls = 0
    tool_calls = 0
    usage_records = []

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=get_tool_definitions(),
            messages=messages,
        )
        model_calls += 1

        usage = usage_from_response(response)
        usage_records.append(usage.to_dict())

        assistant_content = response.content
        messages.append(
            {"role": "assistant", "content": assistant_content}
        )

        if response.stop_reason != "tool_use":
            text_parts = [
                block.text
                for block in assistant_content
                if getattr(block, "type", None) == "text"
            ]
            return {
                "answer": "\n".join(text_parts),
                "messages": messages,
                "model_calls": model_calls,
                "tool_calls": tool_calls,
                "usage": usage_records,
            }

        tool_results = []

        for block in assistant_content:
            if getattr(block, "type", None) != "tool_use":
                continue

            result = execute_tool(block.name, block.input)
            tool_calls += 1

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result, ensure_ascii=False),
                }
            )

        messages.append({"role": "user", "content": tool_results})
