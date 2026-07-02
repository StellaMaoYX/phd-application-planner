# Honesty & verification rules

Applicants make real, expensive decisions from this data. Accuracy beats coverage.

1. **Never fabricate** a stipend, deadline, cohort number, application rule, PI, h-index, or
   citation count. If a figure isn't confirmable on an official/primary source, record it as
   not found and set `stipend_confidence` / a caveat accordingly — do not guess a plausible number.

2. **Stipends** — prefer the program's official funding page or an authoritative pay scale.
   Watch for common traps: 9-month vs 12-month base, tuition-inclusive vs stipend-only,
   department minimum vs actual, local currency vs the applicant's currency. State the basis
   in `stipend_basis`. The workflow's adversarial verify stage exists to catch these — keep it.

3. **`meetsFloor`** must be computed honestly against the user's stipend floor (converted to
   the same currency). Below-floor programs stay in the data (flagged), not silently dropped.

4. **Application restrictions** — verify precisely whether the applicant may apply to more than
   one program at an institution per cycle; this materially changes strategy. Distinguish
   institution-wide rules from sub-unit (e.g. umbrella-vs-department) rules.

5. **h-index / citations** are Google Scholar snapshots — mark them as such; they drift. Use
   `null` for not-found, never a made-up number.

6. **`category`** must be defensible: `rising_star` = genuinely junior/rising (lab ~recently
   started); don't label a senior famous PI as rising to please a rising-star preference.

7. **Currency / dates** — convert stipends to the user's currency and note the rate/date;
   convert relative dates ("next cycle") to absolute where possible.

8. **No personal data** — never embed the applicant's name or identity in any generated file.
   The output is about programs and PIs.

When unsure, say so in the record (`stipendNotes`, `extraIntel`, caveats) rather than
projecting false confidence.
