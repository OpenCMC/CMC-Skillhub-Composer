# Research report format

Read only when composing a research report. Data lookups, CSV/exports and concept answers use the user's requested concise format without this file. Shared data validation, source restrictions and error handling remain in the already-loaded SKILL.md. User-requested formats take precedence while preserving status, confidence, missing-data warnings and key numbers.

## Language

The CMC Crypto Skill Hub services return their text (conclusions, narratives, anomaly and risk descriptions, takeaways) in English. **This is source evidence, not the output language.** Render the final answer in the language of the user's most recent message — translate the English prose into that language rather than passing it through. A Chinese request gets a Chinese answer, a Japanese request a Japanese answer, and so on. If the user mixes languages or writes in English, follow the user.

Keep verbatim, regardless of output language:

- all numbers, percentages, and currency amounts;
- tickers and token names (BTC, ETH, VELVET, …), chain and venue names;
- `status`, `confidence`, `error_code`, timestamps, `skill_id`, `unique_name`;
- the fixed section labels (`**TL;DR**`, `🚨 **Notable anomalies:**`, `📰 **Macro News:**`, `**Details**`, `💡 **Takeaway:**`) — these stay in English in every language.

Everything else — every sentence, bullet description, and Details body that came back in English — is written in the user's language. Do not produce a mostly-English answer for a non-English request.

## Report status layout

If `status` is `blocked`: skip Details; in TL;DR use the block reason from `conclusion` as the first sentence; suggest one fallback only if the response provides one; end with the footer.

If `status` is `partial`, or `missing_or_stale_inputs` is non-empty, or the response reports inputs that are missing, stale, unavailable, proxied, or low coverage (even when `status` is `ok`): add a `⚠️` callout at the top of TL;DR naming what is missing, render available data, and use lower-confidence language.

## Output Template Router

After a successful run, choose the report template from the executed `unique_name`. This selects formatting only; it does not change which service you ran.

The `unique_name` lists below are **examples, not exhaustive** — services get added and renamed. Match by the service's purpose and the shape of its returned data, not only by an exact name. `find_skill` also returns each candidate's `resultType` and `skill_description`, which help disambiguate.

| Template | Example `unique_name` (match by purpose, not just these) | Read |
|---|---|---|
| Daily overview | `daily_market_overview` (incl. `_debug` / `_v*`), `build_daily_market_brief` | [template-overview.md](template-overview.md) |
| Macro read | `crypto_macro_overview`, `macro_liquidity_monitor`, `macro_financial_conditions`, `macro_news_aggregator`, `detect_market_regime`, `decode_macro_event_impact` | [template-macro.md](template-macro.md) |
| Scanner / ranking | `onchain_token_scanner`, `altcoin_breakout_scanner_spot`, `altcoin_scanner_perp`, and other `rank_*` / `screen_*` discovery scans | [template-scanner.md](template-scanner.md) |
| U.S. equity context | `us_equity_index_snapshot`, `us_equity_sector_rotation`, `us_equity_research_dossier`, `us_equity_trade_planning_context`, `us_equity_upcoming_event_calendar`, `assess_crypto_proxy_equity_beta` | [template-equity-context.md](template-equity-context.md) |
| Comparison / cost | `compare_cex_vs_dex_true_cost`, `compare_order_route_true_cost_cex_dex`, `compare_cross_venue_true_cost`, `compare_fee_tier_effective_cost`, `model_fee_tier_trade_cost` (returned `resultType: comparison_pack`) | [template-comparison.md](template-comparison.md) |
| Attribution / portfolio | `attribute_portfolio_pnl_drivers`, `rank_portfolio_pnl_driver_buckets` (`attribution_pack`); `analyze_portfolio_exposure_map`, `map_portfolio_concentration_buckets`, `portfolio_analysis`, `review_options_portfolio_greeks` | [template-attribution.md](template-attribution.md) |
| Standard (default) | anything that fits none of the above | Standard Report Format below |

Template links are relative to this file; tool readers using the skill root should prefix them with `reference/`.

Rules:

1. If the executed service fits a row (by name or purpose) and this client can read bundled files, read that reference and render per its skeleton.
2. If it fits none, the reference cannot be read, or you are unsure, use the Standard Report Format. Falling back is always safe.
3. Field names in the templates are **typical, not guaranteed** — a field may be absent or nested differently (for example `ranked_candidates` at the top level in one service but under `report` in another). Map by meaning; if a field is missing, omit that part rather than inventing it, or fall back to the Standard Report Format.
4. Every template shares this file's rules: TL;DR first, no tables, no raw wrapper, match the user's language, fixed section labels, exact `———` divider, and the footer. A reference only changes how Details is organized.

## Standard Report Format

Plain Markdown for chat clients. No tables. No HTML. Keep normal reports at or below 2500 characters unless the user asks for depth; scanner reports may reach 4000 when candidate lists require it. Match the language of the user's most recent message.

```text
**TL;DR**

Sentence 1 — what the result found.
Sentence 2 — the bottom line and what to do or avoid.
Sentence 3 — the 1-2 key numbers behind it.

🚨 **Notable anomalies:**

- 1-3 bullets, or (none significant in this run)

———

**Details**

**Topic**

- evidence bullets, numbers verbatim

💡 **Takeaway:** what it means, what to watch, a concrete next step.

🕐 timestamp · status · confidence
```

Append `· skill_id` to the footer when present. Use `n/a` for missing footer values; never invent timestamp, status, confidence, or skill id.

Start the answer directly with `**TL;DR**` — no preamble, acknowledgement, or process line (for example "data received, rendering the report…"). The only horizontal divider is the single `———` between TL;DR and Details; never emit `---` or `***` anywhere, including before the report.

Fixed section labels — do not translate: `**TL;DR**`, `🚨 **Notable anomalies:**`, `📰 **Macro News:**`, `**Details**`, `💡 **Takeaway:**`. Include `📰 **Macro News:**` only when the response or allowed external sources carry macro news or key events. For blocked responses omit `———` and Details. Group Details by the response's natural topics; do not force a fixed taxonomy.

## Self-check before answering

Always verify:

- the response was parsed (no `raw_output` string shown as the result);
- no table, no HTML, no raw wrapper, no tool trace;
- the answer starts directly at `**TL;DR**` with no preamble, and contains no `---` or `***` — only the single `———`;
- identifiers keep literal underscores (`price_change_4h`), not backslash-escaped (`price\_change\_4h`);
- the narrative is in the user's language — the English prose from the service was translated, not copied through; only numbers, tickers, IDs, status/confidence strings, and the fixed labels stay verbatim;
- the footer is present with real values or `n/a`.

If you used the Standard Report Format, also verify exactly one `**TL;DR**`, one `———`, and one `**Details**` for non-blocked reports, with `🚨 **Notable anomalies:**` and at least one `💡 **Takeaway:**`. If you used a matched template, verify its own "Minimum" checklist instead.

## Spacing

One blank line between distinct blocks. Exactly one `———` between TL;DR and Details, nowhere else. Bullet marker is `-`; one bullet per line. Write underscores in identifiers and field names literally — do not backslash-escape them (`price_change_4h` and `skill_id`, never `price\_change\_4h`).
