from typing import List, Dict


class MissionPlanner:
    """
    Creates an executable mission plan from a high-level objective.

    The initial version uses a deterministic fallback plan.
    Later, the Strands/Bedrock agent can generate the plan dynamically.
    """

    def create_plan(self, objective: str) -> List[Dict]:
        if not objective.strip():
            raise ValueError("Mission objective cannot be empty.")

        return [
            {
                "id": 1,
                "name": "Identify participants",
                "description": "Identify and validate the training participants.",
            },
            {
                "id": 2,
                "name": "Determine training requirements",
                "description": "Determine resources and requirements for the training.",
            },
            {
                "id": 3,
                "name": "Find suitable venue",
                "description": "Find a venue that satisfies the mission requirements.",
            },
            {
                "id": 4,
                "name": "Confirm the original venue",
                "description": "Confirm availability of the selected venue.",
            },
            {
                "id": 5,
                "name": "Prepare training schedule",
                "description": "Create the training schedule.",
            },
            {
                "id": 6,
                "name": "Prepare participant communications",
                "description": "Prepare communications for the participants.",
            },
            {
                "id": 7,
                "name": "Verify mission completion",
                "description": "Verify that all mission requirements have been satisfied.",
            },
        ]