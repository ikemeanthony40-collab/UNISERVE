from backend.agents.tool_executor import ToolExecutionAgent
from backend.agents.recovery import RecoveryAgent
from backend.agents.planner import MissionPlanner
from backend.events.event_bus import EventBus
from backend.mission_engine.models import (
    Mission,
    MissionRequest,
    MissionStatus,
    TaskStatus,
)


class MissionOrchestrator:

    def __init__(self):
        self.planner = MissionPlanner()
        self.executor = ToolExecutionAgent()
        self.recovery = RecoveryAgent()
        self.events = EventBus()

    def create_mission(self, request: MissionRequest):

        participant_count = request.constraints.get(
            "participant_count",
            50,
        )

        mission = Mission(
            "Autonomous Technology Training Mission",
            request.objective,
            status=MissionStatus.PLANNING,
        )

        mission.memory["participant_count"] = participant_count

        mission.tasks = self.planner.create_plan(
            request.objective
        )

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
                },
            )
        )

        return mission

    def run(self, mission):

        mission.status = MissionStatus.EXECUTING

        while True:

            progressed = False

            for task in mission.tasks:

                if task.status != TaskStatus.PENDING:
                    continue

                dependencies_complete = all(
                    next(
                        (
                            dependency_task.status
                            for dependency_task in mission.tasks
                            if dependency_task.title == dependency
                        ),
                        TaskStatus.PENDING,
                    )
                    == TaskStatus.COMPLETED
                    for dependency in task.dependencies
                )

                if not dependencies_complete:
                    continue

                task.status = TaskStatus.RUNNING

                mission.events.append(
                    self.events.publish(
                        "TASK_STARTED",
                        {
                            "task": task.title,
                            "agent": task.agent,
                        },
                    )
                )

                success, result = self.executor.execute(
                    task,
                    mission,
                )

                if success:

                    task.status = TaskStatus.COMPLETED
                    task.result = result

                    mission.events.append(
                        self.events.publish(
                            "TASK_COMPLETED",
                            {
                                "task": task.title,
                                "tool_result": result,
                            },
                        )
                    )

                else:

                    task.status = TaskStatus.FAILED
                    task.error = result.get(
                        "reason",
                        "Unknown execution failure",
                    )

                    mission.events.append(
                        self.events.publish(
                            "TASK_FAILED",
                            {
                                "task": task.title,
                                "reason": task.error,
                            },
                        )
                    )

                    mission.status = MissionStatus.REPLANNING

                    mission.events.append(
                        self.events.publish(
                            "EXCEPTION_DETECTED",
                            {
                                "task": task.title,
                                "reason": task.error,
                            },
                        )
                    )

                    self.recovery.replan(
                        mission,
                        task,
                    )

                    mission.events.append(
                        self.events.publish(
                            "PLAN_UPDATED",
                            {
                                "task": task.title,
                                "recovery": task.result,
                            },
                        )
                    )

                    task.status = TaskStatus.PENDING

                progressed = True
                break

            if all(
                task.status == TaskStatus.COMPLETED
                for task in mission.tasks
            ):

                mission.status = MissionStatus.COMPLETED

                mission.events.append(
                    self.events.publish(
                        "MISSION_COMPLETED",
                        {
                            "mission": mission.title,
                        },
                    )
                )

                return mission

            if not progressed:

                mission.status = MissionStatus.FAILED

                mission.events.append(
                    self.events.publish(
                        "MISSION_FAILED",
                        {
                            "mission": mission.title,
                            "reason": "No executable task remained.",
                        },
                    )
                )

                return mission
