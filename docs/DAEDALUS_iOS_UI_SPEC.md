# Daedalus iOS Dashboard — UI Specification

**Version:** 1.0  
**Module:** D-09 (iOS Dashboard)  
**Format:** Static HTML5 + CSS3 (zero build step)  
**Target:** iOS Safari 15+, responsive (mobile-first)

---

## 📐 Design Principles

1. **Static-First** — No server, no JavaScript (except simple progress bars)
2. **Accessibility** — WCAG 2.1 AA, semantic HTML, high contrast dark mode
3. **Responsive** — Mobile (320px), tablet (768px), desktop (1024px)
4. **Transparency** — Show real Daedalus state (roles, issues, memory)
5. **Fast** — No API calls required, works offline with mock data

---

## 🎨 Color Scheme & Role Mapping

### Dark Theme (Primary)
```
Background:   #0a0e27 (dark navy)
Surface:      #1a1f3a (card background)
Border:       #2a2f4a (divider)
Text:         #e0e6ff (light blue-white)
Accent:       #4a90ff (bright blue)
```

### 8-Role Color Map
```
Mnemosyne (Orchestrator)  → #4a90ff (bright blue)
Themis (Approval Gate)    → #ffd700 (gold)
Aegis (Safety Blocker)    → #ff4444 (red)
Athena (Planner)          → #44ff44 (green)
Chronos (Tool Manager)    → #ff88ff (magenta)
Argus (Reviewer)          → #ffaa44 (orange)
Iris (Auditor)            → #ff6699 (pink)
Morpheus (Memory)         → #88ddff (cyan)
```

### Status Indicators
```
IDLE       → ⚪ #888888 (gray)
BUSY       → 🟡 #ffaa00 (amber)
BLOCKED    → 🔴 #ff4444 (red)
NOMINAL    → ✅ #44ff44 (green)
DEGRADED   → ⚠️  #ffaa44 (orange)
CRITICAL   → ❌ #ff4444 (red)
```

### Priority Colors (Issues)
```
HIGH       → #ff4444 (red)
MEDIUM     → #ffaa44 (orange)
LOW        → #44ff44 (green)
```

---

## 📱 Layout & Navigation

### Header (Fixed Top)
```
Daedalus Dashboard  [Status Badge]  [Last Sync: 2026-06-10 13:05]
────────────────────────────────────────────────────────────────
Overview  │  Issues  │  PRs  │  Tasks  │  Memory
```

**Status Badge Colors:**
- ✅ NOMINAL — all systems green
- ⚠️ DEGRADED — 1+ role busy/blocked
- ❌ CRITICAL — system offline or 2+ roles blocked

**Last Sync:** Updates every 30s (mock), shows relative time (e.g., "2m ago")

### Tabs (CSS :checked Radio Buttons)
- No JavaScript required
- Smooth transitions
- Mobile-friendly
- Deep linking via anchor (e.g., `#tab-issues`)

### Responsive Breakpoints
```
320px–599px    → Mobile stack (full width, single column)
600px–999px    → Tablet (2-column)
1000px+        → Desktop (3+ column)
```

---

## 🗂️ Tab 1: Overview

**Purpose:** At-a-glance system health and role status.

### Components

**1. Phase Display**
```
Current Phase: Phase 2
├─ V0.1 Complete (4 PRs, 179 tests) ✅
└─ Phase 2 In Progress
   ├─ D-07 Morpheus (PR #11) 🟡 REVIEW
   ├─ D-09 iOS Dashboard (PR #12) 🟡 REVIEW
   └─ D-08 Mnemosyne (Issue #10) ⚪ IDLE
```

**2. Test Coverage Gauge**
```
Overall Coverage:  ██████████ 100%  (47/47 D-07 tests)
V0.1 + Phase 2:    ██████████ 100%  (226/226 tests)
```

**3. Role Status Grid (8 Cards)**
Each card:
```
┌─────────────────────────────────┐
│ 🔵 MNEMOSYNE                    │
├─────────────────────────────────┤
│ Status: IDLE                    │
│ Last Activity: 10 min ago       │
│ Health: ✅ NOMINAL              │
│ Type: Orchestrator              │
└─────────────────────────────────┘
```

