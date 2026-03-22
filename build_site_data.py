"""
Build a compact JSON for the website by merging CSV stats with all score data.

Reads:
  - occupations.csv (BLS stats)
  - scores.json (Karpathy's original single-axis scores)
  - scores_composite.json (multi-axis, multi-horizon scores)

Writes site/data.json with all fields the frontend needs.

Usage:
    python build_site_data.py
"""

import csv
import json
import os


def main():
    # Load original AI exposure scores
    with open("scores.json") as f:
        orig_scores = {s["slug"]: s for s in json.load(f)}

    # Load multi-axis composite scores
    composite = {}
    if os.path.exists("scores_composite.json"):
        with open("scores_composite.json") as f:
            composite = {s["slug"]: s for s in json.load(f)}

    # Load CSV stats
    with open("occupations.csv") as f:
        rows = {row["slug"]: row for row in csv.DictReader(f)}

    # Load occupations list for ordering
    with open("occupations.json") as f:
        occupations = json.load(f)

    data = []
    for occ in occupations:
        slug = occ["slug"]
        row = rows.get(slug, {})
        orig = orig_scores.get(slug, {})
        comp = composite.get(slug, {})

        entry = {
            "title": occ["title"],
            "slug": slug,
            "category": row.get("category", occ.get("category", "")),
            "pay": int(row["median_pay_annual"]) if row.get("median_pay_annual") else None,
            "jobs": int(row["num_jobs_2024"]) if row.get("num_jobs_2024") else None,
            "outlook": int(row["outlook_pct"]) if row.get("outlook_pct") else None,
            "outlook_desc": row.get("outlook_desc", ""),
            "education": row.get("entry_education", ""),
            "url": occ.get("url", ""),
            # Original single-axis score
            "exposure": orig.get("exposure"),
            "exposure_rationale": orig.get("rationale", ""),
            # Multi-axis scores
            "digital_2028": comp.get("digital_exposure_2028"),
            "digital_2031": comp.get("digital_exposure_2031"),
            "digital_2036": comp.get("digital_exposure_2036"),
            "physical_2028": comp.get("physical_exposure_2028"),
            "physical_2031": comp.get("physical_exposure_2031"),
            "physical_2036": comp.get("physical_exposure_2036"),
            "adoption_friction": comp.get("adoption_friction"),
            "demand_elasticity": comp.get("demand_elasticity"),
            # Composite scores
            "composite_2028": comp.get("composite_2028"),
            "composite_2031": comp.get("composite_2031"),
            "composite_2036": comp.get("composite_2036"),
            # Rationales
            "digital_2028_rationale": comp.get("digital_exposure_2028_rationale", ""),
            "digital_2031_rationale": comp.get("digital_exposure_2031_rationale", ""),
            "digital_2036_rationale": comp.get("digital_exposure_2036_rationale", ""),
            "physical_2028_rationale": comp.get("physical_exposure_2028_rationale", ""),
            "physical_2031_rationale": comp.get("physical_exposure_2031_rationale", ""),
            "physical_2036_rationale": comp.get("physical_exposure_2036_rationale", ""),
            "friction_rationale": comp.get("adoption_friction_rationale", ""),
            "elasticity_rationale": comp.get("demand_elasticity_rationale", ""),
        }
        data.append(entry)

    os.makedirs("site", exist_ok=True)
    with open("site/data.json", "w") as f:
        json.dump(data, f)

    print(f"Wrote {len(data)} occupations to site/data.json")
    total_jobs = sum(d["jobs"] for d in data if d["jobs"])
    scored = sum(1 for d in data if d.get("composite_2031") is not None)
    print(f"Total jobs: {total_jobs:,}")
    print(f"Occupations with composite scores: {scored}")


if __name__ == "__main__":
    main()
