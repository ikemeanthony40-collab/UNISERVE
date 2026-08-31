import re

from backend.agents.gemini_planner import GeminiMissionPlanner
from backend.agents.recovery import RecoveryAgent
from backend.agents.tool_executor import ToolExecutionAgent
from backend.events.event_bus import EventBus
from backend.mission_engine.models import (
    Mission,
    MissionRequest,
    MissionStatus,
    TaskStatus,
)


class MissionOrchestrator:
    """
    Central autonomous controller for UNISERVE.

    Responsibilities:
    - receive mission objectives
    - extract mission parameters
    - ask Gemini to generate an executable plan
    - execute tasks through the Tool Registry
    - observe failures
    - invoke recovery/replanning
    - continue until completion or unrecoverable failure
    """

    def __init__(self):
        self.planner = GeminiMissionPlanner()
        self.executor = ToolExecutionAgent()
        self.recovery = RecoveryAgent()
        self.events = EventBus()

    def _extract_participant_count(self, objective: str) -> int:
        """
        Extract participant count from a mission objective.

        Supports:
        - 30 participants
        - 50 students
        - 100 attendees
        - 25 people
        - 40 persons
        - 30 university students
        """

        patterns = [
            r"\b(\d+)\s+(?:university\s+)?students?\b",
            r"\b(\d+)\s+participants?\b",
            r"\b(\d+)\s+attendees?\b",
            r"\b(\d+)\s+people\b",
            r"\b(\d+)\s+persons?\b",
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                objective,
                re.IGNORECASE,
            )

            if match:
                return int(match.group(1))

        return 0

    def create_mission(self, request: MissionRequest):

        participant_count = (
            request.constraints.get("participant_count")
            or self._extract_participant_count(request.objective)
        )

        mission = Mission(
            title="Autonomous Mission",
            objective=request.objective,
            status=MissionStatus.PLANNING,
        )

        mission.memory["participant_count"] = participant_count

        tasks = self.planner.create_plan(
            request.objective
        )

        mission.tasks = tasks

        mission.events.append(
            self.events.publish(
                "MISSION_CREATED",
                {
                    "objective": request.objective,
                    "participant_count": participant_count,
                },
            )
        )

        mission.events.append(
            self.events.publish(
                "PLAN_CREATED",
                {
                    "task_count": len(mission.tasks),
                    "planner": "Gemini",
                },
            )
        )

        return mission

    def _dependencies_completed(self, task, mission):

        for dependency_title in task.dependencies:

            dependency = next(
                (
                    t
                    for t in mission.tasks
                    if t.title == dependency_title
                ),
                None,
            )

            if dependency is None:
                return False

            if dependency.status != TaskStatus.COMPLETED:
                return False

        return True

    def run(self, mission):

        mission.status = MissionStatus.EXECUTING

        while True:

            progressed = False

            for task in mission.tasks:

                if task.status != TaskStatus.PENDING:
                    continue

                if not self._dependencies_completed(task, mission):
                    continue

                task.status = TaskStatus.RUNNING

                event = self.events.publish(
                    "TASK_STARTED",
                    {
                        "task": task.title,
                        "agent": task.agent,
                        "tool": task.tool,
                    },
                )

                mission.events.append(event)

                success, result = self.executor.execute(
                    task,
                    mission,
                )

                if success:

                    task.status = TaskStatus.COMPLETED
                    task.result = result

                    event = self.events.publish(
                        "TASK_COMPLETED",
                        {
                            "task": task.title,
                            "tool": task.tool,
                            "tool_result": result,
                        },
                    )

                    mission.events.append(event)

                else:

                    task.status = TaskStatus.FAILED

                    task.error = result.get(
                        "reason",
                        "Unknown execution error",
                    )

                    event = self.events.publish(
                        "TASK_FAILED",
                        {
                            "task": task.title,
                            "tool": task.tool,
                            "reason": task.error,
                        },
                    )

                    mission.events.append(event)

                    mission.status = MissionStatus.REPLANNING

                    event = self.events.publish(
                        "EXCEPTION_DETECTED",
                        {
                            "task": task.title,
                            "tool": task.tool,
                            "reason": task.error,
                        },
                    )

                    mission.events.append(event)

                    self.recovery.replan(
                        mission,
                        task,
                    )

                    event = self.events.publish(
                        "PLAN_UPDATED",
                        {
                            "task": task.title,
                            "recovery": task.result,
                        },
                    )

                    mission.events.append(event)

                    task.status = TaskStatus.PENDING

                    mission.status = MissionStatus.EXECUTING

                progressed = True
                break

            if all(
                task.status == TaskStatus.COMPLETED
                for task in mission.tasks
            ):

                mission.status = MissionStatus.COMPLETED

                event = self.events.publish(
                    "MISSION_COMPLETED",
                    {
                        "mission": mission.title,
                    },
                )

                mission.events.append(event)

                return mission

            if not progressed:

                mission.status = MissionStatus.FAILED

                event = self.events.publish(
                    "MISSION_FAILED",
                    {
                        "mission": mission.title,
                        "reason": "No executable tasks remain.",
                    },
                )

                mission.events.append(event)

                return mission