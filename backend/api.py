from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.mission_engine.models import MissionRequest
from backend.orchestration.orchestrator import MissionOrchestrator

app = FastAPI(title="UNISERVE Mission Control")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "system": "UNISERVE",
        "status": "online",
        "message": "Autonomous Mission Control API"
    }


@app.post("/mission")
def execute_mission(objective: str):
    request = MissionRequest(objective)
    orchestrator = MissionOrchestrator()

    mission = orchestrator.create_mission(request)
    mission = orchestrator.run(mission)

    mission.events.extend(
        event
        for event in orchestrator.events.history
        if event not in mission.events
    )

    return {
        "title": mission.title,
        "objective": mission.objective,
        "status": mission.status.value,
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "agent": task.agent,
                "tool": task.tool,
                "status": task.status.value,
                "result": task.result,
                "error": task.error,
                "dependencies": task.dependencies,
            }
            for task in mission.tasks
        ],
        "events": mission.events,
        "memory": mission.memory,
    }
