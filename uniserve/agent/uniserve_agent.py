from strands import Agent
from strands.models import BedrockModel

from uniserve.tools.mission_tools import (
    create_mission,
    get_mission_status,
    start_mission_task,
    complete_mission_task,
    fail_mission_task,
    recover_failed_task,
)

from uniserve.tools.operations_tools import (
    create_mission_deliverable,
    verify_mission_deliverable,
)


SYSTEM_PROMPT = """
You are UNISERVE, an autonomous general-purpose operations agent.

You are NOT limited to a predefined assignment, industry, or task list.

For every new user assignment:

1. Understand the user's actual objective.
2. Determine what must be accomplished.
3. Break the assignment into logical executable tasks.
4. Create a mission using create_mission.
5. Check mission state before taking action.
6. Start tasks before executing them.
7. Complete tasks only when the required work has actually been completed.
8. If a task fails, never pretend it succeeded.
9. Use recover_failed_task to determine an alternative strategy.
10. Continue the mission when recovery is possible.
11. Adapt the task sequence when circumstances change.
12. Create a real deliverable when the assignment requires one.
13. Verify the final mission state and deliverable before declaring success.
14. Never claim an external action occurred unless a tool actually performed it.

The user's assignment determines the mission.
Do not assume a particular industry or predefined scenario.

Some tools may currently simulate operational actions. Clearly distinguish
simulated operations from real-world actions.
"""


def create_uniserve_agent():
    model = BedrockModel(
        model_id="us.amazon.nova-2-lite-v1:0",
        region_name="us-east-1",
        temperature=0.2,
        max_tokens=512,
        streaming=False,
    )

    return Agent(
        model=model,
        name="UNISERVE",
        description="General-purpose autonomous operations and mission execution agent",
        system_prompt=SYSTEM_PROMPT,
        tools=[
            create_mission,
            get_mission_status,
            start_mission_task,
            complete_mission_task,
            fail_mission_task,
            recover_failed_task,
            create_mission_deliverable,
            verify_mission_deliverable,
        ],
    )


def main():
    print("=" * 60)
    print("UNISERVE - Autonomous Operations Agent")
    print("=" * 60)

    agent = create_uniserve_agent()

    print("Agent initialized.")
    print("Model: us.amazon.nova-2-lite-v1:0")
    print("General-purpose mission execution enabled.")
    print("Operations deliverable tools enabled.")
    print("=" * 60)

    return agent


if __name__ == "__main__":
    main()
