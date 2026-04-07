# Competitive-Ops v2

AI-powered competitive analysis pipeline for Claude Code.

<p align="center">
  <a href="https://github.com/anthropics/claude-code">
    <img src="https://img.shields.io/badge/Claude_Code-000?style=flat&logo=anthropic&logoColor=white" alt="Claude Code">
  </a>
  <a href="https://github.com/nextlevelbuilder/ui-ux-pro-max-skill">
    <img src="https://img.shields.io/badge/Design_System-ui--ux--pro--max-blue?style=flat" alt="UI UX Pro Max">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  </a>
</p>

---

## What Is This

Competitive-Ops turns Claude Code into a **competitive intelligence command center**. Instead of manually researching competitors, you get an AI-powered pipeline that:

- **Analyzes competitors** with structured SWOT + scoring (10 dimensions)
- **Generates professional reports** in Markdown + HTML + PDF
- **Tracks changes** with alerts for pricing and feature updates
- **Compares multiple competitors** side-by-side
- **Processes in batch** — analyze 10+ competitors in parallel

---

## Quick Start

### 1. Install

```bash
# Clone the repo
git clone https://github.com/YOUR_ORG/competitive-opsetitive-ops-v2.git
cd competitive-ops-v2

# Install Python dependencies
pip install -r requirements.txt

# Configure (copy and edit)
cp config/profile.yml config/profile.yml  # Your company info
```

### 2. Configure API Keys (Optional)

```bash
# Add to your environment or .env file
export TAVILY_API_KEY="tvly-xxxxx"
```

Get a Tavily API key at [tavily.com](https://tavily.com).
Or use Tavily MCP server if configured in Claude Code.

### 3. Use in Claude Code

```bash
claude

# Add a competitor
/competitive-ops add Anthropic

# Full analysis with HTML report
/competitive-ops analyze Anthropic

# Compare two competitors
/competitive-ops compare Anthropic vs OpenAI

# Check pricing changes
/competitive-ops pricing Anthropic

# View all tracked competitors
/competitive-ops track
```

---

## Features

### Skill Modes

| Command | Description |
|---------|-------------|
| `/competitive-ops add <company>` | Add a competitor to tracking |
| `/competitive-ops analyze <company>` | Full analysis: SWOT + scoring + HTML report |
| `/competitive-ops compare <A> vs <B>` | Side-by-side feature matrix |
| `/competitive-ops update <company>` | Check for changes since last analysis |
| `/competitive-ops pricing <company>` | Pricing research with change detection |
| `/competitive-ops batch` | Batch process multiple competitors |
| `/competitive-ops report` | Generate consolidated report |
| `/competitive-ops track` | View tracking dashboard |

### Scoring System

Evaluate competitors across 6 dimensions (1-5 scale):

| Dimension | Weight |
|-----------|--------|
| Product Maturity | 20% |
| Feature Coverage | 20% |
| Pricing | 15% |
| Market Presence | 15% |
| Growth Trajectory | 10% |
| Brand Strength | 10% |

### Archetype Detection

Classify competitors into types:

- **Direct Competitor** — Same product, same market
- **Indirect Competitor** — Different approach, same need
- **Emerging Threat** — New technology, new model
- **Replacement Threat** — Alternative solution
- **Adjacent Player** — Overlapping users
- **Reference Model** — Industry benchmark

### Confidence Scoring

Data is cross-validated from multiple sources:

| Level | Condition |
|-------|-----------|
| 🟢 High | 3+ sources agree |
| 🟡 Medium | 2 sources agree |
| 🔴 Low | Conflicting or insufficient data |

---

## Project Structure

```
competitive-ops-v2/
├── CLAUDE.md                    # Agent instructions
├── cv.md                       # Your product definition
├── config/                     # Configuration files
│   ├── profile.yml            # Company/product config
│   ├── sources.yml            # Trusted data sources
│   ├── pricing-alerts.yml     # Pricing monitoring
│   └── change-detection.yml    # Change thresholds
├── modes/                      # 10 Skill modes
│   ├── _shared.md             # Shared context
│   ├── _profile.md            # User customization
│   └── *.md                   # Individual modes
├── scripts/                    # Python utilities
│   ├── cross_validate.py      # Multi-source validation
│   └── change_detector.py      # Change tracking
├── templates/
│   └── report/
│       └── html/              # HTML templates
└── data/
    └── competitors.md          # Competitor tracker
```

---

## Output Examples

### Markdown Report

```markdown
# Competitor Analysis: Anthropic

**Score: 4.2/5** | **Confidence: High** | **Updated: 2026-04-07**

## SWOT Analysis

### Strengths
- Strong AI research background
- Claude model performance
- Safety-first positioning

### Weaknesses
- Limited enterprise features
- Newer to market
- Smaller team

...
```

### HTML Report

Professional, responsive HTML reports with:
- Executive summary cards
- SWOT visualization (4-quadrant grid)
- Feature comparison matrix
- Pricing tier cards
- Confidence indicators

---

## Design System

Reports use the **ui-ux-pro-max** design system for professional styling:

- **67 UI Styles** — Minimalism, Swiss Style, Glassmorphism, etc.
- **161 Color Palettes** — Industry-specific palettes
- **57 Font Pairings** — Google Fonts combinations
- **25 Chart Types** — Data visualization recommendations

---

## Data Privacy

- **Local-first**: All data stored in your project directory
- **No external APIs** without your consent (Tavily is opt-in)
- **User layer**: Your CV, profile, and tracker are never shared
- **System layer**: Skill modes can be updated without overwriting your config

---

## Contributing

1. Fork the repo
2. Create a feature branch
3. Make changes
4. Submit a PR

---

## License

MIT — free to use, modify, and distribute.

---

## Related

- [Career-Ops](https://github.com/santifer/career-ops) — Job search pipeline (this project's inspiration)
- [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — Design system for AI agents
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — AI coding assistant
