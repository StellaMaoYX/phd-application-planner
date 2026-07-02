#!/usr/bin/env python3
"""phd-application-planner · build_data.py

Turn the research-workflow output into the two files the marimo dashboard reads:
  _research_data.json   (grouped by school)
  _rows.json            (compact table source)

Usage:
  python3 build_data.py <workflow_result.json> <out_dir>

<workflow_result.json> is the JSON the phd-application-planner-research workflow returned
(save the workflow's `result` to a file first). It looks like:
  { "programs": [ { region, school, program, city, facts:{...}, pis:{pis:[...]}, out:{...} }, ... ] }

_config.json is written separately by the skill (title/subtitle/regions/interest_areas/...).
This script only builds the data the dashboard plots.
"""
import json
import sys


def multi_flag(restr: str) -> str:
    r = (restr or "").lower()
    if any(k in r for k in ["only one", "one program", "1 program", "single program",
                            "cannot apply to more", "may not apply", "one per cycle", "⛔"]):
        return "⛔ 1 only"
    if any(k in r for k in ["can apply", "may apply", "more than one", "multiple", "no restriction",
                            "two programs", "separate application", "both", "✅"]):
        return "✅ multi"
    return restr or ""


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    result = json.load(open(sys.argv[1]))
    out_dir = sys.argv[2].rstrip("/")
    programs = result.get("programs", result if isinstance(result, list) else [])

    research: dict = {}
    rows: list = []
    for p in programs:
        if not p:
            continue
        school = p.get("school") or "Unknown"
        facts = p.get("facts") or {}
        pis = p.get("pis") or {}
        pis_list = pis.get("pis", pis) if isinstance(pis, dict) else (pis or [])
        out = p.get("out") or p.get("outcomes") or {}
        # normalize "not found" sentinels (-1) to None so the dashboard treats them as missing
        for _pi in pis_list:
            for _k in ("hIndex", "citations"):
                if _pi.get(_k) is not None and _pi.get(_k) < 0:
                    _pi[_k] = None
        usd = facts.get("stipendUSD")
        usd = usd if isinstance(usd, (int, float)) and usd >= 0 else None

        research.setdefault(school, []).append({
            "program": p.get("program"),
            "facts": facts,
            "pis": {"pis": pis_list},
            "out": out,
        })
        rows.append({
            "region": p.get("region") or "",
            "school": school,
            "program": p.get("program"),
            "city": p.get("city") or facts.get("city") or "",
            "usd": usd,
            "floor": bool(facts.get("meetsFloor")),
            "fit": facts.get("fitScore"),
            "multi": multi_flag(facts.get("applicationRestrictions")),
            "cohort": facts.get("cohortSize") or "",
        })

    json.dump(research, open(f"{out_dir}/_research_data.json", "w"), ensure_ascii=False, indent=1)
    json.dump(rows, open(f"{out_dir}/_rows.json", "w"), ensure_ascii=False, indent=1)
    n_pi = sum(len((r.get("pis") or {}).get("pis", [])) for recs in research.values() for r in recs)
    print(f"wrote _research_data.json ({len(rows)} programs / {n_pi} PIs) and _rows.json to {out_dir}")


if __name__ == "__main__":
    main()
