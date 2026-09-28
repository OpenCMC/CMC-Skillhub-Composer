# Perpetuals, futures, and options

Use when the question concerns leverage, funding, OI, basis, liquidation, or positioning. Observed Hub examples below were discovered on 2026-09-20; refresh their contracts before execution.

## Route by evidence

- **Market-wide snapshot:** discover a Hub service with the requested derivatives universe and metrics. Aggregate OI/funding cannot establish a specific venue or contract rate. Funding's numeric unit/settlement interval may be absent; preserve the raw value and that limitation.
- **Specific venue/asset records, history or export:** find a Hub service whose input schema can express the venue, instrument and window, and verify those fields in its returned rows. A currency-level row is not an individual perpetual contract. If the discovered services do not support the requested funding history or contract, report the gap instead of substituting spot OHLCV.
- **One asset's market structure:** search `BTC perpetual funding rate open interest spot perp CVD liquidation pressure`; observed `perp_contract_analysis` accepts one identity (`cmcid`, `slug`, or `symbol`) and optional `interval`, venue lists, `liq_range`, and `lookback_days`. Its reference-price venue list and aggregated context do not guarantee exact single-contract coverage. It returns positioning evidence, not executable entries/stops.
- **Funding regime change:** search `BTC funding rate regime shift Binance`; observed `detect_funding_rate_regime_shift` requires `symbol`, with optional venue/window. Inspect whether both venue and OI-weighted history are present and current. A latest funding number alone cannot establish a regime change.
- **Ranked opportunities:** find a scanner whose universe, filters, windows and returned candidate count match the request. A single-token deep dive cannot answer a market-wide rank. Do not infer options Greeks, strike/expiry liquidity, or borrow availability from a perpetual report; discover appropriate support separately.

## Align before comparing

Record venue, base/quote, linear or inverse contract, margin/settlement currency, timestamp/timezone, and interval when they affect the result. Resolve omitted details from the user's prior context or ask if material. A broad BTC leverage overview can use declared service defaults; an exact Binance-versus-Bybit funding comparison cannot silently pick instruments.

Funding requires rate unit, payment interval and whether realized/current/predicted. Compare same intervals; show normalization formula and source cadence if converting. Do not annualize an unlabeled rate. OI can be USD notional, coins, or contracts; price changes can move USD OI without new contracts. Basis may be cash difference, ratio, or annualized; verify before formatting it as percent. Preserve the distinction between OI-weighted and simple average rates.

Align price, OI, funding and liquidation windows. A liquidation **heatmap** is estimated pressure; a liquidation **flow** is recorded forced closures. Neither is a guaranteed future price target. Distinguish missing liquidation data from a documented zero. Absent spot CVD cannot become zero or proof that spot buyers are absent.

For a squeeze/reversal judgment, use the applicable returned positioning and flow evidence plus counter-evidence, not just positive funding or rising OI. If core inputs are stale, blocked, or at the wrong scope, narrow the claim. Do not fabricate a market state from a backend `ok` flag.
