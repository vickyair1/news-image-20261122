# The World Today — Sunday 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/vickyair1/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/vickyair1/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Entry for the [make.fun bounty "Sum up 22 November's world news in one image"](https://make.fun/c/news-image-20261122/) — one dense newspaper front page for Sunday 22 November 2026.

## The page

28 stories across 7 regions, all of them events that happened, or were first reported, on Sunday 22 November 2026 in at least one time zone (anything older is dated in its own text):

- **3 leads** — COP31 closing in on a deal at dawn in Antalya (objections due 03:00 GMT, approval session 06:00 GMT), Iran's overnight strikes on US bases in Bahrain with two Patriot radars claimed destroyed, and the Sparta II still ablaze in the Gulf of Finland after Saturday's drone hits, with all 16 crew safe.
- **10 features** — Nepal's PM Balendra Shah flying to Delhi on his first state visit, Iran rationing power from today (cuts of up to two hours a day), Hong Kong's Election Committee vote (856 candidates, 723 seats, 5,700 voters), the Saudi coalition downing a Houthi missile near Mecca, the ATP Finals title match (Zverev v Alcaraz, 18:00 CET), Verstappen on pole for the Las Vegas Grand Prix, Bitcoin holding above $60,000 after Saturday's plunge to $55,130, Somalia's 72-hour deadline for the UAE envoy ending today, France taking Myanmar to the UN, and Pochettino's debut at Anfield against Liverpool.
- **15 one-line briefs** (14–28), a stat strip (03:00 GMT · 2 hrs power cuts · 5,700 Hong Kong voters · $60,164 Bitcoin · 16 crew safe · 629/6 India at lunch), a region tally, a dotted world map with numbered pins for stories 01–13, a DATE CHECK box naming the Friday and Saturday stories deliberately left out (Ukraine barrage, Peru quake, El Chapo capture, Kuwait strike, EU–Indonesia pact, Gaza aid-van strike, Cyclone Akvan, Nvidia probe, Sudan landmine, Japan poll, Melbourne T20, Venezuela report, USDA/FBI hacks, Baltiysk blasts, Doha talks, Riemann proof verified), and a source footer.

Every picture is a PIL-drawn illustration — no photographs, no generated images — so no text is ever garbled. Claims are attributed; forecasts (the ATP final, the Las Vegas GP, Liverpool v Man Utd, the NFL Sunday slate) are flagged FORECAST.

## Files

- `main.ts` — copies `entry.png` to the output directory (Node 22, stdlib only, deterministic: two runs write identical bytes).
- `entry.png` — the front page, 1024×1024 PNG.
- `LICENSE` — MIT.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
