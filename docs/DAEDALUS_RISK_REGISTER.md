# Daedalus Risk Register

**Version:** 0.1  
**Updated:** 2026-06-10  
**Purpose:** Track known risks and mitigations for V0.1 operational scaffold

---

## Risk Classification Matrix

| Risk ID | Category | Issue | Impact | Likelihood | Severity | Mitigation | Status |
|---------|----------|-------|--------|------------|----------|-----------|--------|
| R-001 | Scope Creep | Daedalus operates outside issue directives | Uncontrolled behavior | High | CRITICAL | Issue-driven gate; refuse out-of-scope requests | ACTIVE |
| R-002 | Auth Bypass | Daedalus writes secrets to code | Leaked credentials | Medium | CRITICAL | Aegis blocks credential commits; code scanning | ACTIVE |
| R-003 | Bad Merge | Human accidentally merges to main | Production breakage | Low | CRITICAL | Branch protection; no-commit rules for Daedalus | ACTIVE |
| R-004 | Test Gap | Tests don't cover edge cases | Undetected bugs | Medium | HIGH | >80% coverage mandate; test review gate | ACTIVE |
| R-005 | Arch Violation | Code breaks Mnemosyne design | System degradation | Medium | HIGH | Iris audit; architecture linter | ACTIVE |
| R-006 | Ambiguous Issue | Requirement interpretation fails | Wrong code built | Medium | HIGH | Issue template; clarity checklist | ACTIVE |
| R-007 | Mock Drift | Mocked components diverge from real API | Integration fail when real | Medium | MEDIUM | Update mocks when real APIs ship; doc gap | ACTIVE |
| R-008 | Decision Log Loss | Memory not written | Lost audit trail | Low | MEDIUM | Mandatory decision log before PR; CI check | ACTIVE |
| R-009 | Reviewer Skip | CRITICAL bypassed without approval | No oversight | Low | CRITICAL | Themis gate; no merge without sign-off | ACTIVE |
| R-010 | Escalation Ignored | Human escalation not seen | Blocker unresolved | Medium | HIGH | Timeout check; re-escalate if no response 2h | PLANNED |

---

## Active Risks (V0.1)

### R-001: Scope Creep
**What:** Daedalus operates on tasks not in a GitHub issue (free-roaming mode).

**Why It Matters:** Defeats the purpose of issue-driven safety.

**How It Happens:**
- Agent asked to "build something clever"
- No issue ticket created first
- Task invoked via Slack/email instead of GitHub

**Mitigation:**
- ❌ Refuse all non-issue-driven requests
- ✅ Require: "Create GitHub issue first, link here"
- ✅ Log refusal in agent report

**Status:** ACTIVE — V0.1 enforces issue gate

---

### R-002: Auth Bypass (Secrets Leak)
**What:** Daedalus writes API keys, tokens, or credentials to code.

**Why It Matters:** Credentials in Git = permanent public record.

**How It Happens:**
- Issue asks to "add Stripe API integration"
- Builder generates code with hardcoded keys
- Code committed to repo
- Keys exposed on GitHub

**Mitigation:**
- ✅ Aegis scans for secret patterns (API_KEY=, Bearer, password=, etc.)
- ✅ Block commit if secret detected
- ✅ Refuse any issue asking to "hardcode API keys"
- ✅ Mandate: Use `.env` or env vars only
- ✅ Code review checks for credential patterns

**Status:** ACTIVE — Aegis implements detection

---

### R-003: Bad Merge (Production Breakage)
**What:** Code intended for testing merges to `main` production branch.

**Why It Matters:** Breaks user-facing product.

**How It Happens:**
- PR opened on feature branch
- Human accidentally clicks "Merge" to wrong branch
- Code goes live untested
- Users see bugs

**Mitigation:**
- ✅ Branch protection: Feature branches cannot merge to main
- ✅ Daedalus PRs only target `feature/daedalus-*`
- ✅ Explicit rule: No Daedalus code touches main in V0.1
- ✅ Human must manually promote to main after review

**Status:** ACTIVE — GitHub branch rules enforce

---

### R-004: Test Gap (Undetected Bugs)
**What:** Code passes tests but has edge-case bugs.

**Why It Matters:** Bad code ships due to insufficient test coverage.

**How It Happens:**
- Unit tests pass (happy path)
- Edge case not covered (error handling, boundary)
- Code merges untested
- Bug discovered in production

**Mitigation:**
- ✅ >80% code coverage mandate
- ✅ Test review gate (Iris checks coverage report)
- ✅ Integration test requirements
- ✅ Reviewer inspects test quality (not just count)

**Status:** ACTIVE — Coverage checks enforced

---

### R-005: Architecture Violation
**What:** Code breaks Mnemosyne design patterns or module boundaries.

