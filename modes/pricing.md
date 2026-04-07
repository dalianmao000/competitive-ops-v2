# Mode: pricing -- Pricing Research

Research and track competitor pricing.

## Usage

```
/comp pricing <company-name>
```

## Process

### 1. Input
- Company name (normalized)

### 2. Collect Pricing Data

#### Sources
- [ ] **TODO: Playwright Integration**
  ```javascript
  await Playwright.browser_navigate(pricingPage)
  await Playwright.browser_snapshot()
  ```
- WebSearch for:
  - Official pricing pages
  - Third-party reviews mentioning pricing
  - Comparison sites
  - Reddit/forum mentions

#### Pricing Elements to Capture
- **Plans:** Names, tiers, limits
- **Per-user pricing:** Monthly/annual
- **Enterprise pricing:** Custom/contact sales
- **Free tier:** Available/limits
- **Trial:** Duration, limitations
- **Add-ons:** Prices, bundles
- **Contract terms:** Annual, monthly, usage-based

### 3. Pricing Detection

#### Change Detection
Compare against `data/pricing-snapshots/{company-slug}.md`:

| Element | Previous | Current | Change |
|---------|----------|---------|--------|
| Basic plan | $X/mo | $Y/mo | ±Z% |
| Pro plan | $X/mo | $Y/mo | ±Z% |
| Enterprise | Custom | Custom | - |

#### Alert Thresholds
- **Any pricing change:** Always alert
- **New tier added:** Always alert
- **Free tier change:** Always alert

### 4. Output

#### Pricing Table

```markdown
# Pricing: [Company]

**Researched:** YYYY-MM-DD
**Source:** [URL]

## Current Pricing

| Plan | Price | Users | Key Features |
|------|-------|-------|--------------|
| Free | $0 | 1 | [Features] |
| Basic | $X/mo | up to Y | [Features] |
| Pro | $X/mo | up to Y | [Features] |
| Enterprise | Custom | Unlimited | [Features] |

## Pricing Comparison (vs Market)

| Metric | [Company] | Market Avg |
|--------|-----------|------------|
| Entry price | $X | $X |
| Pro price | $X | $X |
| Value score | X/5 | X/5 |

## Changes Since Last Snapshot

### [Date]
- [Change 1]
- [Change 2]

## Confidence

- **Data freshness:** [date]
- **Source reliability:** [High/Medium/Low]
- **Coverage:** [Complete/Partial/Estimate]
```

### 5. Save Results
- Save snapshot to `data/pricing-snapshots/{company-slug}.md`
- Update `data/profiles/{company-slug}/profile.md` with latest pricing
- Add changelog entry if changed

## Example

```
/comp pricing Anthropic
/comp pricing "OpenAI"
```

## Pricing Snapshot Format

```markdown
# [Company] Pricing Snapshot

**Captured:** YYYY-MM-DD
**Source:** [URL]

## Plans

| Plan | Price | Period | Users | Features |
|------|-------|--------|-------|----------|
| ... | ... | ... | ... | ... |

## Notes

[Any additional context]
```

## TODO Checklist

- [ ] Implement Playwright for dynamic pricing page scraping
- [ ] Add pricing extraction from pricing pages
- [ ] Track pricing history over time
- [ ] Generate pricing alerts
- [ ] Add value scoring algorithm

## Common Pricing Patterns

| Pattern | Detection | Action |
|---------|-----------|--------|
| Freemium | Free tier exists | Flag as competitive |
| Per-seat | Per-user pricing | Calculate market rate |
| Usage-based | Meters, tokens | Note as emerging |
| Enterprise | Contact sales | Flag for discovery |
| Bundle | Multiple products | Note cross-sell |
