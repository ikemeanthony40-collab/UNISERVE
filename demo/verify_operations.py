from uniserve.agent.uniserve_agent import create_uniserve_agent
from uniserve.tools.operations_tools import (
    create_mission_deliverable,
    verify_mission_deliverable,
)

agent = create_uniserve_agent()

print("UNISERVE AGENT READY")
print("Operations tools:")
print(" - create_mission_deliverable")
print(" - verify_mission_deliverable")
