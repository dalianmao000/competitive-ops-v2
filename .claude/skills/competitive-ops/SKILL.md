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
| `analyze <company> [html]` | `analyze` -- Full analysis with SWOT + report (add `html` for HTML output) |
| `compare <A> vs <B> [html]` | `compare` -- Side-by-side comparison (add `html` for HTML output) |
| `update <company>` | `update` -- Check for changes |
| `pricing <company> [html]` | `pricing` -- Pricing research (add `html` for HTML output) |
| `batch` | `batch` -- Batch processing |
| `report [html]` | `report` -- Generate consolidated report (add `html` for HTML output) |
| `track` | `track` -- View tracking dashboard |

---

## Discovery Mode (no arguments)

Show this menu:

```
competitive-ops -- Competitive Intelligence Command Center

Available commands:
  /competitive-ops add <company>      → Add competitor to tracking
  /competitive-ops analyze <company>  → Full analysis: SWOT + scoring + HTML report
  /competitive-ops compare <A> vs <B> → Side-by-side feature matrix
  /competitive-ops update <company>   → Check for changes since last analysis
  /competitive-ops pricing <company> → Pricing research with change detection
  /competitive-ops batch              → Batch process multiple competitors
  /competitive-ops report             → Generate consolidated report
  /competitive-ops track             → View tracking dashboard

First time? Say "setup" to configure your company info.
```

---

## Setup Mode

If `{{mode}}` is "setup":

### Step 1: Install Dependencies

Check for required tools and install if missing:

1. **Playwright** for screenshots (强制安装):
   - Run: `npx playwright install chromium` (无条件执行，确保Chromium可用)
   - Verify: `npx playwright --version`

2. **ui-ux-pro-max** for HTML reports:
   - Install: `npx -y uipro-cli init --ai claude` (in项目目录)
   - Skill 位置: `{project}/.claude/skills/ui-ux-pro-max/`
   - 调用方式: `/skill ui-ux-pro-max`

3. **Tavily MCP** (optional, for fallback search):
   - Correct package name: `tavily-mcp` (NOT `@tavily/tavily-mcp`)
   - Add with: `claude mcp add tavily -- npx -y tavily-mcp`
   - Set API key: `TAVILY_API_KEY=your_key`

4. **Python dependencies** (强制安装，优先使用虚拟环境):
   ```bash
   python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
   ```
   - 或直接安装: `pip install -r requirements.txt` (in项目目录)

### Step 2: Configure System

Check if the system is configured:

1. **Required:** Check if `data/competitors.md` exists
   - If missing, create from template or empty file with headers:
     ```
     # Competitors Tracker
     | # | Company | Tier | Score | Status | Last Updated | Notes |
     |---|---------|------|-------|--------|--------------|-------|
     ```
2. **Optional:** `cv.md` and `config/profile.yml`
   - These define your own product for scoring context
   - Not required for basic competitive analysis
   - If missing, skip and proceed with analysis

### Step 3: Summary

Output setup status:
```
✅ competitive-ops v2 ready!

Installed:
  ✅ Playwright (screenshots)
  ✅ ui-ux-pro-max (HTML reports: npx -y uipro-cli init --ai claude)
  ✅ Tavily MCP (fallback search)
  ✅ Python dependencies

Required:
  ✅ data/competitors.md

Optional (for scoring context):
  [?] cv.md (your product)
  [?] config/profile.yml
```

---

## Add Mode

When `{{mode}}` is `add`:

1. Read `{{company}}` from args
2. Check if competitor already exists in `data/competitors.md`
   - **If exists:** Output warning: "⚠️ {company} already in tracker (score: X)" and skip
   - **If new:** Add entry with tier assignment (Tier 1/2/3)
3. Create initial research structure (snapshot folder)
4. Output confirmation with tier and initial score placeholder

---

## Search Fallback Order

When researching competitors, use this search order:

1. **web-search** → Primary search tool
2. **web-fetch** → Fetch specific URLs for detailed info
3. **Tavily MCP server** → Fallback when native tools unavailable

