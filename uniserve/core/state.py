from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class MissionState:
    mission_id: str
    objective: str
    status: str = "READY"
    total_tasks: int = 0
    completed_tasks: List[str] = field(default_factory=list)
    failed_tasks: List[str] = field(default_factory=list)
    current_task: Optional[str] = None

    @property
    def progress(self) -> int:
        if self.total_tasks == 0:
            return 0

        completed = len(self.completed_tasks)
        return int((completed / self.total_tasks) * 100)

    @property
    def is_complete(self) -> bool:
        return (
            self.total_tasks > 0
            and len(self.completed_tasks) >= self.total_tasks
        )