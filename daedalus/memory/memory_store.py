"""Memory store (mocked for V0.1)."""

def store_decision(task_id: str, decision_log_markdown: str) -> bool:
    """Store decision log (mocked - would write to DB in V1)."""
    return True

def retrieve_decision(task_id: str) -> str:
    """Retrieve decision log (mocked)."""
    return f"# Decision Log — {task_id}\n(Stored in memory)"
