from uniserve.tools.mission_tools import create_mission, get_mission_status


def run_assignment(objective: str, tasks: list[str]):
    print("ASSIGNMENT:", objective)

    result = create_mission(objective, tasks)

    print("MISSION CREATED")
    print(result)

    print("STATUS")
    print(get_mission_status())


if __name__ == "__main__":
    run_assignment(
        "Organize a technology conference for 200 people",
        [
            "Define requirements",
            "Find suitable venue",
            "Arrange speakers",
            "Prepare communications",
            "Verify completion",
        ],
    )
