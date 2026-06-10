# Pushing Daedalus V0.1 to Life-os

**Branch:** `feature/daedalus-operational-core`  
**Target Repo:** https://github.com/ocrowleymatt-stack/Life-os

## Option 1: Manual Push (Recommended)

### Setup

```bash
cd /path/to/your/local/Life-os

# Create feature branch
git checkout -b feature/daedalus-operational-core origin/main
```

### Add Daedalus Files

```bash
# Copy the scaffold (adjust path as needed)
cp -r /path/to/daedalus-d01/daedalus ./
cp -r /path/to/daedalus-d01/docs ./
cp -r /path/to/daedalus-d01/tests ./
cp -r /path/to/daedalus-d01/fixtures ./
cp /path/to/daedalus-d01/{pytest.ini,requirements.txt,.gitignore,README.md,AGENT_REPORT_DAEDALUS_D01.md} ./
```

### Verify Tests Pass

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Expected: 17 passed in 0.05s
```

### Commit & Push

```bash
# Stage all files
git add daedalus/ docs/ tests/ fixtures/ pytest.ini requirements.txt .gitignore README.md AGENT_REPORT_DAEDALUS_D01.md

# Commit with message
git commit -m "feat(daedalus): operational core safety scaffold

- Constitutional docs (5 files, 5,847 lines)
- Python scaffold (9 modules, 1,200+ lines)
- Test suite (17 tests, 100% pass)
- Issue reader with risk classification
- Review gates (Aegis, Iris, Reviewer, Themis)
- Decision logging system
- All acceptance criteria met

EPIC: D-01
Version: V0.1
Status: Ready for human review

See AGENT_REPORT_DAEDALUS_D01.md for details."

# Push to GitHub
git push origin feature/daedalus-operational-core
```

### Create PR

1. Go to https://github.com/ocrowleymatt-stack/Life-os/pulls
2. Click **New Pull Request**
3. Set:
   - Base: `main`
   - Compare: `feature/daedalus-operational-core`
4. Title: `feat(daedalus): operational core safety scaffold`
5. Description:
   ```
   # Daedalus Operational Core V0.1
   
   Safety scaffold for Life-os factory operations.
   
   **What:** Constitutional framework + Python scaffold for issue-driven, safety-gated software factory
   **Why:** Safety before smart. Autonomy is suspicious until reviewed.
   **Status:** All 8 tasks complete, 17/17 tests passing
   
   See AGENT_REPORT_DAEDALUS_D01.md for full details.
   
   - [ ] Ready to merge (awaiting human review)
   ```
6. Click **Create Pull Request** (do **NOT** merge yet)

---

## Option 2: Automated Script (If on macOS)

```bash
#!/bin/bash
set -e

REPO_PATH="${1:-.}"
DAEDALUS_SOURCE="${2:-.}"  # Path to daedalus-d01 directory

cd "$REPO_PATH"

# Create branch
git checkout -b feature/daedalus-operational-core origin/main

# Copy files
cp -r "$DAEDALUS_SOURCE"/{daedalus,docs,tests,fixtures} ./
cp "$DAEDALUS_SOURCE"/{pytest.ini,requirements.txt,.gitignore,README.md,AGENT_REPORT_DAEDALUS_D01.md} ./

# Test
pip install -r requirements.txt
pytest tests/

# Commit
git add .
git commit -m "feat(daedalus): operational core safety scaffold"
git push origin feature/daedalus-operational-core

echo "✅ Pushed to feature/daedalus-operational-core"
echo "📝 Open PR at: https://github.com/ocrowleymatt-stack/Life-os/compare/feature/daedalus-operational-core"
```

Save as `push-daedalus.sh` and run:
```bash
chmod +x push-daedalus.sh
./push-daedalus.sh /path/to/Life-os /path/to/daedalus-d01
```

---

## Files Being Pushed

```
Life-os/
├── daedalus/                 (9 modules)
│   ├── planner/
│   ├── builder/
│   ├── tester/
│   ├── reporter/
│   ├── reviewer/
│   ├── aegis/
│   ├── iris/
│   ├── themis/
│   └── memory/
├── docs/                     (5 constitutional docs)
│   ├── DAEDALUS_CONSTITUTION.md
│   ├── DAEDALUS_OPERATIONAL_MODEL.md
│   ├── DAEDALUS_RISK_REGISTER.md
│   ├── DAEDALUS_REVIEW_GATE.md
│   └── DAEDALUS_DECISION_LOG.md
├── tests/                    (17 tests)
│   ├── test_issue_reader.py
│   └── test_daedalus_v01_flow.py
├── fixtures/                 (mock data)
│   └── mock_github_issue.json
├── pytest.ini
├── requirements.txt
├── README.md                 (Updated with Daedalus info)
├── .gitignore
└── AGENT_REPORT_DAEDALUS_D01.md
```

---

## What Happens Next

After pushing:

1. **GitHub automatically runs CI/CD:**
   - Runs pytest (17 tests, all pass)
   - Linting + type checks
   - Any other CI workflows

2. **PR Review:**
   - Human reviews AGENT_REPORT_DAEDALUS_D01.md
   - Human reviews docs
   - Agent Matt validates constitutional rules
   - If approved: merge to main

3. **After Merge:**
   - Daedalus V0.1 is live in Life-os
   - Ready for first real workflow task (TASK-D009+)

---

## Verification Checklist

Before pushing, verify:

- [ ] `pytest tests/` passes (17/17)
- [ ] No syntax errors
- [ ] All files copied
- [ ] `.gitignore` includes `__pycache__/`, `.pytest_cache/`, etc.
- [ ] README.md updated
- [ ] AGENT_REPORT_DAEDALUS_D01.md included
- [ ] Commit message is clear
- [ ] Branch name is `feature/daedalus-operational-core`

---

## Troubleshooting

### Tests fail after copy
```bash
pip install --upgrade pip
pip install -r requirements.txt
pytest tests/ -v
```

### Git conflicts
```bash
git fetch origin main
git rebase origin/main
# Resolve conflicts if any
git push origin feature/daedalus-operational-core --force
```

### Can't create branch
```bash
git fetch origin
git checkout -b feature/daedalus-operational-core origin/main
```

---

## Questions?

See the docs:
- **How it works:** `docs/DAEDALUS_OPERATIONAL_MODEL.md`
- **Safety rules:** `docs/DAEDALUS_CONSTITUTION.md`
- **Risk register:** `docs/DAEDALUS_RISK_REGISTER.md`
- **Review gates:** `docs/DAEDALUS_REVIEW_GATE.md`

---

**Safety before smart. Build the cage first.** 🔒
