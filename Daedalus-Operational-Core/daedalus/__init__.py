"""
Daedalus Operational Core V0.1

Controlled software factory for Life-os.

Safety before smart.
Autonomy is suspicious until reviewed.
"""

__version__ = "0.1"
__status__ = "Operational Scaffold"

# Lazy imports — only import modules when needed
# This allows Digsbody API to start without loading all 8 Daedalus phases

__all__ = [
    "planner",
    "builder",
    "tester",
    "reporter",
    "reviewer",
    "memory",
    "aegis",
    "iris",
    "themis",
]