from typing import Dict, Any

from uniserve.core.state import MissionState


class MissionController:
    """Controls the lifecycle of a UNISERVE mission."""

    def __init__(
        self,
        mission_id: str,
        objective: str,
        total_tasks: int,
    ) -> None:
        self.state = MissionState(
            mission_id=mission_id,
            objective=objective,
            total_tasks=total_tasks,
        )

    def start_task(self, task: str) -> Dict[str, Any]:
        self.state.current_task = task
        self.state.status = "EXECUTING"

        return self.snapshot()

    def complete_task(self, task: str) -> Dict[str, Any]:
        if task not in self.state.completed_tasks:
            self.state.completed_tasks.append(task)

        self.state.current_task = None

        if self.state.is_complete:
            self.state.status = "COMPLETED"
        else:
            self.state.status = "READY"

        return self.snapshot()

    def fail_task(self, task: str, reason: str) -> Dict[str, Any]:
        if task not in self.state.failed_tasks:
            self.state.failed_tasks.append(task)

        self.state.status = "RECOVERY_REQUIRED"
        self.state.current_task = task

        result = self.snapshot()
        result["failure_reason"] = reason
        result["recovery_required"] = True

        return result

    def snapshot(self) -> Dict[str, Any]:
        return {
            "mission_id": self.state.mission_id,
            "objective": self.state.objective,
            "status": self.state.status,
            "progress": self.state.progress,
            "current_task": self.state.current_task,
            "completed_tasks": list(self.state.completed_tasks),
            "failed_tasks": list(self.state.failed_tasks),
            "is_complete": self.state.is_complete,
        }