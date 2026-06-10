"""
Daedalus Orchestrator Module (D-08 Mnemosyne).

Central hub for multi-agent task dispatch, state management, and coordination.

Provides:
- AgentRegistry: Discovery and status tracking for 8 Daedalus roles
- TaskDispatcher: Task queuing, routing, and state machine
- StateManager: Global state tracking with snapshots and history
- Coordinator: Main orchestrator integrating all three, with Themis gates

Example:
    from daedalus.orchestrator import AgentRegistry, TaskDispatcher, StateManager, Coordinator
    from daedalus.orchestrator import TaskPriority, AgentStatus
    
    # Initialize
    registry = AgentRegistry()
    dispatcher = TaskDispatcher()
    state = StateManager()
    coordinator = Coordinator(registry, dispatcher, state)
    
    # Register agents
    registry.register("Themis", {"approval", "review"})
    registry.register("Aegis", {"safety_check", "validation"})
    
    # Dispatch an issue
    context = DispatchContext(issue_id=10, task_type="memory")
    task = coordinator.dispatch_issue(context)
    
    # Assign to agent
    coordinator.dispatch_to_agent(task, "Themis")
    coordinator.start_task(task)
    
    # ... agent executes ...
    
    coordinator.complete_task(task, {"pr_number": 11})
"""

from .agent_registry import (
    AgentRegistry,
    Agent,
    AgentStatus,
)

from .task_dispatcher import (
    TaskDispatcher,
    Task,
    TaskPriority,
    TaskState,
)

from .state_manager import (
    StateManager,
    IssueState,
    AgentState,
    TaskState as TaskStateRecord,
    StateSnapshot,
    StateTransition,
)

from .coordinator import (
    Coordinator,
    DispatchContext,
)

__all__ = [
    # Registry
    "AgentRegistry",
    "Agent",
    "AgentStatus",
    
    # Dispatcher
    "TaskDispatcher",
    "Task",
    "TaskPriority",
    "TaskState",
    
    # State
    "StateManager",
    "IssueState",
    "AgentState",
    "TaskStateRecord",
    "StateSnapshot",
    "StateTransition",
    
    # Coordinator
    "Coordinator",
    "DispatchContext",
]
