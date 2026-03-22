# US Job Market Visualizer — Multi-Axis AI Exposure

> Fork of [karpathy/jobs](https://github.com/karpathy/jobs) with multi-axis, multi-horizon AI exposure scoring.

## What's new in this fork

Karpathy's original analysis uses a single axis ("Digital AI Exposure") with no timeframe and treats physical jobs as permanently insulated. This fork introduces:

- **4 scoring axes**: digital AI exposure, physical/embodied AI exposure, adoption friction, demand elasticity
- **3 time horizons**: 2028, 2031, 2036
- **A timeline slider** on the frontend so you can watch the treemap shift over time
- **A composite "employment impact" score** at each horizon

## Scoring axes

| Axis | Scale | What it measures |
|------|-------|-----------------|
| Digital AI Exposure | 0–10 | How much digital AI (LLMs, coding agents, analysis tools) can automate the occupation's core tasks |
| Physical AI Exposure | 0–10 | How much embodied AI (humanoid robots, autonomous vehicles, surgical robots) can automate physical tasks |
| Adoption Friction | 0–10 | Real-world barriers that slow adoption even where technology is capable (regulation, liability, employer fragmentation, social trust) |
| Demand Elasticity | -5 to +5 | Whether productivity gains increase demand (positive) or reduce headcount (negative) |

## Composite formula

Applied independently at each time horizon:

```python
def composite_score(digital, physical, friction, elasticity):
    combined_technical = max(digital, physical) + 0.3 * min(digital, physical)
    adoption_adjusted = combined_technical * (1 - friction / 20)
    employment_impact = adoption_adjusted - (elasticity * 0.3)
    return round(min(10, max(0, employment_impact)), 1)
```

**Worked examples:**

| Occupation | Digital | Physical | Friction | Elasticity | Composite | Why |
|-----------|---------|----------|----------|-----------|-----------|-----|
| Software developer (2031) | 8 | 0 | 2 | +3 | 6.3 | High digital exposure but strong latent demand softens impact |
| Delivery truck driver (2036) | 2 | 8 | 4 | -2 | 7.5 | Physical automation + fixed demand = significant headcount impact |
| Registered nurse (2031) | 4 | 3 | 7 | +1 | 2.9 | Moderate exposure but massive friction + slight demand growth = low impact |

## Key findings

**The "physical moat" dissolves over time.** Occupations scoring 0–2 in Karpathy's analysis (warehouse, manufacturing, trucking) show rising composite scores by 2036 as robotics matures.

**Demand elasticity reshapes the story.** Software developers score high on technical exposure but their composite drops due to positive elasticity (+3). Data entry clerks score high on both exposure AND negative elasticity — worst of both worlds.

**Friction creates temporal bifurcation.** A warehouse worker (friction=1) and a surgical nurse (friction=8) with identical technical exposure show radically different composite curves.

**45 "genuinely durable" occupations** score < 3 composite across all horizons — concentrated in hands-on care, emergency response, and skilled trades in variable environments.

## How to run

```bash
# Clone
git clone https://github.com/jakzilla/jobs.git
cd jobs

# Install dependencies
pip install beautifulsoup4

# Generate markdown from HTML (if pages/ doesn't exist)
python process.py

# View scoring status
python score_multi.py --status

# Merge scores and compute composites
python score_multi.py --merge

# Build site data
python build_site_data.py

# Generate analysis report
python analyse.py

# Serve locally
cd site && python -m http.server 8000
# Open http://localhost:8000
```

## File structure

```
prompts/                    # 8 scoring prompts (one per axis x horizon)
scores_digital_2028.json    # Raw scores for each pass
scores_digital_2031.json
scores_digital_2036.json
scores_physical_2028.json
scores_physical_2031.json
scores_physical_2036.json
scores_adoption_friction.json
scores_demand_elasticity.json
scores_composite.json       # Merged scores with computed composites
score_multi.py              # Scoring workflow management
build_site_data.py          # Merges scores + BLS data -> site/data.json
analyse.py                  # Generates analysis_report.md
analysis_report.md          # Comprehensive analysis output
site/index.html             # Frontend with timeline slider
site/data.json              # Compact data for the treemap
```

## Methodology limitations

- Scoring is done by an LLM evaluating BLS job descriptions — pattern-matching, not labour economics
- Time-horizon contexts are informed projections, not predictions
- The composite formula weights are somewhat arbitrary
- Demand elasticity is the hardest axis to score accurately
- No geographic variation
- No consideration of new occupations that don't yet exist
