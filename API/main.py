
from API.agent import CodeStudyAgent
from API.harness.tokens import RunMetrics


def main():
    agent = CodeStudyAgent()
    metrics = RunMetrics()

    print("CodeStudyAgent is ready!")
    print("Type 'exit' to quit.\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() in {"exit", "quit"}:
            break

        if not user_message:
            continue

        started_at = metrics.start_timer()

        try:
            result = agent.chat(user_message)

            print(f"\nAgent: {result['answer']}\n")
            print(
                f"[Model calls: {result['model_calls']}, "
                f"Tool calls: {result['tool_calls']}]\n"
            )

            metrics.record_turn(started_at, result)

        except Exception as error:
            print(f"Error: {error}")

    metrics.save("results/api.json")
    print("Metrics saved to results/api.json")


if __name__ == "__main__":
    main()
