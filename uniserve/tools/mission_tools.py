from typing import Dict, Any, List

from strands import tool

from uniserve.core.mission import MissionController
from uniserve.core.recovery import RecoveryEngine


mission = None
recovery_engine = RecoveryEngine()


@tool
def create_mission(objective: str, tasks: List[str]) -> Dict[str, Any]:
    """Create a new UNISERVE mission from the user's assignment and a dynamically generated task list."""
    global mission

    if not objective.strip():
        raise ValueError("Mission objective cannot be empty.")

    if not tasks:
        raise ValueError("At least one mission task is required.")

    cleaned_tasks = [task.strip() for task in tasks if task.strip()]

    if not cleaned_tasks:
        raise ValueError("Mission must contain at least one valid task.")

    mission = MissionController(
        mission_id="UNISERVE-LIVE",
        objective=objective,
        total_tasks=len(cleaned_tasks),
    )

    return {
        **mission.snapshot(),
        "planned_tasks": cleaned_tasks,
    }


@tool
def get_mission_status() -> Dict[str, Any]:
    """Inspect the current mission state."""
    if mission is None:
        return {
            "status": "NO_MISSION",
            "message": "No mission has been created yet.",
        }

    return mission.snapshot()


@tool
def start_mission_task(task: str) -> Dict[str, Any]:
    """Start a mission task."""
    if mission is None:
        raise RuntimeError("Create a mission before starting tasks.")

    return mission.start_task(task)


@tool
def complete_mission_task(task: str) -> Dict[str, Any]:
    """Mark a mission task as successfully completed."""
    if mission is None:
        raise RuntimeError("Create a mission before completing tasks.")

    return mission.complete_task(task)


@tool
def fail_mission_task(task: str, reason: str) -> Dict[str, Any]:
    """Report a failed mission task."""
    if mission is None:
        raise RuntimeError("Create a mission before reporting failure.")

    return mission.fail_task(task, reason)


@tool
def recover_failed_task(task: str, reason: str) -> Dict[str, Any]:
    """Analyze a failed task and determine a recovery strategy."""
    return recovery_engine.analyze_failure(task, reason)
