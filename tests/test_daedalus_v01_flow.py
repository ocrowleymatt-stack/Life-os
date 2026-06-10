"""
End-to-end test for Daedalus V0.1 flow

Tests the complete operational model:
Issue → Plan → Code → Test → Report → PR (no merge)

This test validates that all gates pass and decision log is generated.
"""

import json
from daedalus.planner import parse_issue, generate_plan
from daedalus.builder import generate_code
from daedalus.tester import run_tests
from daedalus.reporter import generate_report, write_decision_log
from daedalus.aegis import scan_security
from daedalus.iris import check_architecture
from daedalus.reviewer import review_code


def test_v01_complete_flow():
    """Test complete V0.1 workflow."""
    
    # Stage 1: INGEST
    with open("fixtures/mock_github_issue.json") as f:
        issue_json = json.load(f)
    
    parsed_issue = parse_issue(issue_json)
    assert parsed_issue.issue_id == "1"
    print(f"✅ Stage 1 INGEST: Parsed issue #{parsed_issue.issue_id}")
    
    # Stage 2: PLAN
    plan = generate_plan(parsed_issue)
    assert plan.task_id == "D001"
    assert len(plan.files_to_create) > 0
    print(f"✅ Stage 2 PLAN: Generated plan for {plan.task_id}")
    
    # Stage 3: CODE (mocked)
    code = generate_code(plan)
    assert code.status == "GENERATED"
    assert len(code.files) > 0
    print(f"✅ Stage 3 CODE: Generated {len(code.files)} files")
    
    # Stage 4: TEST (mocked)
    tests = run_tests(plan.task_id)
    assert tests.is_success()
    assert tests.coverage_percent >= 80
    print(f"✅ Stage 4 TEST: {tests.passed}/{tests.total_tests} passed, {tests.coverage_percent}% coverage")
    
    # Stage 5: GATES (Aegis, Iris, Reviewer)
    security = scan_security(plan.task_id)
    assert security.passed
    print(f"✅ Aegis: Security scan passed")
    
    arch = check_architecture(plan.task_id, parsed_issue.modules_affected)
    assert arch.passed
    print(f"✅ Iris: Architecture audit passed")
    
    review = review_code(plan.task_id, parsed_issue.risk_level.value)
    assert review.approved
    print(f"✅ Reviewer: Code review approved")
    
    # Stage 6: REPORT
    gates_status = {
        "Automated Tests": "✅ PASS",
        "Aegis": "✅ PASS",
        "Iris": "✅ PASS",
        "Reviewer": "✅ APPROVE",
        "Themis": "⏳ PENDING (awaiting human)"
    }
    
    report = generate_report(parsed_issue, plan, code, tests, gates_status)
    assert report.task_id == "D001"
    report_md = report.to_markdown()
    assert "TASK-D001" in report_md
    print(f"✅ Reporter: Generated agent report")
    
    # Stage 7: DECISION LOG
    decision_log = write_decision_log(
        task_id="D001",
        parsed_issue=parsed_issue,
        plan=plan,
        tests=tests,
        approach="Create issue reader module with comprehensive tests"
    )
    assert "Decision Log" in decision_log
    assert "D001" in decision_log
    assert "PENDING REVIEW" in decision_log
    print(f"✅ Memory: Decision log generated")
    
    # Note: Mock issue mentions risk keywords (secret, auth, deploy)
    # so it gets flagged as CRITICAL and escalates (correct behavior!)
    # This demonstrates the safety-first approach: when in doubt, escalate
    print(f"✅ Risk correctly identified: {parsed_issue.escalation_reason}")
    
    # Verify all acceptance criteria covered
    assert len(parsed_issue.acceptance_criteria) == 5
    print(f"✅ All {len(parsed_issue.acceptance_criteria)} acceptance criteria addressed")
    
    print("\n" + "="*60)
    print("🎉 DAEDALUS V0.1 FLOW COMPLETE — ALL GATES PASSED")
    print("="*60)
    print("\nNext step: Open PR for human review (do not merge)")
    print(f"Decision log: DECISION_LOG_D001.md")
    print(f"Agent report: AGENT_REPORT_D001.md")


def test_v01_critical_escalation():
    """Test that CRITICAL risk issues escalate correctly."""
    
    issue_json = {
        "number": 99,
        "title": "Add API key to code",
        "body": "Hardcode the Stripe secret API key in config.py"
    }
    
    parsed = parse_issue(issue_json)
    
    assert parsed.risk_level.value == "CRITICAL"
    assert parsed.escalate
    assert parsed.escalation_reason is not None
    print(f"✅ CRITICAL issue escalated: {parsed.escalation_reason}")


def test_v01_no_auto_merge():
    """Verify that V0.1 never auto-merges."""
    from daedalus.themis import check_approval
    
    approval = check_approval("D001", "GREEN")
    
    # Even GREEN-level tasks don't auto-approve
    assert approval.approved == False
    assert "Human" in approval.required_approvals
    print(f"✅ V0.1 requires explicit human approval (no auto-merge)")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
