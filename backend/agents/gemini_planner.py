import json
from google import genai

from backend.mission_engine.models import Task


class GeminiMissionPlanner:
    """
    Gemini-powered mission planner for UNISERVE.

    Gemini interprets the human objective and produces
    a structured sequence of executable mission tasks.
    """

    def __init__(self):
        self.client = genai.Client()

        self.model_names = [
            "gemini-3.5-flash",
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
            "gemini-2.5-flash",
        ]

    def create_plan(self, objective: str):

        prompt = f"""
You are the mission-planning intelligence inside UNISERVE,
an autonomous task-execution system.

Your job is to convert the user's objective into a practical,
executable sequence of tasks.

USER OBJECTIVE:
{objective}

AVAILABLE UNISERVE TOOLS:

1. analyse_requirements
2. determine_resources
3. create_schedule
4. prepare_communications
5. generate_documents
6. confirm_venue
7. verify_readiness

Return ONLY valid JSON.

Use exactly this structure:

{{
  "tasks": [
    {{
      "title": "short task title",
      "description": "what must be accomplished",
      "agent": "planner|researcher|communications|execution|verification",
      "tool": "one of the available tools",
      "dependencies": ["title of previous task"]
    }}
  ]
}}

Rules:

- Create only tasks necessary to accomplish the objective.
- Every task MUST have one tool from AVAILABLE UNISERVE TOOLS.
- The tool must be appropriate for the task.
- Dependencies must reference earlier task titles.
- Do not invent tools.
- Do not include explanations outside the JSON.
"""

        response = None
        last_error = None

        for model_name in self.model_names:
            try:
                print(f"Gemini planner: trying {model_name}...")

                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )

                print(f"Gemini planner: {model_name} succeeded.")
                break

            except Exception as exc:
                last_error = exc
                print(f"Gemini planner: {model_name} unavailable.")
                print(f"Reason: {exc}")

        if response is None:
            raise RuntimeError(
                f"All Gemini planner models failed. Last error: {last_error}"
            )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        data = json.loads(text)

        tasks = []

        for item in data["tasks"]:
            tasks.append(
                Task(
                    title=item["title"],
                    description=item["description"],
                    agent=item["agent"],
                    tool=item["tool"],
                    dependencies=item.get("dependencies", []),
                )
            )

        return tasks
