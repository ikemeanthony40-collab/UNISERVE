from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    REPLANNED = "replanned"


class MissionStatus(str, Enum):
    CREATED = "created"
    PLANNING = "planning"
    EXECUTING = "executing"
    REPLANNING = "replanning"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class MissionRequest:
    objective: str
    constraints: dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    title: str
    description: str
    agent: str
    tool: str | None = None
    dependencies: list[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid4())[:8])
    status: TaskStatus = TaskStatus.PENDING
    result: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass
class Mission:
    title: str
    objective: str
    tasks: list[Task] = field(default_factory=list)
    status: MissionStatus = MissionStatus.CREATED
    events: list[dict[str, Any]] = field(default_factory=list)
    memory: dict[str, Any] = field(default_factory=dict)
