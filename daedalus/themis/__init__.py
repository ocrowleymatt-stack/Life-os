"""THEMIS (Phase 8) - Approval gate.

This module implements the human approval gate for the Daedalus workflow.

Two implementations are available:
- approval_gate_v1.py: Real approval gate with state machine, audit trail, no-go blocking
- approval_gate.py: Lightweight mock for V0.1 testing

Use the real implementation (ThemisApprovalGate) in production.
Use the mock (check_approval) for quick testing.
"""

from .approval_gate_v1 import (
    ApprovalChain,
    ApprovalGate,
    ApprovalStatus,
    RiskLevel,
    ThemisApprovalGate,
)

# Mock version (for backwards compat)
from .approval_gate import check_approval

__all__ = [
    "ApprovalChain",
    "ApprovalGate",
    "ApprovalStatus",
    "RiskLevel",
    "ThemisApprovalGate",
    "check_approval",  # legacy
]