**Grid Layout:**
- Mobile: 2 columns
- Tablet: 4 columns
- Desktop: 4 columns (flexible)

**Card Colors:** Each role has its assigned color (see Color Map)

**Status Indicators:**
```
IDLE     → ⚪ Gray (waiting)
BUSY     → 🟡 Amber (active)
BLOCKED  → 🔴 Red (escalated)
```

**Example Timeline (Last Activity):**
```
< 1 min ago  → "now"
< 5 min      → "5 min ago"
< 1 hour     → "30 min ago"
> 1 hour     → "2 hours ago"
```

---

## 🗂️ Tab 2: Issues

**Purpose:** Track open GitHub issues and acceptance criteria.

### Components

**1. Issue List**
```
#8  D-07 Morpheus Memory System
    Priority: HIGH    Assignee: System    Status: ✅ MERGED
    ├─ Acceptance: [✅✅✅✅✅✅✅✅✅✅✅] 11/11 criteria
    └─ Description: Memory system with TTL, context...

#9  D-09 iOS Dashboard
    Priority: MEDIUM  Assignee: System    Status: 🟡 IN PROGRESS
    ├─ Acceptance: [✅✅✅✅✅✅✅⬜⬜⬜] 7/10 criteria
    └─ Description: Static HTML UI with 5 tabs...

#10 D-08 Mnemosyne Orchestrator
    Priority: HIGH    Assignee: System    Status: ⚪ TODO
    ├─ Acceptance: [⬜⬜⬜⬜⬜⬜⬜⬜] 0/8 criteria
    └─ Description: Multi-agent coordination engine...
```

**Priority Coloring:**
- HIGH (red bg) → Bold text, top of list
- MEDIUM (orange bg) → Normal weight
- LOW (green bg) → Dimmer

**Status Icons:**
```
⚪ TODO         → Not started
🟡 IN PROGRESS → Active work
🟢 REVIEW      → PR open
✅ MERGED      → Complete
❌ BLOCKED     → Escalated
```

**2. Expandable Details (CSS :checked)**
```
Click issue header → Expand to show:
├─ Full description
├─ All acceptance criteria (checklist)
├─ Links to PR(s)
├─ Assignee avatar + name
└─ Comments (if any)
```

**3. Filter Buttons (Display Toggle)**
```
[All] [Open] [In Progress] [Review] [Blocked]
(CSS :checked on hidden input)
```

---

## 🗂️ Tab 3: PRs

**Purpose:** Track pull requests and CI/test status.

### Components

**1. PR List**
```
#11 feat: D-07 Morpheus Memory System
    Branch: feature/d07-morpheus-memory
    Status: [REVIEW ▶ READY]
    Tests: 47/47 ✅ PASS
    GitHub: https://github.com/.../pull/11
    Created: 2026-06-10
```

**2. Status Badges**
```
[DRAFT]  → Editing, no CI
[REVIEW] → CI passing, awaiting review
[READY]  → All checks green, mergeable
```

**3. Test Result Summary**
```
✅ 47 passed
❌ 0 failed
⏭️ 0 skipped
⏱️ 25.3s
```

**4. Merge Status (Read-Only Display)**
```
Reviewers: 1 approved
Checks: All passing ✅
Conflicts: None
Merge Status: Ready (manual merge required)
```

---

## 🗂️ Tab 4: Tasks

**Purpose:** Show active Daedalus workflows and progress.

### Components

**1. Active Task List**
```
Task 001 (D-07 Morpheus Memory)
├─ Issue: #8
├─ Current Agent: Argus (Reviewer)
├─ Progress: [████████░░░░] 8/12 steps
├─ ETA: ~15 min
└─ Steps:
   ✅ Code generation
   ✅ Test execution
   ✅ Risk classification
   🟡 Iris audit (in progress)
   ⬜ Themis approval
   ⬜ GitHub PR
   ⬜ Reporting

Task 002 (D-09 iOS Dashboard)
├─ Issue: #9
├─ Current Agent: Code Gen
├─ Progress: [████░░░░░░░░] 2/12 steps
├─ ETA: ~90 min
└─ Steps:
   ✅ Scope analysis
   🟡 Design spec (in progress)
   ⬜ HTML build
   ...
```