**Tavily MCP Usage:**
```
Use Tavily MCP server for competitive intelligence search:
- tavily-search for company overview, products, pricing
- tavily-search with topic="business" for business intelligence
- tavily-search with topic="news" for recent news
```

**Fallback Detection:**
- If `web-search` returns no results or error → try `web-fetch`
- If `web-fetch` fails or unavailable → invoke Tavily MCP server
- Always log which search method was used in the report metadata

---

## Analyze Mode

When `{{mode}}` is `analyze`:

1. Read `{{company}}` and optional `{{html}}` flag from args
2. Check if competitor exists in `data/competitors.md`
   - **If new:** Add to `data/competitors.md` first
   - **If exists:** Note: "ℹ️ New analysis for {company}"
3. Run research (following fallback order above):
   - Try web-search first for company info
   - Try web-fetch for specific URLs
   - Fallback to Tavily MCP server if needed
   - Cross-validate from multiple sources
4. Generate SWOT analysis
5. Score across 6 dimensions
6. Generate report in `data/reports/{date}/{company}-{date}.md`
   - **Always creates new file (never overwrites)**
   - **Update symlink** to point to the new report:
     ```bash
     rm -f data/reports/latest/{company}.md
     ln -s ../{date}/{company}-{date}.md data/reports/latest/{company}.md
     ```
     This ensures `latest/` always reflects the most recent analysis, regardless of date.
7. **If `html` flag is present in args:**
   - Read the markdown report
   - Use ui-ux-pro-max skill: `/skill ui-ux-pro-max`
   - Generate Chinese HTML with Tailwind dark theme
   - Save to `data/reports/html/{company}-{date}.html`
8. Update `data/competitors.md` with new score and date
9. Output summary with score and confidence
   - Include path to HTML report if generated

**Note:** For incremental change tracking, use `update` mode instead. `analyze` always creates fresh analysis.

---

## Compare Mode

When `{{mode}}` is `compare`:

1. Parse `A vs B` and optional `{{html}}` flag from args
2. Load both companies' latest reports from `data/reports/latest/`
3. Generate feature matrix comparison
4. Score delta analysis
5. Save comparison to `data/reports/{date}/compare-{A}-vs-{B}-{date}.md`
6. **If `html` flag is present:**
   - Read the comparison markdown
   - Use ui-ux-pro-max skill: `/skill ui-ux-pro-max`
   - Generate Chinese HTML with Tailwind dark theme
   - Save to `data/reports/html/compare-{A}-vs-{B}-{date}.html`
7. Output path to comparison report

---

## Update Mode

When `{{mode}}` is `update`:

1. Read `{{company}}` from args
2. Re-run research (following Search Fallback Order):
   - Try web-search/web-fetch first
   - Fallback to Tavily MCP if unavailable
3. Load the previous report from `data/reports/{company}-{prev-date}.md` as baseline
4. Generate new analysis: SWOT + scores → new `data/reports/{company}-{date}.md`
5. **Diff analysis:** Compare old vs new report, compute score delta per dimension
6. **If score change ≥ 5% on any dimension → alert user with 🔴 flag**
7. Save snapshot to `data/snapshots/{company}/{date}.json`
8. Output:
   - New report path
   - Score delta table (before → after per dimension)
   - Changelog: what changed (new features, pricing changes, etc.)

---

## Pricing Mode

When `{{mode}}` is `pricing`:

1. Read `{{company}}` and optional `{{html}}` flag from args
2. Research pricing from (following fallback order):
   - Company website (try web-fetch first)
   - G2, Capterra, Glassdoor
   - News articles
   - Tavily MCP server as fallback for business intelligence
3. Compare to `data/snapshots/pricing/{company}.json`
4. If change detected, alert user with change details
5. Update `data/snapshots/pricing/{company}.json`
6. Save pricing report to `data/reports/{date}/pricing-{company}-{date}.md`
7. **If `html` flag is present:**
   - Read the pricing report markdown
   - Use ui-ux-pro-max skill: `/skill ui-ux-pro-max`
   - Generate Chinese HTML with Tailwind dark theme
   - Save to `data/reports/html/pricing-{company}-{date}.html`
