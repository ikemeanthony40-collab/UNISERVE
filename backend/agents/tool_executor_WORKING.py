from backend.tools.tool_setup import create_tool_registry


class ToolExecutionAgent:
    """
    Executes mission tasks through the UNISERVE Tool Registry.

    The agent translates mission tasks into registered tools and
    passes mission context to those tools where required.
    """

    def __init__(self):
        self.registry = create_tool_registry()

    def execute(self, task, mission):
        tool_map = {
            "Analyse mission requirements": "analyse_requirements",
            "Determine required resources": "determine_resources",
            "Create programme schedule": "create_schedule",
            "Prepare participant communications": "prepare_communications",
            "Generate mission documents": "generate_documents",
            "Confirm venue": "confirm_venue",
            "Verify mission readiness": "verify_readiness",
        }

        tool_name = tool_map.get(task.title)

        if not tool_name:
            return False, {
                "reason": f"No registered tool mapped to task: {task.title}"
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
                    50,
                )

                result = self.registry.execute(
                    tool_name,
                    participant_count=participant_count,
                )

            elif tool_name == "confirm_venue":
                replanned = mission.memory.get(
                    "venue_replanned",
                    False,
                )

                result = self.registry.execute(
                    tool_name,
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
