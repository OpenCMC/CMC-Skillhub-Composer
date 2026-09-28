# U.S. equities and cross-asset context

Standalone U.S. equity research is in scope when a discovered Hub service supports it. Crypto metadata/quotes are not U.S. stock quotes. **Tokenized equity** products are distinct instruments with issuers, chains and trading rules; do not silently use them for the underlying listed stock.

Use focused queries for the actual evidence rather than one overloaded “stocks macro BTC sectors” query. In the 2026-09-20 discovery, an overloaded equity query returned altcoin services above genuine equity candidates; splitting into an index query and an exact-ticker research query recovered useful capabilities.

| Need | Observed example / useful query | Boundary to verify |
|---|---|---|
| Broad U.S. index tape | `us_equity_index_snapshot`; `U.S. stock index S&P 500 Nasdaq Dow completed session snapshot` | Actual index identities; market phase; current session vs completed returns. Observed schema accepts only `preview: true`, not symbols or arbitrary window. |
| Company fundamentals/filings | `us_equity_research_dossier`; `NVDA U.S. equity company fundamentals valuation SEC filings research dossier` | One exact `symbol`; facts and interpretation separated; no promised analyst estimates or transcripts. |
| Price/volume structure | `us_equity_trade_planning_context`; `NVDA completed session price volume benchmark context` | EOD evidence, not a live executable quote; no options/borrow inference. |
| Scheduled event risk | `us_equity_upcoming_event_calendar`; `NVDA upcoming event calendar earnings` | Observed fixed rolling 168h UTC window and symbol-only schema; cannot change it to a month. |
| Durable uptrends / breakout continuation | Discover current uptrend-quality or momentum scanner | Completed-session vs intraday scope, universe, candidate count; a scanner is not proven alpha. |
| Sector/basket leadership | `U.S. equity sector rotation industry leadership breadth` | Must actually return equity-sector evidence. `altcoin_sector_analysis` is not equivalent. A historical name like `us_equity_sector_rotation` is not permission to execute without discovery. |
| Crypto-linked stocks / BTC beta | Discover proxy-equity screening or beta analysis | Public-company exposure, aligned sample, benchmark, residual risk; business exposure is not price beta. |
| BTC with stocks/DXY/gold/rates | Separate asset comparison from macro-condition evidence as needed | Each requested asset needs its own sourced observation; a narrative mentioning DXY is not DXY data. |

Check listing identity, currency, session date, timezone, delayed/live/EOD status, and corporate-action adjustments before comparisons. Crypto trades continuously; equities have sessions and holidays. Align timestamp/sample and use completed sessions for historical returns. Price levels alone do not establish correlation, beta, or causal decoupling. If computing them, obtain aligned return series and state horizon/sample/method.

Do not call both a broad dossier and narrow packs if the first already covers the request. Conversely, a crypto overview mentioning “stocks rose” is insufficient for separate index breadth, rates and company event requirements. A source with a fixed calendar window cannot fulfill an arbitrary historical/monthly calendar; return the verified portion and seek the remaining evidence from another suitable Hub service, or disclose the gap.

An event with date-only precision stays date-only. A checked quiet calendar is different from a failed event lookup. Keep financial reporting period separate from publication/filing date; latest fetch time does not refresh old financials.

For crypto-proxy beta, the observed `assess_crypto_proxy_equity_beta` accepts 2–8 distinct `symbols`, with MSTR/COIN defaults, and uses 60 aligned equity-session returns. If using its default comparison to obtain COIN context, identify the extra comparator and extract the requested stock; do not pass an invalid single-symbol array or call the result a different horizon.

For ETF demand versus leverage, `detect_etf_flow_price_absorption` supports BTC/ETH and an observed fixed `time_window: "7d"` meaning seven ETF sessions. Explicitly pass `asset: "ETH"` for ETH; an omitted optional asset would become BTC. Keep session-window ETF/price evidence separate from rolling 7-day quote changes and 24h derivatives. A BTC-specific ETF report does not answer ETH demand, even if ranked first.