8. Output pricing table

---

## Batch Mode

**Multi-Agent Parallel Implementation** (see `modes/batch.md` for full details)

When `{{mode}}` is `batch`:

1. Read optional tier filter from args (e.g., `batch tier 1` → only Tier 1)
2. Check for `data/batch-queue.md` file with list of companies
3. If file doesn't exist, prompt user to create it
4. **Filter by tier if specified** (e.g., `tier 1` → only ## Tier 1 section)
5. **Create agent team** using TeamCreate
6. **Spawn parallel agents** - one per company (max 5 concurrent)
7. Each agent runs full `analyze` workflow independently
8. Track progress in `data/batch-status.json`
9. Consolidate results from all agents
10. Output batch summary

**Key Feature:** Uses Claude Code multi-agent for ~3x speedup

### Batch Queue Format

Create `data/batch-queue.md`:

```markdown
# Batch Queue

## Tier 1 (Direct Competitors)
- Anthropic
- OpenAI
- Google DeepMind

## Tier 2 (Indirect Competitors)
- Mistral
- Cohere
- Meta AI

## Tier 3 (Emerging)
- Character.AI
- Inflection
```

Or use CSV format in `data/batch-queue.csv`:

```csv
company,tier,priority
Anthropic,1,high
OpenAI,1,high
Mistral,2,medium
```

---

## Report Mode

When `{{mode}}` is `report`:

1. Check for optional `html` flag and filters in args (company, date range)
2. Aggregate all reports in `data/reports/`
3. Generate consolidated report in `data/reports/{date}/consolidated-{date}.md`
4. **If `html` flag is present in args:**
   - Read the consolidated markdown report
   - Use ui-ux-pro-max skill: `/skill ui-ux-pro-max`
   - Generate Chinese HTML with Tailwind dark theme
   - Save to `data/reports/html/index.html`
5. Output path to report (include HTML path if generated)

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

**规范结构：** 所有报告按日期归档到 `data/reports/{date}/` 目录，`latest/` 目录仅存 symlink。

| Output | Location |
|--------|----------|
| 分析报告 | `data/reports/{date}/{company}-{date}.md` |
| 最新报告 symlink | `data/reports/latest/{company}.md` → `../{date}/{company}-{date}.md` |
| 对比报告 | `data/reports/{date}/compare-{A}-vs-{B}-{date}.md` |
| 定价报告 | `data/reports/{date}/pricing-{company}-{date}.md` |
| 综合报告 | `data/reports/{date}/consolidated-{date}.md` |
| HTML 报告 | `data/reports/html/{company}-{date}.html` |
| 快照 (update diff) | `data/snapshots/{company}/{date}.json` |
| 截图 (Playwright) | `data/reports/screenshots/{company}-{date}.png` |

**Snapshots用途:**
- `update` 模式对比新旧报告的分数变化 (≥5% alert)
- `pricing` 模式对比历史定价变化
- 每次analyze/update后自动保存

**Playwright用途:**
- 为 `analyze` / `report` 模式生成竞品官网截图
- 当用户需要可视化证据时调用
- 可选功能，不影响核心分析流程
| Competitor Tracker | `data/competitors.md` |

**Note:** Reports are never overwritten — each run creates a new dated file. Use `update` mode for incremental change tracking.

---

## Next Steps

After routing, execute the selected mode by reading:
- `modes/{mode}.md` for mode-specific instructions
- `modes/_shared.md` for system context
- `modes/_profile.md` for user customizations

## Agent Implementation

For **batch mode**, use multi-agent architecture:

```
/competitive-ops batch tier 1
    ↓
TeamCreate: competitive-batch-{timestamp}
    ↓
Agent analyzer-1 → analyze Anthropic (parallel)
Agent analyzer-2 → analyze OpenAI (parallel)
Agent analyzer-3 → analyze Google DeepMind (parallel)
    ↓
Wait for all agents to complete
    ↓
Consolidate results → output batch summary
```

Each agent executes independently using the `analyze` workflow.
