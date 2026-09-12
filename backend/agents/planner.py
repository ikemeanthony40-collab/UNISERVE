from backend.mission_engine.models import Task

class MissionPlanner:
    def create_plan(self, objective):
        return [
            Task("Analyse mission requirements","Identify requirements and success criteria.","planner"),
            Task("Determine required resources","Identify venue, equipment, personnel and materials.","researcher",["Analyse mission requirements"]),
            Task("Create programme schedule","Build the training schedule.","planner",["Determine required resources"]),
            Task("Prepare participant communications","Prepare invitations and instructions.","communications",["Create programme schedule"]),
            Task("Generate mission documents","Create the programme and operational checklist.","execution",["Prepare participant communications"]),
            Task("Confirm venue","Verify a suitable venue for 50 participants.","execution",["Determine required resources"]),
            Task("Verify mission readiness","Check that all critical requirements are satisfied.","verification",["Generate mission documents","Confirm venue"]),
        ]
