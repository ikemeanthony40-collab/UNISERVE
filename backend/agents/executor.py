class ExecutionAgent:
    def execute(self, task, mission):
        if task.title=="Confirm venue" and not mission.memory.get("venue_replanned"):
            return False, {"reason":"Original venue unavailable"}
        return True, {"message":task.title+" completed"}
