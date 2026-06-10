"""
BUILDER (Phase 2)

Generates code proposals from implementation plans.

Input: ImplementationPlan
Output: Code files (mocked in V0.1)
"""

from .code_generator import generate_code, CodeProposal

__all__ = ["generate_code", "CodeProposal"]
