# Data schema (what the dashboard reads)

The research step first writes `_wf_result.json`; `assets/build_data.py` converts it into the
files the marimo app reads.

## `_wf_result.json` — research workflow output
```json
{
  "field": "Human-Computer Interaction",
  "regions": [{"key": "US", "label": "United States"}],
  "floor": 35000,
  "currency": "USD",
  "programs": [
    {
      "region": "US",
      "school": "Example University",
      "program": "Example PhD Program",
      "city": "Example City",
      "facts": { "...": "FACTS fields below" },
      "pis": { "pis": [{ "...": "PI fields below" }] },
      "out": { "...": "OUTCOMES fields below" }
    }
  ]
}
```

Codex or other hosts without a Workflow tool may write this file directly after equivalent
web research. Claude Code may produce the same object by running `assets/research_workflow.js`.

## Dashboard input files

The marimo app (`dashboard_template.py`) reads three files from its own folder.

## `_research_data.json` — grouped by school
```json
{
  "<School Name>": [
    {
      "program": "Human-Computer Interaction PhD",
      "facts": { ...FACTS... },
      "pis": { "pis": [ { ...PI... }, ... ] },
      "out": { ...OUTCOMES... }
    }
  ]
}
```

### FACTS (per program)
`city, stipendUSD (number), stipendLocal, stipend_basis, stipend_confidence,
stipend_foundOfficial (bool), stipendNotes, meetsFloor (bool), cohortSize, degreeStructure,
applicationRoute, deadlineAndTests, applicationRestrictions, researchFocus,
systemsEmpiricalBalance, quantQualApproach, fitScore (number 0-10), fitRationale,
siblingPrograms, sources (array)`

### PI (per faculty)
`name, category (rising_star|direction_fit|interesting|famous_but_fits), rank, hIndex (number
or null), citations (number or null), scholarUrl, startedApprox ("2021"), labSize, labFocus
(systems|empirical|both), research, whyFit, recruiting, url`.
`category` drives colors/labels; `rising_star`+`direction_fit` count as "fitting PIs".
Use `null` (not -1) for missing hIndex/citations — `build_data.py` normalizes -1 → null.

### OUTCOMES (`out`)
`careerOutcomes, admitBackgrounds, intlNotes, stipendVerified, restrictionsVerified, extraIntel`

## `_rows.json` — compact table source (one per program)
`region, school, program, city, usd (number|null), floor (bool), fit (number), multi
("✅ multi" | "⛔ 1 only" | ""), cohort`.
`region` values must match the `key`s in `_config.json.regions`.

## `_config.json` — branding + region/taxonomy config
`title, subtitle, stipend_floor (number), currency, current_year, regions
([{key,label,short,color,order}]), region_order ({key:int}), interest_areas ({bucket:[kw...]}),
col_index ({city_substr:index})`. All optional except that `regions` should cover every region
key present in `_rows.json` (else a fallback palette is used).

## Persistent user state (created by the dashboard at runtime — do not overwrite)
`_pi_notes.json` ({pi_name: note}) · `_pi_hidden.json` ({pis:[...], programs:[...]})
