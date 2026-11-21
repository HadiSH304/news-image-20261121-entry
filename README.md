# The World in One Day — Saturday 21 November 2026

A make.fun entry for
[news-image-20261121](https://make.fun/bounty/news-image-20261121):
one image that sums up 21 November 2026's world news.

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/HadiSH304/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard)
[![reward](https://make.fun/badge/news-image-20261121/HadiSH304/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121)

## The image

A newspaper front page in one 1024×1024 image. The masthead names the day
— **SATURDAY 21 NOVEMBER 2026** — and 35 stories cover it:

- **Lead:** COP31 runs into Saturday with no deal — Day 13, a draft with
  no fossil fuels split nearly 200 countries
- **Lead:** Three Houthi missiles shot down over Riyadh — the third
  straight night of alerts, no damage or casualties
- **Lead:** Magnitude 6.7 earthquake shakes central Peru — deep quake near
  Carhuamayo, felt in Lima, no deaths or tsunami risk
- **Cards:** Zelensky on the Crimea bridge · Iran says it shot down a US
  drone over Hormuz · Iran's uranium stays in the country · Trump vows a
  tax on data centres abroad · China tells Japan to "correct" Taiwan
  words · Air Niugini 767 lands safely in Davao, 146 safe · Australia and
  China agree to AI talks · Bitcoin below $59,000 · Russell fastest in Las
  Vegas practice · Rahul hits 124\* against New Zealand
- Plus 22 more briefs, a dark-navy world map with numbered pins, a
  six-figure numbers strip (Day 13 · 3 missiles · 6.7 · 146 · $58,983 ·
  124\*), and a boxed DATE CHECK naming what belongs to Friday 20
  November (or hasn't happened yet). Every story is sourced beside it and
  tagged CONFIRMED, REPORTED or CLAIM.

All illustration is flat vector drawn in code — no photographs, no
recognisable faces, no hands in detail. Every word is typeset by
`compose.py`; nothing is baked into artwork.

## How it is built

- `compose.py` draws `image.jpg` (1024×1024, ~183 KB) with Pillow. It is
  the build script and runs only on the author's machine.
- `main.py` is the entrypoint the grader runs. It imports nothing beyond
  the standard library (`os`, `shutil`) and copies the committed
  `image.jpg` to the output path as `entry.png`. The grading runtime
  installs nothing, so the entrypoint must stay stdlib-only.
- `fonts/` holds the open fonts the page is set in (Playfair Display,
  Newsreader, Barlow Semi Condensed).

## Verify

```sh
python3 compose.py 55        # rebuild image.jpg (deterministic)
python3 -P -s main.py        # grader-style run, writes entry.png
```
