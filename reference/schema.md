# Data schema (what the dashboard reads)

The marimo app (`dashboard_template.py`) reads three files from its own folder.

## `_research_data.json` — grouped by school
```json
{
  "<School Name>": [
    {
      "program": "Computational Biology PhD",
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
applicationRoute, deadlineAndTests, applicationRestrictions, researchFocus, wetDryIntegration,
gwasOrMechanistic, fitScore (number 0-10), fitRationale, siblingPrograms, sources (array)`

### PI (per faculty)
`name, category (rising_star|direction_fit|interesting|famous_but_fits), rank, hIndex (number
or null), citations (number or null), scholarUrl, startedApprox ("2021"), labSize, wetDry
(dry|wet|both), research, whyFit, recruiting, url`.
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
