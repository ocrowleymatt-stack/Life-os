"""
REPORTER (Phase 4)

Generates agent reports and decision logs.

Input: Plan, Code, Tests, Reviews
Output: Agent report + Decision log (markdown)
"""

from .report_generator import generate_report, AgentReport
from .decision_logger import write_decision_log

__all__ = ["generate_report", "AgentReport", "write_decision_log"]
