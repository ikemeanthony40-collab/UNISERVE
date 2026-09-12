from backend.agents.executor import ExecutionAgent
from backend.agents.planner import MissionPlanner
from backend.agents.recovery import RecoveryAgent
from backend.events.event_bus import EventBus
from backend.mission_engine.models import Mission, MissionRequest, MissionStatus, TaskStatus

class MissionOrchestrator:
    def __init__(self):
        self.planner=MissionPlanner(); self.executor=ExecutionAgent()
        self.recovery=RecoveryAgent(); self.events=EventBus()

    def create_mission(self, request: MissionRequest):
        m=Mission("Autonomous Technology Training Mission",request.objective,status=MissionStatus.PLANNING)
        m.tasks=self.planner.create_plan(request.objective)
        m.events.append(self.events.publish("MISSION_CREATED",{"objective":request.objective}))
        m.events.append(self.events.publish("PLAN_CREATED",{"task_count":len(m.tasks)}))
        return m

    def run(self,m):
        m.status=MissionStatus.EXECUTING
        while True:
            progressed=False
            for t in m.tasks:
                if t.status!=TaskStatus.PENDING: continue
                if any(next((x.status for x in m.tasks if x.title==d),TaskStatus.PENDING)!=TaskStatus.COMPLETED for d in t.dependencies): continue
                t.status=TaskStatus.RUNNING
                self.events.publish("TASK_STARTED",{"task":t.title})
                ok,result=self.executor.execute(t,m)
                if ok:
                    t.status=TaskStatus.COMPLETED; t.result=result
                    self.events.publish("TASK_COMPLETED",{"task":t.title})
                else:
                    t.status=TaskStatus.FAILED; t.error=result["reason"]
                    self.events.publish("TASK_FAILED",{"task":t.title,"reason":t.error})
                    m.status=MissionStatus.REPLANNING
                    self.events.publish("EXCEPTION_DETECTED",{"task":t.title,"reason":t.error})
                    self.recovery.replan(m,t)
                    self.events.publish("PLAN_UPDATED",{"task":t.title,"recovery":t.result})
                    t.status=TaskStatus.PENDING
                progressed=True
                break
            if all(t.status==TaskStatus.COMPLETED for t in m.tasks):
                m.status=MissionStatus.COMPLETED
                self.events.publish("MISSION_COMPLETED",{"mission":m.title})
                return m
            if not progressed:
                m.status=MissionStatus.FAILED
                return m
