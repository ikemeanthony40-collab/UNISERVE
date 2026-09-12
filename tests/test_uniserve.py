import pytest

from uniserve.core.mission import MissionController
from uniserve.core.recovery import RecoveryEngine


def create_mission():
    return MissionController(
        mission_id="TEST-001",
        objective="Organize an agricultural training event",
        total_tasks=3,
    )


def test_mission_starts_ready():
    mission = create_mission()

    state = mission.snapshot()

    assert state["status"] == "READY"
    assert state["progress"] == 0
    assert state["completed_tasks"] == []
    assert state["failed_tasks"] == []
    assert state["is_complete"] is False


def test_task_can_start():
    mission = create_mission()

    state = mission.start_task("Identify participants")

    assert state["status"] == "EXECUTING"
    assert state["current_task"] == "Identify participants"


def test_task_completion_updates_progress():
    mission = create_mission()

    mission.start_task("Identify participants")
    state = mission.complete_task("Identify participants")

    assert state["status"] == "READY"
    assert state["progress"] == 33
    assert "Identify participants" in state["completed_tasks"]


def test_failed_task_requires_recovery():
    mission = create_mission()

    mission.start_task("Find suitable venue")
    state = mission.fail_task(
        "Find suitable venue",
        "Original venue is unavailable",
    )

    assert state["status"] == "RECOVERY_REQUIRED"
    assert state["current_task"] == "Find suitable venue"
    assert "Find suitable venue" in state["failed_tasks"]
    assert state["recovery_required"] is True
    assert state["failure_reason"] == "Original venue is unavailable"


def test_venue_failure_is_recoverable():
    recovery = RecoveryEngine()

    result = recovery.analyze_failure(
        "Find suitable venue",
        "Original venue is unavailable",
    )

    assert result["recoverable"] is True
    assert result["strategy"] == "alternative_resource"
    assert result["failed_task"] == "Find suitable venue"
    assert len(result["recovery_plan"]) > 0


def test_non_venue_failure_is_also_recoverable():
    recovery = RecoveryEngine()

    result = recovery.analyze_failure(
        "Prepare participant communications",
        "Email service failed",
    )

    assert result["recoverable"] is True
    assert result["strategy"] == "retry_with_alternative"
    assert result["failed_task"] == "Prepare participant communications"


def test_mission_does_not_claim_success_after_failure():
    mission = create_mission()

    mission.start_task("Find suitable venue")

    state = mission.fail_task(
        "Find suitable venue",
        "Original venue is unavailable",
    )

    assert state["is_complete"] is False
    assert state["status"] == "RECOVERY_REQUIRED"


def test_mission_can_complete():
    mission = create_mission()

    tasks = [
        "Task 1",
        "Task 2",
        "Task 3",
    ]

    for task in tasks:
        mission.start_task(task)
        state = mission.complete_task(task)

    assert state["progress"] == 100
    assert state["is_complete"] is True
    assert state["status"] == "COMPLETED"
