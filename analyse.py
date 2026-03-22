"""
Generate comprehensive analysis from multi-axis scoring data.

Reads scores_composite.json and occupations.csv, outputs analysis_report.md.

Usage:
    python analyse.py
"""

import csv
import json


def fmt_pay(pay):
    if pay is None:
        return "?"
    return f"${pay:,}"


def fmt_jobs(jobs):
    if jobs is None:
        return "?"
    if jobs >= 1_000_000:
        return f"{jobs / 1e6:.1f}M"
    if jobs >= 1_000:
        return f"{jobs / 1e3:.0f}K"
    return str(jobs)


def main():
    with open("scores_composite.json") as f:
        scores = {s["slug"]: s for s in json.load(f)}

    with open("occupations.csv") as f:
        csv_rows = {row["slug"]: row for row in csv.DictReader(f)}

    # Also load original Karpathy scores
    with open("scores.json") as f:
        orig_scores = {s["slug"]: s for s in json.load(f)}

    # Merge
    records = []
    for slug, s in scores.items():
        row = csv_rows.get(slug, {})
        orig = orig_scores.get(slug, {})
        pay = int(row["median_pay_annual"]) if row.get("median_pay_annual") else None
        jobs = int(row["num_jobs_2024"]) if row.get("num_jobs_2024") else None
        records.append({
            "slug": slug,
            "title": s.get("title", slug),
            "pay": pay,
            "jobs": jobs,
            "education": row.get("entry_education", ""),
            "outlook_pct": int(row["outlook_pct"]) if row.get("outlook_pct") else None,
            "original_exposure": orig.get("exposure"),
            **{k: s.get(k) for k in [
                "digital_exposure_2028", "digital_exposure_2031", "digital_exposure_2036",
                "physical_exposure_2028", "physical_exposure_2031", "physical_exposure_2036",
                "adoption_friction", "demand_elasticity",
                "composite_2028", "composite_2031", "composite_2036",
            ]},
        })

    lines = []
    lines.append("# Multi-Axis AI Exposure Analysis Report")
    lines.append("")
    lines.append(f"**{len(records)} occupations scored across 4 axes and 3 time horizons.**")
    lines.append("")

    total_jobs = sum(r["jobs"] or 0 for r in records)
    total_wages = sum((r["jobs"] or 0) * (r["pay"] or 0) for r in records)

    # Per-horizon analysis
    for year in ["2028", "2031", "2036"]:
        key = f"composite_{year}"
        scored = [r for r in records if r.get(key) is not None]
        if not scored:
            continue

        lines.append(f"## Horizon: {year}")
        lines.append("")

        vals = [r[key] for r in scored]
        avg = sum(vals) / len(vals)

        # Weighted average
        w_sum = sum(r[key] * (r["jobs"] or 0) for r in scored if r["jobs"])
        w_count = sum(r["jobs"] or 0 for r in scored if r["jobs"])
        w_avg = w_sum / w_count if w_count else 0

        lines.append(f"- **Unweighted average composite:** {avg:.1f}")
        lines.append(f"- **Job-weighted average composite:** {w_avg:.1f}")

        # High exposure (7+)
        high = [r for r in scored if r[key] >= 7]
        high_jobs = sum(r["jobs"] or 0 for r in high)
        high_wages = sum((r["jobs"] or 0) * (r["pay"] or 0) for r in high)
        lines.append(f"- **Jobs scoring 7+:** {len(high)} occupations, {fmt_jobs(high_jobs)} jobs ({high_jobs / total_jobs * 100:.1f}% of total)")
        lines.append(f"- **Wages in 7+ tier:** ${high_wages / 1e12:.2f}T")
        lines.append("")

        # By salary band
        lines.append(f"### Composite {year} by salary band")
        lines.append("")
        lines.append("| Salary Band | Avg Composite | Jobs | % of Band Scoring 7+ |")
        lines.append("|-------------|--------------|------|---------------------|")
        bands = [("<$35K", 0, 35000), ("$35-75K", 35000, 75000), ("$75-100K", 75000, 100000), ("$100K+", 100000, float("inf"))]
        for name, lo, hi in bands:
            group = [r for r in scored if r["pay"] and lo <= r["pay"] < hi]
            if group:
                gavg = sum(r[key] for r in group) / len(group)
                gjobs = sum(r["jobs"] or 0 for r in group)
                ghigh = sum(1 for r in group if r[key] >= 7)
                lines.append(f"| {name} | {gavg:.1f} | {fmt_jobs(gjobs)} | {ghigh}/{len(group)} ({ghigh / len(group) * 100:.0f}%) |")
        lines.append("")

        # Top 10 highest composite
        top = sorted(scored, key=lambda r: -r[key])[:10]
        lines.append(f"### Top 10 highest composite {year}")
        lines.append("")
        lines.append("| Occupation | Composite | Digital | Physical | Friction | Elasticity | Pay |")
        lines.append("|-----------|-----------|---------|----------|----------|-----------|-----|")
        for r in top:
            d = r.get(f"digital_exposure_{year}", "?")
            p = r.get(f"physical_exposure_{year}", "?")
            f_val = r.get("adoption_friction", "?")
            e = r.get("demand_elasticity", "?")
            lines.append(f"| {r['title']} | {r[key]:.1f} | {d} | {p} | {f_val} | {e} | {fmt_pay(r['pay'])} |")
        lines.append("")

        # Bottom 10
        bottom = sorted(scored, key=lambda r: r[key])[:10]
        lines.append(f"### Top 10 lowest composite {year} (most durable)")
        lines.append("")
        lines.append("| Occupation | Composite | Digital | Physical | Friction | Elasticity | Pay |")
        lines.append("|-----------|-----------|---------|----------|----------|-----------|-----|")
        for r in bottom:
            d = r.get(f"digital_exposure_{year}", "?")
            p = r.get(f"physical_exposure_{year}", "?")
            f_val = r.get("adoption_friction", "?")
            e = r.get("demand_elasticity", "?")
            lines.append(f"| {r['title']} | {r[key]:.1f} | {d} | {p} | {f_val} | {e} | {fmt_pay(r['pay'])} |")
        lines.append("")

    # Cross-horizon analysis
    lines.append("## Cross-Horizon Analysis")
    lines.append("")

    # Delayed cliff: composite < 3 in 2028 but > 7 by 2036
    delayed = [r for r in records
               if r.get("composite_2028") is not None and r.get("composite_2036") is not None
               and r["composite_2028"] < 3 and r["composite_2036"] > 7]
    delayed.sort(key=lambda r: r["composite_2036"] - r["composite_2028"], reverse=True)
    lines.append(f"### \"Delayed Cliff\" occupations ({len(delayed)} found)")
    lines.append("*Composite < 3 in 2028 but > 7 by 2036 — jobs that look safe today but face a reckoning.*")
    lines.append("")
    if delayed:
        lines.append("| Occupation | 2028 | 2031 | 2036 | Jobs | Pay |")
        lines.append("|-----------|------|------|------|------|-----|")
        for r in delayed[:20]:
            lines.append(f"| {r['title']} | {r['composite_2028']:.1f} | {r.get('composite_2031', '?')} | {r['composite_2036']:.1f} | {fmt_jobs(r['jobs'])} | {fmt_pay(r['pay'])} |")
    lines.append("")

    # Imminent disruption: composite > 7 already in 2028
    imminent = [r for r in records if r.get("composite_2028") is not None and r["composite_2028"] > 7]
    imminent.sort(key=lambda r: -r["composite_2028"])
    lines.append(f"### \"Imminent Disruption\" occupations ({len(imminent)} found)")
    lines.append("*Composite > 7 in 2028 — already facing significant impact.*")
    lines.append("")
    if imminent:
        lines.append("| Occupation | 2028 | 2031 | 2036 | Jobs | Pay |")
        lines.append("|-----------|------|------|------|------|-----|")
        for r in imminent[:20]:
            lines.append(f"| {r['title']} | {r['composite_2028']:.1f} | {r.get('composite_2031', '?')} | {r.get('composite_2036', '?')} | {fmt_jobs(r['jobs'])} | {fmt_pay(r['pay'])} |")
    lines.append("")

    # Genuinely durable: composite < 3 across ALL horizons
    durable = [r for r in records
               if all(r.get(f"composite_{y}") is not None and r[f"composite_{y}"] < 3 for y in ["2028", "2031", "2036"])]
    durable.sort(key=lambda r: r["composite_2036"])
    lines.append(f"### \"Genuinely Durable\" occupations ({len(durable)} found)")
    lines.append("*Composite < 3 across all horizons — resistant to both digital and physical AI.*")
    lines.append("")
    if durable:
        lines.append("| Occupation | 2028 | 2031 | 2036 | Jobs | Pay |")
        lines.append("|-----------|------|------|------|------|-----|")
        for r in durable[:20]:
            lines.append(f"| {r['title']} | {r['composite_2028']:.1f} | {r['composite_2031']:.1f} | {r['composite_2036']:.1f} | {fmt_jobs(r['jobs'])} | {fmt_pay(r['pay'])} |")
    lines.append("")

    # Axis-specific analysis
    lines.append("## Axis-Specific Analysis")
    lines.append("")

    # Physical exposure surprises: high physical_2036 but low original Karpathy score
    phys_surprises = [r for r in records
                      if r.get("physical_exposure_2036") is not None
                      and r.get("original_exposure") is not None
                      and r["original_exposure"] <= 3
                      and r["physical_exposure_2036"] >= 5]
    phys_surprises.sort(key=lambda r: -r["physical_exposure_2036"])
    lines.append(f"### Physical exposure surprises ({len(phys_surprises)} found)")
    lines.append("*High physical_exposure_2036 (>=5) where Karpathy's original digital score was <=3 — the ones his analysis missed.*")
    lines.append("")
    if phys_surprises:
        lines.append("| Occupation | Physical 2036 | Karpathy Original | Jobs | Pay |")
        lines.append("|-----------|--------------|-------------------|------|-----|")
        for r in phys_surprises[:20]:
            lines.append(f"| {r['title']} | {r['physical_exposure_2036']} | {r['original_exposure']} | {fmt_jobs(r['jobs'])} | {fmt_pay(r['pay'])} |")
    lines.append("")

    # Feasibility-adoption gap: friction > 7 but max(digital, physical) > 7
    gap = [r for r in records
           if r.get("adoption_friction") is not None
           and r["adoption_friction"] > 7
           and any(r.get(f"digital_exposure_{y}", 0) > 7 or r.get(f"physical_exposure_{y}", 0) > 7 for y in ["2028", "2031", "2036"])]
    gap.sort(key=lambda r: -r.get("adoption_friction", 0))
    lines.append(f"### Biggest feasibility-adoption gap ({len(gap)} found)")
    lines.append("*Friction > 7 but technical exposure > 7 — technology is ready but adoption is blocked.*")
    lines.append("")
    if gap:
        lines.append("| Occupation | Friction | Max Digital | Max Physical | Jobs |")
        lines.append("|-----------|----------|------------|-------------|------|")
        for r in gap[:20]:
            max_d = max(r.get(f"digital_exposure_{y}", 0) or 0 for y in ["2028", "2031", "2036"])
            max_p = max(r.get(f"physical_exposure_{y}", 0) or 0 for y in ["2028", "2031", "2036"])
            lines.append(f"| {r['title']} | {r['adoption_friction']} | {max_d} | {max_p} | {fmt_jobs(r['jobs'])} |")
    lines.append("")

    # Demand expansion: elasticity > +3
    expanding = [r for r in records if r.get("demand_elasticity") is not None and r["demand_elasticity"] >= 3]
    expanding.sort(key=lambda r: -r["demand_elasticity"])
    lines.append(f"### Demand expansion occupations ({len(expanding)} found)")
    lines.append("*Demand elasticity >= +3 — AI makes the pie bigger, partially offsetting automation.*")
    lines.append("")
    if expanding:
        lines.append("| Occupation | Elasticity | Composite 2031 | Jobs | Pay |")
        lines.append("|-----------|-----------|---------------|------|-----|")
        for r in expanding[:20]:
            c31 = r.get("composite_2031")
            lines.append(f"| {r['title']} | +{r['demand_elasticity']} | {c31 if c31 is not None else '?'} | {fmt_jobs(r['jobs'])} | {fmt_pay(r['pay'])} |")
    lines.append("")

    text = "\n".join(lines)
    with open("analysis_report.md", "w") as f:
        f.write(text)

    print(f"Wrote analysis_report.md ({len(text):,} chars)")
    print(f"\nSummary:")
    print(f"  Total occupations: {len(records)}")
    print(f"  Total jobs: {fmt_jobs(total_jobs)}")
    print(f"  Delayed cliff occupations: {len(delayed)}")
    print(f"  Imminent disruption occupations: {len(imminent)}")
    print(f"  Genuinely durable occupations: {len(durable)}")
    print(f"  Physical exposure surprises: {len(phys_surprises)}")
    print(f"  Demand expansion occupations: {len(expanding)}")


if __name__ == "__main__":
    main()