**Why It Matters:** System degrades over time; tech debt accumulates.

**How It Happens:**
- Builder doesn't understand Mnemosyne architecture
- Code violates layer separation (UI logic in persistence layer)
- Circular dependencies introduced
- Module boundaries blurred

**Mitigation:**
- ✅ Iris architecture audit (linter + human review)
- ✅ Architecture rules documented in Constitution
- ✅ Daedalus planner must reference architecture
- ✅ Code review focuses on design compliance

**Status:** ACTIVE — Iris audit enforces

---

### R-006: Ambiguous Issue
**What:** GitHub issue requirements unclear or contradictory.

**Why It Matters:** Builder interprets differently than human intended.

**How It Happens:**
- Issue: "Add feature X"
- No detail on acceptance criteria
- Builder guesses implementation
- Human reviews, "That's not what I meant"
- Time wasted on rework

**Mitigation:**
- ✅ Issue template mandates acceptance criteria
- ✅ Daedalus planner requests clarification if ambiguous
- ✅ Escalate to human before building
- ✅ Require issue review before planning starts

**Status:** ACTIVE — Template + clarification gate

---

### R-007: Mock Drift
**What:** Mocked components don't match real API behavior.

**Why It Matters:** V0.1 mocks work; V1 real APIs fail due to discrepancy.

**How It Happens:**
- V0.1 uses mocked GitHub issue reader
- V1 replaces with real GitHub API
- Real API has different response format
- Integration breaks
- Daedalus fails in real workflow

**Mitigation:**
- ✅ Document mock API contracts explicitly
- ✅ Create adapter layer (easy to swap mock ↔ real)
- ✅ Plan V1 migration path in decision log
- ✅ Update mocks when real APIs deployed

**Status:** ACTIVE — Documented; migration tracked

---

### R-008: Decision Log Loss
**What:** Decision log not written; audit trail incomplete.

**Why It Matters:** Can't trace why decisions made; institutional memory lost.

**How It Happens:**
- Task completes
- Report generated
- Decision log skipped (didn't have time)
- 6 months later: "Why did we build it this way?"

**Mitigation:**
- ✅ Mandatory decision log before PR merge
- ✅ CI check validates decision log exists
- ✅ Template provided (easy to fill)
- ✅ Reporter stage writes decision log automatically

**Status:** ACTIVE — CI enforces

---

### R-009: Reviewer Skip (No Oversight)
**What:** CRITICAL risk bypassed without Themis approval.

**Why It Matters:** Safety gates defeated; dangerous code ships.

**How It Happens:**
- Issue touches auth logic (CRITICAL)
- Aegis flags CRITICAL
- PR opened anyway
- Reviewer forgets to check
- Code merges unreviewed

**Mitigation:**
- ✅ CRITICAL PRs require explicit human approval
- ✅ Themis gate blocks merge if approval missing
- ✅ Clear labeling: "⚠️ CRITICAL — Human review required"
- ✅ Escalation message sent to human

**Status:** ACTIVE — Themis enforces

---

### R-010: Escalation Ignored
**What:** Daedalus escalates to human but request goes unnoticed.

**Why It Matters:** Task hangs; blocker never resolved.

**How It Happens:**
- Escalation sent via agent report
- Human doesn't read it (buried in noise)
- Hours pass
- Task stalled waiting for approval

**Mitigation:**
- ✅ (V0.1) Escalation logged in decision log + PR
- 🔜 (V1) Timeout check: if no response 2h, re-escalate
- 🔜 (V1) Contacting Users: Send message to human
- ✅ Clear escalation format (see Constitution)

**Status:** ACTIVE (V0.1), PLANNED (V1)

---

## Risk Acceptance

### Accepted Risks (by design in V0.1)

| Risk | Why Accepted | Mitigation |
|------|--------------|-----------|
| **Mock APIs** | V0.1 is test/scaffold; real APIs come in V1 | Documented; migration plan in place |
| **No Auto-Merge** | Safety requires human review | Not a problem; intended design |
| **No Prod Deploy** | V0.1 only operates on Life-os | Not a problem; intended scope |
| **Requires Manual Issue Creation** | Issue-driven gate; no autonomous mode | Not a problem; enforces safety |

---

## Risk Monitoring

### Weekly Review
- [ ] Check GitHub issue queue for escalations
- [ ] Review decision logs for patterns
- [ ] Audit git log for unexpected commits
- [ ] Validate test coverage hasn't dropped

### Incident Response
If R-002 (secrets leak) detected:
1. ❌ Stop all operations immediately
2. 📢 Rotate exposed credentials
3. 📝 Log incident + response
4. 🔍 Audit git history for other leaks
5. ✅ Update Aegis detection rules

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-06-10 | Initial risk register for V0.1 scaffold |

