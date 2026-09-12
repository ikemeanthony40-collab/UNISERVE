from backend.mission_engine.models import MissionRequest
from backend.orchestration.orchestrator import MissionOrchestrator


def print_header():
    print()
    print("=" * 72)
    print("                    UNISERVE")
    print("             AUTONOMOUS MISSION CONTROL")
    print("=" * 72)
    print()


def print_mission(mission):
    print()
    print("-" * 72)
    print("MISSION")
    print("-" * 72)
    print(f"Title:     {mission.title}")
    print(f"Objective: {mission.objective}")
    print(f"Status:    {mission.status.value.upper()}")
    print()

    print("-" * 72)
    print("MISSION TASKS")
    print("-" * 72)

    for number, task in enumerate(mission.tasks, start=1):
        status = task.status.value.upper()

        print(f"\n[{number}] {task.title}")
        print(f"    Agent:   {task.agent}")
        print(f"    Status:  {status}")

        if task.description:
            print(f"    Action:  {task.description}")

        if task.error:
            print(f"    ERROR:   {task.error}")

        if task.result:
            for key, value in task.result.items():
                print(f"    {key}: {value}")

    print()
    print("-" * 72)
    print("EVENT TRACE")
    print("-" * 72)

    for event in mission.events:
        event_type = event["type"]
        payload = event["payload"]

        print(f"  {event_type}")
        if payload:
            for key, value in payload.items():
                print(f"      {key}: {value}")

    print()
    print("=" * 72)

    if mission.status.value == "completed":
        print("                 ✓ MISSION COMPLETED")
    else:
        print(f"                 MISSION {mission.status.value.upper()}")

    print("=" * 72)
    print()


def main():
    print_header()

    objective = (
        "Prepare and execute a technology training "
        "programme for 50 participants."
    )

    print("OBJECTIVE RECEIVED")
    print(f"> {objective}")
    print()
    print("UNISERVE is analysing the mission...")
    print()

    request = MissionRequest(objective)

    orchestrator = MissionOrchestrator()

    mission = orchestrator.create_mission(request)

    print(f"Mission plan created: {len(mission.tasks)} tasks")
    print("Beginning autonomous execution...")
    print()

    mission = orchestrator.run(mission)

    # Include all events generated during execution.
    mission.events.extend(
        event
        for event in orchestrator.events.history
        if event not in mission.events
    )

    print_mission(mission)


if __name__ == "__main__":
    main()