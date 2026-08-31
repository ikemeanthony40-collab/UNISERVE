from datetime import datetime, timezone

class EventBus:
    def __init__(self):
        self.history=[]

    def publish(self, event_type, payload):
        event={"type":event_type,"timestamp":datetime.now(timezone.utc).isoformat(),"payload":payload}
        self.history.append(event)
        return event
