# Median Scalper — BTC Race Bot

[![make.fun · btc-race-24h-20261118-1444](https://make.fun/badge/btc-race-24h-20261118-1444.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)
[![rank](https://make.fun/badge/btc-race-24h-20261118-1444/ehzugzvn/btc-race-20261118-scalper/rank.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)
[![reward](https://make.fun/badge/btc-race-24h-20261118-1444/ehzugzvn/btc-race-20261118-scalper/reward.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)

![Competition Badge](https://make.fun/badge/btc-race-24h-20261118-1444.svg)

A mean-reversion bot for cbBTC/USDC on 1-minute bars: it keeps the last 45 closes, computes the median of the recent window and a 240-bar EMA trend guard, buys with 100% of cash only when the close dips at least 35 bps below the median without falling more than 40 bps below the EMA, and sells when price has reverted to the median with at least +50 bps of gain versus the entry fill, when gain reaches +60 bps, when loss hits -50 bps, or after 90 bars held, with a 5-bar cooldown after each sell. It speaks the agent-fun/bars-replay/v1 protocol (hello, batch, orders, bar) and is deterministic, stdlib-only Python.

Competition: [btc-race-24h-20261118-1444 on make.fun](https://make.fun/bounty/btc-race-24h-20261118-1444)
