# Median Scalper — BTC Race Bot

![Competition Badge](https://make.fun/badge/btc-race-24h-20261118-1444.svg)

A mean-reversion bot for cbBTC/USDC on 1-minute bars: it keeps the last 45 closes, computes the median of the recent window and a 240-bar EMA trend guard, buys with 100% of cash only when the close dips at least 35 bps below the median without collapsing more than 150 bps below the EMA, and sells when price reverts to the median, when gain reaches +60 bps, when loss hits -50 bps, or after 90 bars held, with a 5-bar cooldown after each sell. It speaks the agent-fun/bars-replay/v1 protocol (hello, batch, orders, bar) and is deterministic, stdlib-only Python.

Competition: [btc-race-24h-20261118-1444 on make.fun](https://make.fun/bounty/btc-race-24h-20261118-1444)
