"""
Multi-pass scoring management for the multi-axis, multi-horizon analysis.

Manages the scoring workflow:
  --pass <name>     Show status of a specific scoring pass
  --status          Show overall scoring status
  --merge           Merge all 8 score files + compute composites → scores_composite.json

Usage:
    python score_multi.py --status
    python score_multi.py --pass digital_2028
    python score_multi.py --merge
"""

import argparse
import json
import os

PASSES = [
    "digital_2028", "digital_2031", "digital_2036",
    "physical_2028", "physical_2031", "physical_2036",
    "adoption_friction", "demand_elasticity",
]

SCORE_KEYS = {
    "digital_2028": "digital_exposure_2028",
    "digital_2031": "digital_exposure_2031",
    "digital_2036": "digital_exposure_2036",
    "physical_2028": "physical_exposure_2028",
    "physical_2031": "physical_exposure_2031",
    "physical_2036": "physical_exposure_2036",
    "adoption_friction": "adoption_friction",
    "demand_elasticity": "demand_elasticity",
}


def load_occupations():
    with open("occupations.json") as f:
        return json.load(f)


def load_scores(pass_name):
    path = f"scores_{pass_name}.json"
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return {s["slug"]: s for s in json.load(f)}


def composite_score(digital, physical, friction, elasticity):
    """
    Compute composite employment impact score at a given time horizon.
    """
    combined_technical = max(digital, physical) + 0.3 * min(digital, physical)
    adoption_adjusted = combined_technical * (1 - friction / 20)
    employment_impact = adoption_adjusted - (elasticity * 0.3)
    return round(min(10, max(0, employment_impact)), 1)


def merge():
    occupations = load_occupations()
    all_scores = {}
    for p in PASSES:
        scores = load_scores(p)
        key = SCORE_KEYS[p]
        for slug, s in scores.items():
            if slug not in all_scores:
                all_scores[slug] = {"slug": slug, "title": s.get("title", "")}
            all_scores[slug][key] = s.get(key)
            all_scores[slug][f"{key}_rationale"] = s.get("rationale", "")

    # Compute composites for each horizon
    for slug, s in all_scores.items():
        for year in ["2028", "2031", "2036"]:
            d = s.get(f"digital_exposure_{year}")
            p = s.get(f"physical_exposure_{year}")
            f = s.get("adoption_friction")
            e = s.get("demand_elasticity")
            if all(v is not None for v in [d, p, f, e]):
                s[f"composite_{year}"] = composite_score(d, p, f, e)
            else:
                s[f"composite_{year}"] = None

    result = list(all_scores.values())
    with open("scores_composite.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"Wrote scores_composite.json with {len(result)} occupations")

    # Print summary
    for year in ["2028", "2031", "2036"]:
        vals = [s[f"composite_{year}"] for s in result if s.get(f"composite_{year}") is not None]
        if vals:
            avg = sum(vals) / len(vals)
            high = sorted(result, key=lambda s: -(s.get(f"composite_{year}") or 0))[:3]
            low = sorted(result, key=lambda s: (s.get(f"composite_{year}") or 999))[:3]
            print(f"\n--- Composite {year} ---")
            print(f"  Average: {avg:.1f}")
            high_str = ', '.join(s["title"] + " (" + str(s.get("composite_" + year)) + ")" for s in high)
            low_str = ', '.join(s["title"] + " (" + str(s.get("composite_" + year)) + ")" for s in low)
            print(f"  Highest: {high_str}")
            print(f"  Lowest:  {low_str}")


def show_status():
    occupations = load_occupations()
    total = len(occupations)
    print(f"Scoring status ({total} occupations):\n")
    for p in PASSES:
        scores = load_scores(p)
        key = SCORE_KEYS[p]
        scored = sum(1 for s in scores.values() if s.get(key) is not None)
        vals = [s[key] for s in scores.values() if s.get(key) is not None]
        avg = sum(vals) / len(vals) if vals else 0
        bar = "█" * (scored * 30 // total) + "░" * (30 - scored * 30 // total)
        print(f"  {p:25s} [{bar}] {scored:3d}/{total} (avg: {avg:.1f})")


def show_pass(pass_name):
    scores = load_scores(pass_name)
    key = SCORE_KEYS[pass_name]
    print(f"\n{pass_name}: {len(scores)} scored")
    vals = [(s.get("title", s["slug"]), s.get(key)) for s in scores.values() if s.get(key) is not None]
    vals.sort(key=lambda x: -(x[1] or 0))
    print(f"\nTop 5:")
    for title, v in vals[:5]:
        print(f"  {v:4} {title}")
    print(f"\nBottom 5:")
    for title, v in vals[-5:]:
        print(f"  {v:4} {title}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--pass", dest="pass_name")
    parser.add_argument("--merge", action="store_true")
    args = parser.parse_args()

    if args.merge:
        merge()
    elif args.pass_name:
        show_pass(args.pass_name)
    else:
        show_status()


if __name__ == "__main__":
    main()
