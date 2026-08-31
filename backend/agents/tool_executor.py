from backend.tools.tool_setup import create_tool_registry


class ToolExecutionAgent:
    """
    Executes Gemini-generated mission tasks through the
    UNISERVE Tool Registry.
    """

    def __init__(self):
        self.registry = create_tool_registry()

    def execute(self, task, mission):

        tool_name = task.tool

        if not tool_name:
            return False, {
                "reason": f"Task has no execution tool assigned: {task.title}"
            }

        if not self.registry.has_tool(tool_name):
            return False, {
                "reason": f"Tool '{tool_name}' is not registered.",
                "tool": tool_name,
            }

        try:

            if tool_name == "analyse_requirements":
                result = self.registry.execute(
                    tool_name,
                    objective=mission.objective,
                )

            elif tool_name in {
                "determine_resources",
                "create_schedule",
                "prepare_communications",
            }:
                participant_count = mission.memory.get(
                    "participant_count",
                    0,
                )

                result = self.registry.execute(
                    tool_name,
                    participant_count=participant_count,
                )

            elif tool_name == "confirm_venue":
                participant_count = mission.memory.get(
                    "participant_count",
                    0,
                )

                replanned = mission.memory.get(
                    "venue_replanned",
                    False,
                )

                result = self.registry.execute(
                    tool_name,
                    participant_count=participant_count,
                    replanned=replanned,
                )

            else:
                result = self.registry.execute(tool_name)

            if result.get("status") == "failed":
                return False, result

            mission.memory.setdefault("tool_results", {})
            mission.memory["tool_results"][tool_name] = result

            return True, result

        except Exception as exc:
            return False, {
                "reason": str(exc),
                "tool": tool_name,
            }