**2. Progress Bar (JavaScript Allowed Here)**
```html
<progress value="8" max="12"></progress>
<!-- Plus CSS styling for color matching role -->
```

**3. Agent Timeline**
```
Mnemosyne → Aegis → Athena → Chronos → Code Gen → Argus → Iris → Themis → Done
   ✅         ✅       ✅        ✅          ✅       🟡      ⬜      ⬜
```

---

## 🗂️ Tab 5: Memory

**Purpose:** Debug memory system and view stored trajectories.

### Components

**1. Memory Stats Card**
```
┌──────────────────────────────────┐
│ Memory System (Morpheus)         │
├──────────────────────────────────┤
│ Total Entries:     487           │
│ Average TTL:       24 hours      │
│ Retrieval Latency: 12 ms         │
│ Storage:           2.3 MB        │
│ Last Cleanup:      3 min ago     │
└──────────────────────────────────┘
```

**2. Recent Entries Table**
```
Timestamp          │ Key                      │ Size    │ TTL
───────────────────┼──────────────────────────┼─────────┼─────────
2026-06-10 13:05   │ issue:8:acceptance       │ 2.1 KB  │ 24h
2026-06-10 13:04   │ pr:11:test_results       │ 1.8 KB  │ 48h
2026-06-10 13:03   │ role:morpheus:state      │ 0.9 KB  │ ∞
2026-06-10 13:02   │ context:d07:window       │ 5.2 KB  │ 12h
...
```

**3. Search Box**
```
Search Memory: [                    ]
Results (live):
├─ issue:9:title (0.8 KB)
├─ issue:9:description (2.1 KB)
└─ issue:9:acceptance (0.5 KB)
```

**4. Memory Scope Indicator**
```
Scopes:
├─ ✅ Global       (100 entries)
├─ ✅ Agent        (287 entries)
└─ ✅ Conversation (100 entries)
```

---

## 🎯 HTML Structure

### Skeleton
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Daedalus Dashboard</title>
  <style>/* embedded CSS */</ style>
</head>
<body>
  <!-- Header with status -->
  <header>
    <h1>Daedalus Dashboard</h1>
    <div class="status-badge">✅ NOMINAL</div>
    <div class="last-sync">Last Sync: now</div>
  </header>

  <!-- Tab Navigation -->
  <nav class="tabs">
    <input type="radio" id="tab-overview" name="tabs" checked>
    <label for="tab-overview">Overview</label>
    <!-- ... other tabs ... -->
  </nav>

  <!-- Tab Content (CSS :checked display) -->
  <main class="tab-content">
    <section id="tab-overview-content"><!-- content --></section>
    <!-- ... other sections ... -->
  </main>

  <!-- Inline SVG Icons -->
  <svg style="display:none;"><!-- icons --></svg>

  <!-- Mock Data (JSON) -->
  <script type="application/json" id="mock-data">
    {
      "roles": [ ... ],
      "issues": [ ... ],
      "prs": [ ... ],
      "tasks": [ ... ],
      "memory": { ... }
    }
  </script>

  <!-- Simple JavaScript (Progress, Search) -->
  <script>
    // Tab switching (CSS, no JS needed)
    // Memory search (simple filter)
    // Progress bar updates (if real data)
  </script>
