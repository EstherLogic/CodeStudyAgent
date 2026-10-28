
from SDK.agent import CodeStudySDKAgent
from API.harness.tokens import RunMetrics


def main():
    agent = CodeStudySDKAgent()
    metrics = RunMetrics()

    print("CodeStudyAgent SDK - Offline Mode")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if user_message.lower() in {"exit", "quit"}:
            break

        if not user_message:
            continue

        started_at = metrics.start_timer()

        try:
            result = agent.chat_offline(user_message)
            print(f"\nAgent: {result['answer']}\n")

            metrics.record_turn(started_at, result)

        except Exception as error:
            print(f"Error: {error}")

    metrics.save("results/sdk.json")
    print("Metrics saved to results/sdk.json")


if __name__ == "__main__":
    main()
