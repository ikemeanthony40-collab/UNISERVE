from backend.tools.registry import ToolRegistry
from backend.tools.mission_tools import (
    analyse_requirements,
    determine_resources,
    create_schedule,
    prepare_communications,
    generate_documents,
    confirm_venue,
    verify_readiness,
)


def create_tool_registry():
    registry = ToolRegistry()

    registry.register(
        "analyse_requirements",
        "Analyse a mission objective and identify success criteria.",
        analyse_requirements,
    )

    registry.register(
        "determine_resources",
        "Determine resources required for a mission.",
        determine_resources,
    )

    registry.register(
        "create_schedule",
        "Create an operational schedule.",
        create_schedule,
    )

    registry.register(
        "prepare_communications",
        "Prepare participant communications.",
        prepare_communications,
    )

    registry.register(
        "generate_documents",
        "Generate mission and operational documents.",
        generate_documents,
    )

    registry.register(
        "confirm_venue",
        "Confirm a suitable venue for the mission.",
        confirm_venue,
    )

    registry.register(
        "verify_readiness",
        "Verify that all mission requirements are satisfied.",
        verify_readiness,
    )

    return registry