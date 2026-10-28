# CodeStudyAgent — Implementation and Evaluation Report

## 1. Project Overview

CodeStudyAgent is a programming study assistant prototype. It manages study tasks, stores user preferences, and preserves conversation history across agent instances.

The project contains two approaches:

- **API implementation:** A custom agent loop that handles model responses and tool calls.
- **SDK implementation:** An offline-testable agent prototype with shared tools and persistent conversation history.

Both implementations reuse shared data models, JSON storage, and task-management functions.

## 2. Architecture

### Shared components

- `shared/models.py` — Task and Preference data models.
- `shared/storage.py` — JSON-based persistent storage.
- `shared/tools.py` — Shared task and preference operations.

### API components

- `API/harness/loop.py` — Model interaction loop and tool execution.
- `API/harness/tools.py` — Tool definitions and dispatch.
- `API/harness/memory.py` — Preference retrieval and persistence.
- `API/harness/history.py` — Persistent conversation history.
- `API/harness/context.py` — Context construction.
- `API/harness/compaction.py` — Conversation history compaction.
- `API/harness/tokens.py` — Token usage and run-metrics utilities.
- `API/harness/caching.py` — Cache-related helper functions.

### SDK components

- `SDK/tools.py` — Functions exposed to the SDK agent.
- `SDK/agent.py` — Offline-testable agent and persistent history.
- `SDK/main.py` — Terminal entry point for offline mode.

## 3. Automated Test Results

The latest full test run reported:

- **Total tests:** 17
- **Passed:** 17
- **Failed:** 0

The tests cover:

- Task and preference data models.
- JSON storage, including missing and invalid files.
- Creating, listing, and completing tasks.
- Saving and retrieving preferences.
- API-loop behavior using mocked model responses.
- Tool execution and continuation after a tool call.
- SDK offline responses.
- Persistent conversation history across new agent instances.
- Error handling for unknown tools and invalid arguments.

These are offline tests. They do not establish real model quality or real API/SDK performance.

## 4. Scenario Design

The scenario was executed using `python run_scenario.py` in `offline_deterministic_simulation` mode. All five integration checks passed. The runner directly invokes the expected actions; therefore, this validates persistence and deterministic behavior, but not model-driven tool selection or real end-to-end LLM performance. Results are saved in `results/scenario_results.json`.
## 5. Metrics and Limitations

The project includes utilities for recording:

- Duration per turn.
- Model call count.
- Tool call count.
- Input and output tokens.
- Cache-read and cache-creation token counts.
- Estimated API cost.

The existing metrics utility has been tested with sample data. These sample values are not real model measurements.

A genuine API-versus-SDK comparison remains pending because a real model-backed SDK run has not been completed. The current SDK implementation operates in offline mode and records zero model calls.

The external search tool is also not yet implemented as an executable tool in the current project.

No claims about relative speed, cost, token efficiency, or answer quality should be made until both implementations have been run with equivalent scenarios and comparable measurement settings.

## 6. Remaining Work

1. Implement and verify external documentation search.
2. Implement scenario execution across two separate sessions.
3. Verify that preferences and tasks persist after restarting the agent.
4. Ensure the temporary contradictory request does not overwrite the saved preference.
5. Connect the SDK implementation to its actual SDK runtime when access is available.
6. Run the same scenario against both real implementations.
7. Record real token usage, cache metrics, duration, model calls, tool calls, and cost.
8. Measure lines of code for both implementations using the same counting method.
9. Update this report with actual results and a fair comparison.

## 7. Conclusion

The current prototype has a shared persistence layer, task-management tools, an API agent loop, an offline SDK prototype, and 17 passing automated tests.

The project is not yet a completed real-model benchmark. End-to-end scenario execution, external search, and real API-versus-SDK measurements remain to be completed.
## 8. Integration Scenario Results

The offline integration scenario was executed successfully.

- Sessions defined: 2
- Requests defined: 8
- Real model calls: 0
- Integration checks passed: 5 of 5

### Verified checks

1. User preferences persisted across separate agent instances.
2. Study tasks persisted across sessions.
3. The selected task was marked as completed.
4. A temporary contradictory request did not overwrite the saved preference.
5. The unavailable external-search capability was reported explicitly instead of fabricating a result.

Results were saved to `results/scenario_results.json`.

### Interpretation

These results validate the shared persistence layer and the deterministic offline scenario. They do not validate model-driven tool selection, response quality, or real API-versus-SDK performance. The scenario runner invokes expected actions directly rather than asking a language model to choose the tools.
## 9. Code Size and Current Comparison

### Lines of Code (LOC)

| Component | Non-empty, non-comment Python lines |
|---|---:|
| API | 422 |
| SDK | 107 |
| Shared | 87 |
| Tests | 226 |
| **Total** | **842** |

The counts exclude blank lines and comment-only lines. They include Python files in the listed folders and exclude `__pycache__` directories.

### Current Validation Results

- 17 unit tests passed.
- 5 deterministic integration checks passed.
- Real model calls: 0.
- Real model token usage, latency, and cost: not measured.

### Comparison Limitations

The current SDK implementation runs in offline mode and does not yet invoke the actual Claude Agent SDK runtime. The API and SDK implementations have not been benchmarked under equivalent real-model conditions. Therefore, the LOC figures describe the current codebase, but they do not establish which implementation is faster, cheaper, or more reliable in real usage.