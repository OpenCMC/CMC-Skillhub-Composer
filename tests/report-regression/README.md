# Composer report compatibility regression

The baseline is GitHub main at `a7cb81af67ac5642b4c9ee1d631aca108e665a45`.
The final skill bundle SHA-256 is `c2737c132107b3e1e1db942982312a61229075532ca2df13f6ccaac79ac324e9`.
The bundle hash covers sorted relative file paths, a NUL byte and file bytes; Python bytecode/cache files are excluded.

## What was preserved

Run `python3 tests/verify_report_compatibility.py` from a full Git checkout.
It compares the five original templates and eight startup files byte for byte,
and checks the original inline language, Standard format, self-check, spacing,
router rows/rules, successful-run default and blocked/partial formatting.
This source check does not prove agent behavior.

## Actual agent runs

Real Codex CLI 0.157.1 agents used the same fixed data and isolated read-only tools.
The requested model settings were `gpt-6-astra` / `ultra`. Tools supplied synthetic
Hub discovery/execution responses and a reader restricted to the tested bundle.
For the read-failure case, the reader explicitly refused the overview template.
No live market endpoint or paid Hub execution was used.

Each final case ran once. Outputs were checked mechanically for routing and shared
report structure, then reviewed by the implementer against the case's semantic
checks and the templates' Minimum checklists. This was not blinded. It does not
require identical prose, translated subsection wording or rigid sentence counts.

| Shared case | Original main A | Final candidate B |
|---|---|---|
| Brief Daily overview | Pass | Pass |
| Brief Macro read | Missing Notable anomalies heading | Pass |
| Scanner / ranking | Pass | Pass |
| Comparison / cost | Pass | Pass |
| Attribution / portfolio | Pass | Pass |
| Standard fallback for unmatched service | Pass | Pass |
| Partial overview / missing inputs | Pass | Pass |
| Blocked overview | Pass | Pass |
| Unreadable template / inline fallback | Pass | Pass |

The final candidate also passed five output-boundary cases: standalone NVDA,
standalone COIN, explicitly requested BTC/equity context, explicit CSV and a
two-sentence concept explanation. Total: **14/14 final template/output cases**.
The original main observation was **8/9**, which is a single-run observation,
not evidence of a general accuracy or stability improvement.

Two development failures are retained in the records: a template-read diagnostic
leaked into a report, and symbol-only PEPE diligence ran before identity confirmation.
The final bundle fixes both. Its three domain boundary checks completed with
**8 Hub business calls, 0 non-Hub calls and 0 schema errors**. The identity case
made one discovery call and no analysis execution. The DEX and derivatives cases
still lack requested evidence; passing means respecting that boundary, not filling it.
Two domain answers still cite skill rules when clarifying identity or explaining
source limits; that client presentation limitation remains visible in the records.

The unchanged offline JSON helper separately passed **15 parser tests** in the
development workspace. Those tests are not counted as template behavior tests.

## Evidence and limits

- [cases.json](cases.json) contains all 14 prompts, checks and synthetic tool fixtures.
- [results.json](results.json) contains the nine baseline answers, all 14 final answers,
  file reads, business calls, bundle/fixture hashes, domain results and retained failures.
- The domain fixtures are mixed captured/synthetic development fixtures, not live reruns.
- Startup failures from obsolete/missing CLI components were excluded before scoring.
- These checks do not measure live Hub coverage, search relevance, token savings or
  repeated-run stability. The original template content remains the compatibility contract.
