# The World Today — Sunday 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/vickyair1/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/vickyair1/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Entry for the [make.fun bounty "Sum up 22 November's world news in one image"](https://make.fun/c/news-image-20261122/) — one dense newspaper front page for Sunday 22 November 2026.

## The page

36 stories across 7 regions, all of them events that happened, or were first reported, on Sunday 22 November 2026 in at least one time zone (anything older is dated in its own text):

- **3 leads** — COP31 closing in on a deal at dawn in Antalya (objections due 03:00 GMT, approval session 06:00 GMT), Iran's overnight strikes on US bases in Bahrain with two Patriot radars claimed destroyed, and Nepal's PM Balendra Shah flying to Delhi on his first state visit.
- **10 features** — the Sparta II still ablaze in the Gulf of Finland after Saturday's drone hits, the ATP Finals title match (Zverev v Alcaraz, 18:00 CET), Verstappen on pole for the Las Vegas Grand Prix, Bitcoin holding above $60,000 after Saturday's plunge to $55,130, Somalia's 72-hour deadline for the UAE envoy ending today, Trump vowing a "permanent" Iran deal, France taking Myanmar to the UN, four killed in Gaza despite the truce, Pochettino's debut at Anfield against Liverpool, and 40,000 runners in the Philadelphia Marathon.
- **23 one-line briefs** (14–36), a stat strip, a region tally, a dotted world map with numbered pins for stories 01–13, a DATE CHECK box naming the Friday and Saturday stories deliberately left out (Peru quake, Eisenkot mandate, El Chapo capture, Roundup, Gupta, Nitish Setu, Basra fire, England 37-12, Leeds 4-1, the US airlines warning, the Hegseth memo), and a source footer.

Every picture is a PIL-drawn illustration — no photographs, no generated images — so no text is ever garbled. Claims are attributed; forecasts (the ATP final, the Las Vegas GP, Liverpool v Man Utd, the Philadelphia Marathon, the NFL Sunday slate, the Sunday Angelus) are flagged FORECAST.

## Files

- `main.ts` — copies `entry.png` to the output directory (Node 22, stdlib only, deterministic: two runs write identical bytes).
- `entry.png` — the front page, 1024×1024 PNG.
- `LICENSE` — MIT.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
