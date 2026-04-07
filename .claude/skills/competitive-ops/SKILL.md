---
name: competitive-ops
description: AI competitive intelligence pipeline -- analyze competitors, generate reports, track changes
user_invocable: true
args: mode company
---

# Competitive-Ops -- Router

## Mode Routing

Determine the mode from `{{mode}}`:

| Input | Mode |
|-------|------|
| (empty / no args) | `discovery` -- Show command menu |
| `add <company>` | `add` -- Add competitor to tracking |
| `analyze <company>` | `analyze` -- Full analysis with SWOT + report |
| `compare <A> vs <B>` | `compare` -- Side-by-side comparison |
| `update <company>` | `update` -- Check for changes |
| `pricing <company>` | `pricing` -- Pricing research |
| `batch` | `batch` -- Batch processing |
| `report` | `report` -- Generate consolidated report |
| `track` | `track` -- View tracking dashboard |

---

## Discovery Mode (no arguments)

Show this menu:

```
competitive-ops -- Competitive Intelligence Command Center

Available commands:
  /comp add <company>      → Add competitor to tracking
  /comp analyze <company>  → Full analysis: SWOT + scoring + HTML report
  /comp compare <A> vs <B> → Side-by-side feature matrix
  /comp update <company>   → Check for changes since last analysis
  /comp pricing <company> → Pricing research with change detection
  /comp batch              → Batch process multiple competitors
  /comp report             → Generate consolidated report
  /comp track             → View tracking dashboard

First time? Run /comp setup to configure your company info.
```

---

## Setup Mode

If `{{mode}}` is "setup", check if the system is configured:

1. Check if `cv.md` exists with company info
2. Check if `config/profile.yml` exists
3. Check if `data/competitors.md` exists

If any are missing, guide the user through setup:
- Copy `cv.md.template` to `cv.md` and fill in company info
- Copy `config/profile.yml.example` to `config/profile.yml`
- Create `data/competitors.md` from template

---

## Add Mode

When `{{mode}}` is `add`:

1. Read `{{company}}` from args
2. Check if competitor already exists in `data/competitors.md`
3. If new, add entry with tier assignment (Tier 1/2/3)
4. Create initial research structure
5. Output confirmation with tier and initial score placeholder

---

## Analyze Mode

When `{{mode}}` is `analyze`:

1. Read `{{company}}` from args
2. Run research:
   - Tavily search for company info
   - Web search for news and reviews
   - Cross-validate from multiple sources
3. Generate SWOT analysis
4. Score across 6 dimensions
5. Generate report in `data/reports/{company}-{date}.md`
6. Generate HTML report (if configured)
7. Update `data/competitors.md`
8. Output summary with score and confidence

---

## Compare Mode

When `{{mode}}` is `compare`:

1. Parse `A vs B` from args
2. Load both companies' latest reports
3. Generate feature matrix comparison
4. Score delta analysis
5. Output side-by-side comparison

---

## Update Mode

When `{{mode}}` is `update`:

1. Read `{{company}}` from args
2. Re-run Tavily search to detect changes
3. Compare to last snapshot in `data/snapshots/`
4. If significant change detected (threshold: 5%), alert user
5. Update report and snapshot
6. Output changelog

---

## Pricing Mode

When `{{mode}}` is `pricing`:

1. Read `{{company}}` from args
2. Research pricing from:
   - Company website
   - G2, Capterra, Glassdoor
   - News articles
3. Compare to last pricing snapshot
4. If change detected, alert user
5. Update `data/snapshots/pricing/{company}.json`
6. Output pricing table

---

## Batch Mode

When `{{mode}}` is `batch`:

1. Read list of companies from `data/batch-queue.md` (or prompt user)
2. Run analyze mode for each in parallel (max 5 concurrent)
3. Track progress in `data/batch-status.json`
4. Consolidate results
5. Output batch summary

---

## Report Mode

When `{{mode}}` is `report`:

1. Check for filters in args (company, date range)
2. Aggregate all reports in `data/reports/`
3. Generate consolidated report
4. Generate HTML (if configured)
5. Output path to report

---

## Track Mode

When `{{mode}}` is `track`:

1. Read `data/competitors.md`
2. Display dashboard:
   - All competitors with scores
   - Last updated dates
   - Alert indicators (stale data, significant changes)
   - Filter by tier, score, status
3. Output formatted table

---

## Shared Context

All modes have access to:

- `cv.md` -- Your company/product definition
- `config/profile.yml` -- Configuration
- `config/sources.yml` -- Trusted data sources
- `modes/_shared.md` -- Scoring system, archetypes, rules
- `modes/_profile.md` -- Your customizations

---

## Scoring System

| Dimension | Weight |
|-----------|--------|
| Product Maturity | 20% |
| Feature Coverage | 20% |
| Pricing | 15% |
| Market Presence | 15% |
| Growth Trajectory | 10% |
| Brand Strength | 10% |

**Confidence Levels:**
- 🟢 High: 3+ sources agree
- 🟡 Medium: 2 sources agree
- 🔴 Low: Conflicting or insufficient data

---

## Archetypes

Classify competitors into:
- **Direct Competitor** -- Same product, same market
- **Indirect Competitor** -- Different approach, same need
- **Emerging Threat** -- New technology, new model
- **Replacement Threat** -- Alternative solution
- **Adjacent Player** -- Overlapping users
- **Reference Model** -- Industry benchmark

---

## Output Locations

| Output | Location |
|--------|----------|
| Reports | `data/reports/{company}-{date}.md` |
| HTML Reports | `data/reports/html/{company}-{date}.html` |
| Snapshots | `data/snapshots/{company}/{type}-{date}.json` |
| Competitor Tracker | `data/competitors.md` |

---

## Next Steps

After routing, execute the selected mode by reading:
- `modes/{mode}.md` for mode-specific instructions
- `modes/_shared.md` for system context
- `modes/_profile.md` for user customizations
