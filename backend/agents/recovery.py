class RecoveryAgent:
    def replan(self, mission, task):
        participant_count = mission.memory.get(
            "participant_count",
            0,
        )

        venue_capacity = max(participant_count + 10, 20)

        mission.memory["venue_replanned"] = True

        task.result = {
            "recovery": "Alternative venue selected",
            "capacity": venue_capacity,
            "required": participant_count,
        }