</body>
</html>
```

---

## 🎨 Styling Approach

### CSS Variables (Theming)
```css
:root {
  --bg-primary: #0a0e27;
  --bg-surface: #1a1f3a;
  --text-primary: #e0e6ff;
  --accent: #4a90ff;
  
  --role-mnemosyne: #4a90ff;
  --role-themis: #ffd700;
  /* ... */
}
```

### Component Classes
```
.card              → bordered box, dark surface
.badge             → small label, role color
.tab-nav           → horizontal nav, :checked styling
.progress-bar      → visual progress, role color
.status-icon       → status indicator (⚪🟡🔴)
.role-grid         → 2/4 column layout
.issue-list        → expandable items
.table-responsive  → horizontal scroll on mobile
```

### Responsive Helpers
```css
@media (max-width: 599px) {
  /* Single column, full width */
  .grid { columns: 1; }
}

@media (min-width: 600px) and (max-width: 999px) {
  /* Two columns */
  .grid { columns: 2; }
}

@media (min-width: 1000px) {
  /* Multi-column desktop */
  .grid { columns: auto-fit; }
}
```

---

## ♿ Accessibility (WCAG 2.1 AA)

### Semantic HTML
```html
<header><!-- page header --></header>
<nav><!-- navigation --></nav>
<main><!-- main content --></main>
<section><!-- logical sections --></section>
<article><!-- self-contained content --></article>
```

### ARIA Labels
```html
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="tab-overview-content">
    Overview
  </button>
</div>
<div role="tabpanel" id="tab-overview-content"><!-- content --></div>
```

### Color Contrast
- Text vs background: 7:1 ratio (AAA standard)
- Badges vs background: 4.5:1 ratio (AA standard)
- Tested with WCAG contrast checker

### Keyboard Navigation
- Tab through all interactive elements
- Enter/Space to activate
- Escape to close (if applicable)
- No keyboard traps

### Screen Reader Support
- Descriptive link text (not "click here")
- Image alt text (if any)
- Form labels (`<label for>`)
- ARIA live regions (if updates)

---

## 🧪 Testing Strategy

### HTML Validation
- W3C HTML5 validator (no errors)
- Semantic tags used correctly
- No deprecated attributes

### CSS Coverage
- All classes used (no dead styles)
- All breakpoints tested
- Print styles (if needed)

### Accessibility Testing
```
✅ Color contrast (7:1 text, 4.5:1 badges)
✅ Semantic HTML
✅ Keyboard navigation (Tab, Enter, Escape)
✅ ARIA labels (tabs, buttons, regions)
✅ Screen reader (NVDA, JAWS simulation)
```

### Responsive Testing
```
✅ 320px (mobile)
✅ 425px (mobile landscape)
✅ 768px (tablet)
✅ 1024px (desktop)
```

### Browser Testing
```
✅ iOS Safari 15.0
✅ iOS Safari 16.0
✅ Safari (macOS)
✅ Chrome (desktop)
```

---

## 📦 File Deliverables

| File | Lines | Purpose |
|------|-------|---------|
| `daedalus-dashboard.html` | ~850 | Main dashboard (all 5 tabs, mock data) |
| `assets/style.css` | ~400 | Styling, responsive, dark mode |
| `assets/icons.svg` | ~150 | Role + status SVG icons |
| `DAEDALUS_iOS_UI_SPEC.md` | ~600 | This spec |
| `test_ios_dashboard.py` | ~300 | HTML validation + accessibility tests |

---

## 🚀 Deployment & Usage

### Local Development
```bash
# Open in browser (no server needed)
open daedalus-dashboard.html
```

### iOS Safari
```
1. Save HTML to iCloud Drive / Files
2. Open in Safari
3. Add to Home Screen (web app)
4. Full screen, no address bar
```

### Real Data Integration (Future)
```javascript
// Replace mock data with API calls
const data = await fetch('/.tasklet/agent-db/roles').then(r => r.json());
// Populate from real state
```

---

## 📝 Notes

- **No Build Step:** HTML, CSS, SVG are served as-is
- **Offline-Capable:** Works without network (mock data embedded)
- **Mobile-First:** Designed for iOS Safari 15+
- **Accessibility-Focused:** WCAG 2.1 AA compliance
- **Dark Mode:** Reduces eye strain, modern aesthetic
- **Real Data Ready:** Mock data can be replaced with API calls
