# Onchain, DEX, and DeFi

Route by the user's evidence object. A ticker, token contract, wallet, transaction hash, and pool/pair are different identities. Chain is essential for addresses; the same address string can exist on multiple networks. Use trusted identity metadata to disambiguate, not rank or guessed chain defaults.

## Match the right evidence

| Question | Suitable evidence | Insufficient substitute |
|---|---|---|
| Holder concentration or holding age | Token-level holder aggregates/list, explicit denominator, time | Whale-transfer counts |
| Did large wallets transfer to exchanges? | Transaction-level transfers, value, chain, timestamps, direction and exchange labels | Holder distribution or ETF flows |
| Did the wallet actually sell? | Observed swaps/trades and token flows, with transaction references | Deposit/transfer alone |
| Pool liquidity, execution price, historical bars | Identified chain + pool/pair, reserves/liquidity, swaps, aligned candles | CEX price or global token volume |
| Contract and memecoin risk | Exact chain+contract, security flags, holder composition, pool coverage, liquidity/lock evidence | A clean price chart or “security passed” slogan |
| Protocol yield, TVL, utilization | Matching protocol/market/chain data and definitions | Governance-token price or market cap |

Verify which evidence the discovered Hub service actually returns. Holder aggregates do not establish wallet transactions or exchange netflows; a token/pool report does not establish arbitrary wallet-history coverage. Empty objects mean unavailable, and service names alone do not prove transaction rows or entity labels exist.

## Hub search and schema boundaries

- Whale anomalies: query one asset, chain and timeframe using `whale transfer anomalies exchange flows`. Observed `monitor_whale_transfer_anomalies` accepts `symbol`, `chain`, `window` (`1d`, `7d`, `30d`). Supply the actual requested asset/chain even though its defaults can otherwise become BTC + ethereum. It has no minimum-USD parameter. A $10M filter can be applied only to returned transaction rows with USD values; an aggregate summary cannot prove the complete >$10M set.
- One EVM memecoin: `onchain_memecoin_analysis` and `onchain_memecoin_token_profile` were observed with identity alternatives including `contract_address` + `chain`. The analysis service's EVM scope does not establish Solana support. Read its current description and output coverage.
- New-token discovery: the observed `onchain_token_scanner` description promises a chain-specific scan, but its schema exposes only `max_gain_threshold` and required `top_n_deep_dive` (1–2). Do not pass an invented chain, ask the user for a chain just to discard it, or label returned candidates as the requested chain. Use a capability with enforceable chain scope, or disclose that a complete scoped scan is unavailable. Returned rows with chain metadata may support a limited local filter, not an exhaustive chain scan.
- DeFi: a focused `Aave protocol lending borrowing utilization supply APY TVL` query recovered `review_yield_sustainability` (required `protocol_or_pool`) and `detect_borrow_market_stress` (optional `protocol`, `time_window`), below an unrelated token report. Verify returned pool/network scope and historical support; a requested window does not guarantee a time series. If candidates still provide only token research, refine the Hub query or report the unsupported scope. Do not treat a related token as coverage.

## Interpret carefully

Exchange-linked transfers are not proven sales. Record labeling provenance, self-transfers/bridges/mints/burns where known, and uncertainty in owner attribution. Address count is not unique people; pools, custodians and bridges may dominate holder concentration. Never equate a displayed top-holder percentage with freely tradeable supply without denominator/context.

Security flags and liquidity locks describe observed checks at a time; they do not establish that a token is safe or an audit is complete. DEX liquidity/volume may differ across pools; do not mix token-wide and pool-level metrics. Mark incomplete pagination or unsupported networks. A verified empty result means no matching records in the checked scope; a failed or incomplete query means unknown.
