# PhD Application Planner

A [Claude Code](https://claude.com/claude-code) **skill** that turns a short conversation into
a researched, interactive **[marimo](https://marimo.io) dashboard** for planning your PhD
applications — find programs, surface fitting advisors (PIs), compare stipends and application
rules, and decide where to apply.

It works for **any field, any region**. You tell it what you care about; it researches in
parallel and hands you a dashboard you can filter, annotate, and rank.

> No personal data is baked in. Every run is driven entirely by your own intake answers.

---

## What you get

A single-page marimo app with:

- **KPIs** and a **⭐ top-fit picks** grid
- **🔎 Program browser** — filter by region / fit / stipend / application-hedge; aligned table
  rows; click **✕** on any row to hide it (and restore later)
- **🏫 Program detail cards** — stipend (with verification basis), cohort, deadlines,
  application restrictions, career outcomes, international-student notes
- **🔬 PI browser** — filter by category / wet-dry / region / min-h-index / keyword; per-row
  **✕** hide; **editable notes per advisor that persist across restarts**; Google Scholar links
- **🎯 Weighted priority ranker** — 5 sliders + interest picks, live re-ranking
- **💰 Cost-of-living-adjusted "real" stipend** chart
- **📊 Statistics** — Spearman correlation, Kruskal–Wallis, Pareto frontier, K-means
  clustering + PCA — with plain-language, stats-based recommendations

Your notes and hidden lists are saved next to the data, so they survive restarts.

---

## Requirements

- **[Claude Code](https://claude.com/claude-code)** (the skill runs inside it)
- **Python 3.9+** with:
  ```bash
  pip install marimo pandas matplotlib scipy scikit-learn
  ```
- Web access for the research step (Claude Code's built-in web tools)

---

## Install

Clone into your Claude Code skills directory:

```bash
git clone https://github.com/SihengTao/phd-application-planner \
  ~/.claude/skills/phd-application-planner
```

That's it — Claude Code auto-discovers skills in `~/.claude/skills/`.

---

## Usage (tutorial)

Just ask Claude Code, in any project:

> "Help me find PhD programs in *<your field>* and build me a dashboard."

or invoke it explicitly with `/phd-application-planner`.

### The 5 steps it runs

1. **Interactive intake.** It asks what you care about — research field & subfields, target
   regions/countries, minimum stipend (your hard floor) + currency, how many programs and how
   many advisors per program, your PI preferences (rising-star vs established, small/young vs
   large labs, wet/dry balance, methods), and any application constraints (e.g. can you apply
   to multiple programs at one school). ~3–5 quick questions.

2. **Config.** It writes a `_config.json` with your branding, regions, stipend floor, and an
   auto-generated interest-tag taxonomy for your field.

3. **Parallel research.** It runs a multi-agent workflow that, for each program, gathers
   **facts ‖ fitting PIs ‖ career outcomes** in parallel, then adversarially double-checks
   stipends and application rules. (Stipends and PIs are verified against official pages and
   Google Scholar — never fabricated; "not found" stays honest.)

4. **Build data.** It assembles the results into the dashboard's data files.

5. **Launch.** It copies the marimo app next to the data and starts it (detached, persistent),
   opening it in your browser.

### After it launches

- Browse programs and advisors; **✕** the ones you're not interested in.
- Write notes on each advisor as you meet/read about them — they persist.
- Use the priority ranker sliders to weight fit / stipend / city / advisor-density / topics.
- Read the statistics section for data-driven strategy tips.

Re-running the research refreshes the program/PI data but **keeps your notes and hidden lists**.

---

## Repository layout

```
phd-application-planner/
├── SKILL.md                    # how Claude runs the pipeline
├── assets/
│   ├── dashboard_template.py   # the marimo app (all features; config-driven)
│   ├── research_workflow.js    # parallel research workflow
│   ├── build_data.py           # research output → dashboard data files
│   └── launch.py               # detached marimo launcher
├── reference/
│   ├── intake.md               # the intake question bank
│   ├── schema.md               # data schema
│   └── honesty.md              # verification / no-fabrication rules
├── README.md
└── LICENSE
```

### Configuration notes

- **Regions are arbitrary** — US, EU, UK, Canada, Singapore, China, etc. Each gets a color and
  short label in `_config.json`; the whole dashboard (including the stats charts) adapts.
- **Seed programs** — if you already have a target list, it's passed straight into the research
  step instead of auto-discovery.
- **Language** — the dashboard UI labels ship in Chinese; translate the strings in
  `dashboard_template.py` if you prefer another language. All titles/subtitles are configurable
  per run via `_config.json`.

---

## A note on accuracy

Stipends, deadlines, cohort sizes, application rules, and h-indexes are **web-research
snapshots**. They can be wrong or out of date. Always confirm the numbers that matter on the
program's official pages before deciding. See `reference/honesty.md` for the verification rules
the skill follows.

---

## License

[MIT](LICENSE) — powered by [marimo](https://marimo.io).
