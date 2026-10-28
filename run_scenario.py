
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import shared.tools as shared_tools
from shared.storage import JsonStorage
from SDK.agent import CodeStudySDKAgent


ROOT = Path(__file__).resolve().parent
SCENARIO_PATH = ROOT / "scenario.json"
RESULTS_PATH = ROOT / "results" / "scenario_results.json"


def run_scenario():
    with SCENARIO_PATH.open("r", encoding="utf-8") as file:
        scenario = json.load(file)

    results = {
        "scenario_name": scenario["scenario_name"],
        "mode": "offline_deterministic_simulation",
        "real_model_calls": 0,
        "sessions": [],
        "checks": {},
    }

    with TemporaryDirectory() as temp_dir:
        data_dir = Path(temp_dir)

        tasks_storage = JsonStorage(str(data_dir / "tasks.json"))
        preferences_storage = JsonStorage(
            str(data_dir / "preferences.json")
        )

        with (
            patch.object(shared_tools, "tasks_storage", tasks_storage),
            patch.object(
                shared_tools, "preferences_storage", preferences_storage
            ),
        ):
            for session in scenario["sessions"]:
                # A new agent instance is created for each session.
                history_path = data_dir / f"{session['session_id']}_history.json"
                agent = CodeStudySDKAgent(str(history_path))

                session_result = {
                    "session_id": session["session_id"],
                    "fresh_instance": True,
                    "requests": [],
                }

                for request in session["requests"]:
                    request_id = request["id"]

                    # Store the user's message in the offline agent history.
                    agent.chat_offline(request["message"])

                    action_result = None

                    if request_id == 1:
                        action_result = agent.run_tool(
                            "save_preference",
                            {
                                "key": "explanation_style",
                                "value": "small steps",
                            },
                        )

                    elif request_id == 2:
                        action_result = agent.run_tool(
                            "add_task",
                            {
                                "title": "Practice JavaScript classes",
                            },
                        )

                    elif request_id in (3, 6):
                        action_result = agent.run_tool("list_tasks")

                    elif request_id == 4:
                        action_result = {
                            "status": "unavailable",
                            "message": (
                                "External search is not implemented; "
                                "no URL was fabricated."
                            ),
                        }

                    elif request_id == 5:
                        preferences = agent.run_tool("get_preferences")
                        action_result = preferences.get(
                            "explanation_style"
                        )

                    elif request_id == 7:
                        tasks = agent.run_tool("list_tasks")
                        target = next(
                            (
                                task for task in tasks
                                if task["title"]
                                == "Practice JavaScript classes"
                            ),
                            None,
                        )

                        if target is None:
                            action_result = {
                                "error": "Expected task was not found"
                            }
                        else:
                            action_result = agent.run_tool(
                                "complete_task",
                                {"task_id": target["task_id"]},
                            )

                    elif request_id == 8:
                        # This request is temporary: do not overwrite memory.
                        action_result = {
                            "status": "temporary_request",
                            "saved_preference_unchanged": True,
                        }

                    session_result["requests"].append({
                        "request_id": request_id,
                        "actions": request["expected_actions"],
                        "result": action_result,
                    })

                results["sessions"].append(session_result)

            final_preferences = shared_tools.get_preferences()
            final_tasks = shared_tools.list_tasks()

            saved_preference = final_preferences.get("explanation_style")
            completed_task = next(
                (
                    task for task in final_tasks
                    if task["title"] == "Practice JavaScript classes"
                ),
                None,
            )

            results["checks"] = {
                "preference_persisted_across_sessions": (
                    saved_preference is not None
                    and saved_preference["value"] == "small steps"
                ),
                "task_persisted_across_sessions": completed_task is not None,
                "task_completed": (
                    completed_task is not None
                    and completed_task["completed"]
                ),
                "temporary_request_preserved_preference": (
                    saved_preference is not None
                    and saved_preference["value"] == "small steps"
                ),
                "external_search_reported_unavailable": any(
                    request["request_id"] == 4
                    and request["result"]["status"] == "unavailable"
                    for session in results["sessions"]
                    for request in session["requests"]
                ),
            }

    results["all_checks_passed"] = all(results["checks"].values())

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

    print("Scenario:", results["scenario_name"])
    print("Mode:", results["mode"])
    print("Real model calls:", results["real_model_calls"])
    print("\nChecks:")

    for name, passed in results["checks"].items():
        print(f"  {'PASS' if passed else 'FAIL'}: {name}")

    print("\nAll checks passed:", results["all_checks_passed"])
    print("Results saved to:", RESULTS_PATH)

    if not results["all_checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    run_scenario()
