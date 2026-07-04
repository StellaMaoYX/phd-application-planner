// phd-application-planner · parallel research workflow (TEMPLATE)
// Runs entirely in parallel: discover candidate programs per region → per-program
// (facts ‖ PIs ‖ outcomes) → adversarial stipend/restriction verify.
// Drive it by passing the intake config as `args` (see SKILL.md). No editing needed
// for the common case; edit only to tune counts or add a seed program list.

export const meta = {
  name: 'phd-application-planner-research',
  description: 'Parallel web-research of PhD programs + fitting PIs for a user-defined field/region/funding profile',
  phases: [
    { title: 'Discover', detail: 'per-region candidate program discovery (parallel)' },
    { title: 'Research', detail: 'per-program facts ‖ PIs ‖ outcomes (parallel, pipelined)' },
    { title: 'Verify', detail: 'adversarial stipend + application-restriction verification' },
  ],
}

const cfg = args || {}
const FIELD = cfg.field || 'human-computer interaction'
const SUBFIELDS = cfg.subfields || ''
const REGIONS = cfg.regions || [{ key: 'US', label: 'United States' }]
const FLOOR = cfg.stipend_floor || 35000
const CURRENCY = cfg.currency || 'USD'
const N_TOTAL = cfg.n_programs || 20
const N_PIS = cfg.n_pis_per_program || 10
const PI_PREFS = cfg.pi_preferences || 'favor rising-star / direction-fit PIs (small, young, actively-recruiting labs) over famous names'
const RISING_WEIGHT = cfg.rising_star_bias || 'strong'
const EXTRA = cfg.notes || ''
const SEED = cfg.seed_programs || []  // optional [{school, program, region, city}]

const WEB = `You have web access. If WebSearch/WebFetch are not already callable, FIRST call ToolSearch with query "select:WebSearch,WebFetch" to load them, then use them. Verify against CURRENT official program / admissions / funding pages and Google Scholar. Do NOT fabricate stipends, deadlines, cohort numbers, or PIs — if a figure is not confirmable, say so honestly and set confidence accordingly.`

const PROFILE = `Applicant profile driving fit:
- Field: ${FIELD}${SUBFIELDS ? ' — subfields: ' + SUBFIELDS : ''}
- Target regions: ${REGIONS.map(r => r.label || r.key).join(', ')}
- Hard stipend floor: ${FLOOR} ${CURRENCY}/year (mark meetsFloor accordingly)
- PI preference: ${PI_PREFS}. Rising-star bias: ${RISING_WEIGHT}.
${EXTRA ? '- Notes: ' + EXTRA : ''}`

const DISCOVER_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    programs: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          school: { type: 'string' }, program: { type: 'string' },
          city: { type: 'string' }, whyRelevant: { type: 'string' },
        },
        required: ['school', 'program'],
      },
    },
  },
  required: ['programs'],
}

const FACTS_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    city: { type: 'string' },
    stipendUSD: { type: 'number', description: `annual stipend converted to ${CURRENCY} (number only; -1 if not found)` },
    stipendLocal: { type: 'string', description: 'stipend as stated on the official page, incl. local currency' },
    stipend_basis: { type: 'string' }, stipend_confidence: { type: 'string', description: 'high|medium|low' },
    stipend_foundOfficial: { type: 'boolean' }, stipendNotes: { type: 'string' },
    meetsFloor: { type: 'boolean' },
    cohortSize: { type: 'string' }, degreeStructure: { type: 'string' },
    applicationRoute: { type: 'string' }, deadlineAndTests: { type: 'string' },
    applicationRestrictions: { type: 'string', description: 'CRITICAL: can the applicant apply to >1 program here per cycle? state clearly' },
    researchFocus: { type: 'string' },
    systemsEmpiricalBalance: { type: 'string', description: 'balance of systems-building/engineering work (robots, prototypes, interaction techniques) vs empirical/user-study work (human-subjects experiments, field deployments) in this program' },
    quantQualApproach: { type: 'string', description: 'balance of quantitative methods (controlled experiments, stats, log/sensor analysis) vs qualitative methods (interviews, ethnography, design research) in this program' },
    fitScore: { type: 'number', description: 'fit-for-applicant 0-10 (one decimal ok)' },
    fitRationale: { type: 'string' }, siblingPrograms: { type: 'string' },
    sources: { type: 'array', items: { type: 'string' } },
  },
  required: ['stipendUSD', 'stipend_foundOfficial', 'meetsFloor', 'applicationRestrictions', 'fitScore'],
}

const PIS_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    pis: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          name: { type: 'string' },
          category: { type: 'string', description: 'one of: rising_star (junior/rising, lab ~2019+), direction_fit (mid-career, strong topic match), interesting (novel methods), famous_but_fits (senior/famous but relevant)' },
          rank: { type: 'string' }, hIndex: { type: 'number', description: 'Google Scholar h-index; -1 if not found' },
          citations: { type: 'number', description: 'total citations; -1 if not found' },
          scholarUrl: { type: 'string' }, startedApprox: { type: 'string', description: 'year lab started, e.g. "2021"' },
          labSize: { type: 'string' }, labFocus: { type: 'string', description: 'systems | empirical | both — does the lab primarily build systems/prototypes (interfaces, robots, toolkits), run human-subjects/user studies, or both' },
          research: { type: 'string' }, whyFit: { type: 'string' },
          recruiting: { type: 'string' }, url: { type: 'string' },
        },
        required: ['name', 'category', 'whyFit'],
      },
    },
  },
  required: ['pis'],
}

