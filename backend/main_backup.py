from backend.mission_engine.models import MissionRequest
from backend.orchestration.orchestrator import MissionOrchestrator

request = MissionRequest(
    "Prepare and execute a technology training programme for 50 participants."
)
mission = MissionOrchestrator().create_mission(request)
MissionOrchestrator().run(mission)
