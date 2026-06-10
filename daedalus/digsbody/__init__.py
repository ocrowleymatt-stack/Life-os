"""
Digsbody Operator Module — General-purpose user task assistant

Three modes:
- Draft: prepare content only
- Review: show proposed actions + risk classification
- Execute: run after human approval (disabled by default)

Safety model: SAFE / REVIEW_REQUIRED / BLOCKED
"""

__version__ = "1.0.0"

from daedalus.digsbody.policy import TaskClassifier, ClassificationLevel
from daedalus.digsbody.schemas import TaskRequest, TaskResponse, ReviewReport
from daedalus.digsbody.service import DigsbodyService
from daedalus.digsbody.task_log import TaskLogger

__all__ = [
    "TaskClassifier",
    "ClassificationLevel",
    "TaskRequest",
    "TaskResponse",
    "ReviewReport",
    "DigsbodyService",
    "TaskLogger",
]