const OUT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    careerOutcomes: { type: 'string' }, admitBackgrounds: { type: 'string' }, intlNotes: { type: 'string' },
    stipendVerified: { type: 'string' }, restrictionsVerified: { type: 'string' }, extraIntel: { type: 'string' },
  },
  required: ['careerOutcomes'],
}

// ---------- Phase 1: Discover ----------
phase('Discover')
let candidates = SEED.slice()
if (candidates.length < N_TOTAL) {
  const perRegion = Math.max(4, Math.ceil((N_TOTAL - candidates.length) / REGIONS.length) + 2)
  const found = await parallel(REGIONS.map(r => () =>
    agent(`${WEB}\n\n${PROFILE}\n\nTASK: List ${perRegion} strong PhD programs in ${r.label || r.key} for this applicant's field, that plausibly meet the stipend floor and are a good research fit. Prefer programs with dense rising-star / direction-fit faculty. For each: school, program (exact name), city, one-line whyRelevant.`,
      { label: `discover:${r.key}`, phase: 'Discover', schema: DISCOVER_SCHEMA }).then(x => ({ region: r.key, x }))
  ))
  const seen = new Set(candidates.map(c => (c.school + '|' + c.program).toLowerCase()))
  for (const item of found.filter(Boolean)) {
    for (const p of (item.x.programs || [])) {
      const k = (p.school + '|' + p.program).toLowerCase()
      if (seen.has(k)) continue
      seen.add(k)
      candidates.push({ region: item.region, school: p.school, program: p.program, city: p.city || '' })
    }
  }
}
candidates = candidates.slice(0, N_TOTAL)
log(`researching ${candidates.length} programs across ${REGIONS.length} regions`)

// ---------- Phase 2+3: Research (facts ‖ PIs ‖ outcomes) then Verify ----------
phase('Research')
const results = await pipeline(
  candidates,
  (c) => parallel([
    () => agent(`${WEB}\n\n${PROFILE}\n\nTASK: Full factual profile of the PhD program "${c.program}" at ${c.school} (${c.city || 'city?'}). Confirm current stipend (in ${CURRENCY}), whether it meets the ${FLOOR} floor, funding model, cohort size, application route + deadlines + tests, and CRITICALLY whether an applicant may apply to more than one program at this institution per cycle. Give a fitScore 0-10 for this applicant. Fill the schema.`,
      { label: `facts:${c.school}`, phase: 'Research', schema: FACTS_SCHEMA }),
    () => agent(`${WEB}\n\n${PROFILE}\n\nTASK: Find ${N_PIS} PIs at/through "${c.program}" (${c.school}) who fit this applicant. ${PI_PREFS}. Categorize each as rising_star / direction_fit / interesting / famous_but_fits. For each include Google Scholar h-index + citations, lab start year, lab size, lab focus (systems-building vs empirical/user-study vs both), recruiting status, and a why-fit line.`,
      { label: `pis:${c.school}`, phase: 'Research', schema: PIS_SCHEMA }),
    () => agent(`${WEB}\n\n${PROFILE}\n\nTASK: Career outcomes (academia/industry, named examples if findable), typical admit backgrounds, and international-student funding/CPT notes for "${c.program}" at ${c.school}. Be honest about what is/isn't published.`,
      { label: `out:${c.school}`, phase: 'Research', schema: OUT_SCHEMA }),
  ]).then(([facts, pis, out]) => ({ ...c, facts, pis, out })),
  // Verify stage: adversarial stipend + restriction double-check, merged into facts
  (rec) => {
    if (!rec || !rec.facts) return rec
    return agent(`${WEB}\n\n${PROFILE}\n\nADVERSARIAL VERIFY for "${rec.program}" at ${rec.school}. A prior pass reported: stipend=${rec.facts.stipendUSD} ${CURRENCY} (official=${rec.facts.stipend_foundOfficial}); restriction="${rec.facts.applicationRestrictions}". Try to REFUTE these against the official pages. Return corrected stipendUSD, stipend_foundOfficial, stipend_confidence, stipendNotes, and applicationRestrictions (and meetsFloor vs ${FLOOR}). If the prior values hold, return them unchanged.`,
      { label: `verify:${rec.school}`, phase: 'Verify', schema: {
        type: 'object', additionalProperties: false,
        properties: {
          stipendUSD: { type: 'number' }, stipend_foundOfficial: { type: 'boolean' }, stipend_confidence: { type: 'string' },
          stipendNotes: { type: 'string' }, applicationRestrictions: { type: 'string' }, meetsFloor: { type: 'boolean' },
        }, required: ['stipendUSD', 'meetsFloor'],
      } }).then(v => {
        if (v) Object.assign(rec.facts, {
          stipendUSD: v.stipendUSD, stipend_foundOfficial: v.stipend_foundOfficial ?? rec.facts.stipend_foundOfficial,
          stipend_confidence: v.stipend_confidence || rec.facts.stipend_confidence,
          stipendNotes: v.stipendNotes || rec.facts.stipendNotes,
          applicationRestrictions: v.applicationRestrictions || rec.facts.applicationRestrictions,
          meetsFloor: v.meetsFloor,
        })
        return rec
      })
  }
)

return { field: FIELD, regions: REGIONS, floor: FLOOR, currency: CURRENCY, programs: results.filter(Boolean) }
