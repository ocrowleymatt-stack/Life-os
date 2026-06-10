"""
Daedalus Operational Core V0.1

Controlled software factory for Life-os.

Safety before smart.
Autonomy is suspicious until reviewed.
"""

__version__ = "0.1"
__status__ = "Operational Scaffold"

# Phase imports
from . import planner
from . import builder
from . import tester
from . import reporter
from . import reviewer
from . import memory
from . import aegis
from . import iris
from . import themis

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
