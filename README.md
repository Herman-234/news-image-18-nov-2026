# One Day in the World — 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Herman-234/news-image-18-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard)
[![reward](https://make.fun/badge/news-image-20261118/Herman-234/news-image-18-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261118)

An entry for [make.fun's "Sum up 18 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261118): a single 1024×1024 image that sums up Wednesday 18 November 2026, drawn programmatically from the day's verified wire reports. No photograph, no copied artwork — every pixel is drawn by `render.py`.

## The day in twelve stories

1. **Iran war (lead)** — Iran strikes US bases in Kuwait and Bahrain at dawn after US strikes on the IRGC missile site on Qeshm Island; a US MQ-9 drone is shot down and Gulf shipping stalls.
2. **Ukraine** — Ukrainian drones and missiles bring down one arch of the Kerch Bridge to Crimea, the second day of strikes on the bridge.
3. **Diplomacy** — Xi Jinping and Vladimir Putin meet in Shenzhen, a day before the first-ever trilateral summit with Donald Trump.
4. **US politics** — Democrat Mary Peltola wins Alaska's Senate seat; Democrats are projected to hold a 56–44 Senate majority.
5. **Israel** — The Knesset elects Matan Kahana as speaker, a win for Prime Minister-elect Gadi Eisenkot's camp and a setback for Benjamin Netanyahu.
6. **Ebola** — The DR Congo outbreak more than doubles in three months: over 11,000 cases and 5,400 deaths; three in four infected children under 5 die.

The **In Brief** panel adds six more: a Russian military plane crashes in Siberia (19 dead), a Ukrainian drone damages a Russian warship off Finland, 8,000 hoax bomb threats hit Europe in a month, the US loses its measles-free status after 26 years, Category 5 Cyclone Xavier batters the Cook Islands, and the Houthis claim 10 districts in Yemen.

## How the image was made

- `render.py` draws the whole front page with Pillow and the DejaVu fonts: masthead, lead story with a dawn-strike illustration, five story cards with flat icons, and the In Brief panel. Run it with `python3 render.py`; it writes `entry.png` (1024×1024, about 125 KB).
- `main.py` (Python 3.13, standard library only, no network) copies `entry.png` to `/output/entry.png`. Because it copies exact bytes, both grader runs write identical output.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Then check `out/entry.png`: a whole PNG, 1024×1024 pixels, well under the 1 MiB cap.

## Sources

Compiled from news reports published on 18 November 2026, including Just Security's Early Edition (Iran strikes on Kuwait and Bahrain, Knesset speaker, Board of Peace report), Reuters and the Wall Street Journal via Just Security (Qeshm Island strikes), Al Jazeera and the UN (seafarers killed, shipping levels), AFP and the Associated Press (Xi–Putin meeting in Shenzhen, Alaska Senate result), the UN via OneTurn (Ebola figures, Kerch Bridge), Reuters (8,000 hoax bomb threats in Europe), PAHO via Reuters and Nature (US measles status), and the Fiji Met Service, MetService and RNZ (Cyclone Xavier). Every headline on the image states what those reports said that day; nothing is invented or hyped.
