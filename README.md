# US Job Market Visualizer — Multi-Axis AI Exposure

> Fork of [karpathy/jobs](https://github.com/karpathy/jobs) extending Karpathy's single-axis model into a multi-dimensional, time-varying analysis.

**Live site:** [site-lp6a3lriq-just-for-fun.vercel.app](https://site-lp6a3lriq-just-for-fun.vercel.app)

## Why this fork exists

Karpathy's original project (published March 14, 2026) scores 342 US occupations on a single "AI exposure" axis. His model has an explicit design assumption: physical work is a barrier to AI. Roofers score 0, janitors score 1, construction laborers score 0. In his framework, these occupations are effectively safe.

But the model doesn't score low for physical jobs because it assessed the physical AI threat and found it small — it scores low because **physical AI is entirely absent from the model**. There is no robotics axis. The only question asked is "how much of this work is digital?"

This fork adds the robotics question, splits digital and physical exposure into separate axes, adds adoption friction and demand elasticity modifiers, and projects everything across three time horizons.

## What changed

| Feature | Karpathy original | This fork |
|---------|-------------------|-----------|
| Scoring axes | 1 (AI exposure) | 4 (digital AI, physical AI, adoption friction, demand elasticity) |
| Time horizons | None (single snapshot) | 3 (2028, 2031, 2036) |
| Physical AI | Absent (physical work = shield) | Separate axis with smartphone adoption curve calibration |
| Demand effects | Not considered | Elasticity score (-5 to +5) |
| Adoption barriers | Not considered | Friction score (0-10) |
| Global impact | Not considered | Dedicated analysis page |
| Total individual scores | 342 | 2,736 |

## Scoring axes

| Axis | Scale | What it measures |
|------|-------|-----------------|
| Digital AI Exposure | 0-10 | How much digital AI (LLMs, coding agents, analysis tools) can automate the occupation's core tasks |
| Physical AI Exposure | 0-10 | How much embodied AI (humanoid robots, autonomous vehicles, automated systems) can automate physical tasks |
| Adoption Friction | 0-10 | Real-world barriers that slow adoption: regulation, liability, employer fragmentation, social trust, unions |
| Demand Elasticity | -5 to +5 | Whether AI-driven productivity gains expand demand (positive) or just reduce headcount (negative) |

## Physical AI calibration

The physical AI scores use the smartphone adoption curve as an analogy:
- **2028** = iPhone 1 era: early adopters, structured environments, expensive units
- **2031** = iPhone 4/5 era: growing but limited to specific use cases
- **2036** = iPhone X era: millions of units at commodity pricing, deployed across many industries

Tesla went from a person in a robot costume (2022) to converting Fremont production lines to manufacture Optimus (2026) in under four years. Embodied AI training happens increasingly in simulation (Google Genie, NVIDIA Isaac), meaning the intelligence scales exponentially even while manufacturing scales with production lines.

## Key findings (March 2026)

**Digital AI hits first and hardest.** By 2028, 27 occupations covering 18.5M jobs score composite 7+. These are almost exclusively clerical and administrative roles. By 2031, this expands to 46 occupations (35M jobs) as professional knowledge work enters the blast zone.

**Physical AI accelerates through the 2030s.** The physical AI average rises from 1.0 (2028) to 3.0 (2036). Warehouse workers, truck drivers, agricultural labourers, janitors, and cashiers all reach scores of 7-9 by 2036 as humanoid robots reach commodity pricing.

**Both waves converge by 2036.** The composite average rises from 3.7 (2028) to 5.7 (2036). By 2036, occupations face simultaneous disruption from digital AI (automating their knowledge work) and physical AI (automating their manual tasks).

**Demand elasticity is the single most important variable** separating "AI transforms the job" from "AI eliminates the job." Software development and tutoring have high elasticity (+3 to +5) — when the work gets cheaper, demand explodes. Data entry and insurance claims processing have negative elasticity — demand is fixed, so productivity gains directly reduce headcount.

## How it was built

The human behind this fork has zero coding experience. The entire project was built in a single Claude Code session through natural language direction. The human's contribution was direction, criticism, judgment, and taste. All implementation was done by AI agents:

- 8 parallel scoring agents produced 2,736 individual scores
- Research agents gathered adoption data from McKinsey, Gartner, Stack Overflow, and BPO industry sources
- Frontend agents built the interactive treemap, stats dashboard, and analysis panels
- Multiple rounds of rescoring when calibration issues were identified

## File structure

```
prompts/                         # 8 scoring prompts
scores_digital_2028.json         # Raw scores per pass
scores_digital_2031.json
scores_digital_2036.json
scores_physical_2028.json
scores_physical_2031.json
scores_physical_2036.json
scores_adoption_friction.json
scores_demand_elasticity.json
site/
  index.html                     # Context page
  treemap.html                   # Interactive treemap with analysis
  global.html                    # Global impact analysis
  data.json                      # All scores merged for frontend
```

## Run locally

```bash
cd site && python3 -m http.server 8000
# Open http://localhost:8000
```

## Limitations

- Scores are LLM-generated analytical estimates, not empirical measurements
- The composite formula is one reasonable approach among many
- Adoption timeline calibration uses real 2026 data but extrapolation to 2036 is inherently uncertain
- The global impact page covers only the US-outsourcing channel
- No geographic variation within the US
- No consideration of new occupations that don't yet exist
- Different analysts — human or AI — would make different judgment calls
