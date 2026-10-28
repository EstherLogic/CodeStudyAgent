
def compact_messages(
    messages: list[dict],
    keep_last: int = 6,
) -> list[dict]:
    """
    Keep recent messages and replace older messages with a short summary.
    This function does not call an AI model.
    """
    if keep_last < 2:
        raise ValueError("keep_last must be at least 2")

    if len(messages) <= keep_last:
        return list(messages)

    older_messages = messages[:-keep_last]
    recent_messages = messages[-keep_last:]

    summary_parts = []

    for message in older_messages:
        role = message.get("role", "unknown")
        content = message.get("content", "")

        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            text = " ".join(
                block.get("text", "")
                for block in content
                if isinstance(block, dict)
            )
        else:
            text = str(content)

        if text.strip():
            summary_parts.append(f"{role}: {text.strip()}")

    summary = "Earlier conversation summary:\n" + "\n".join(
        summary_parts
    )

    return [
        {"role": "user", "content": summary},
        *recent_messages,
    ]
