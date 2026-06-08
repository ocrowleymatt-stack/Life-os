# Daedalus

**Standalone Mnemosyne Factory Workshop**

Daedalus is the autonomous software factory for building and maintaining Mnemosyne / Life.

It is not the user-facing memory app. It is the workshop UI and control layer for:

- reading implementation issues
- producing plans
- tracking branches and pull requests
- displaying test results
- generating agent reports
- enforcing Themis approval gates
- surfacing safety blocks
- recording model and cost activity

## Product Boundary

```txt
Life / Mnemosyne = the memory operating layer
Daedalus         = the workshop that builds and maintains it
Themis           = the final approval gate
```

## Workflow

```txt
Issue
→ Plan
→ Branch
→ Code
→ Tests
→ Agent Report
→ PR
→ Themis Review
→ Human approval where required
```

## Safety Defaults

Daedalus starts in safe mode.

Disabled by default:

- production deployment
- autonomous merging
- secret rotation
- auth redesign
- storage redesign
- destructive migrations
- evidence deletion
- audit-log deletion
- sending sensitive evidence to cloud AI

## Initial Stack

- `apps/web` — standalone workshop UI
- `apps/api` — factory API / GitHub bridge
- `prompts` — Mnemosyne Factory operating prompt
- `agents` — Daedalus, Athena, Argus, Aegis, Iris, Chronos, Morpheus, Themis
- `workflows` — task, review and release policies
- `reports` — agent reports

## Status

Bootstrap scaffold. No dangerous automation is enabled.
