# Stack / Flow — Scratch edition

A single-player falling-block game inspired by TETR.IO's minimal competitive layout, built with editable native Scratch 3 blocks and original embedded vector artwork.

**[Download the game](https://github.com/vnanzero-crypto/tetris-on-scratch/blob/main/stack-flow.sb3)** — click **Download raw file** (↓), then open [Scratch](https://scratch.mit.edu/projects/editor/) and choose **File → Load from your computer**. Click the green flag to play.

![Gameplay preview](docs/preview.png)

## Controls

| Key | Action |
| --- | --- |
| A / D | Move left / right, with automatic repeat |
| S | Soft drop |
| W | Rotate clockwise |
| Z | Rotate counterclockwise |
| Space | Hard drop |
| C | Hold / swap once per piece |
| R | Restart |
| 1–5 | Select a theme |
| T | Cycle to the next theme |

Arrow keys are no longer bound. Holding W makes one rotation; release and press again for another rotation.

## Scoring

Each successful rotation awards **5 points**; a blocked rotation awards nothing. Soft drop awards 1 point per cell and hard drop awards 2 points per cell.

| Lines cleared | Normal clear | T-spin |
| --- | --- | --- |
| 0 | 0 | 400 |
| 1 | 100 | 800 |
| 2 | 300 | 1,200 |
| 3 | 500 | 1,600 |
| 4 | 800 | — |

Clear and T-spin scores are multiplied by the current level, before updating the level. T-spin scores replace normal line-clear scores; the rotation's 5 points are additional. A T-spin requires a T piece whose last successful horizontal/rotation action was a rotation and at least three occupied corners around its center when it locks. Walls and floor count as occupied. Successful horizontal movement, spawning, and hold reset spin eligibility; failed movement and vertical drops preserve it. This is a simplified three-corner rule without separate mini-T-spin or SRS kick classifications.

## Combos, camera, and themes

Clear again within **four seconds** to increase COMBO. The first clear starts at 1; each new clear refreshes the timer. Non-clearing placements do not break the chain while time remains. After four seconds without a clear, the counter resets. A shrinking bar below COMBO shows the remaining time.

Combo bonus per clear is **50 × (COMBO − 1) × level**, in addition to line-clear or T-spin points. The first clear has no extra combo bonus. Restarting or topping out resets the combo.

A line clear gives the game view a brief, decaying shake of at most 1.6 pixels horizontally and 0.8 vertically. The game view is rendered at **82% scale**; the logical board and collision rules stay the same. The themed landscape and selector remain steady.

Click the theme buttons, press **1–5**, or use **T** to cycle. Changing themes preserves the board, score, and combo, and restarting retains the chosen theme.

| Key | Theme | Background and block style |
| --- | --- | --- |
| 1 | [Galaxy](docs/theme-1.png) | Nebulae, stars, ringed planet; shimmering blocks |
| 2 | [Mountains](docs/theme-2.png) | Snowy peaks, pines and moon; faceted blocks |
| 3 | [Ocean](docs/theme-3.png) | Underwater light rays, fish and coral; wave blocks |
| 4 | [Sunset](docs/theme-4.png) | Warm sun, dunes and palms; striped blocks |
| 5 | [Neon City](docs/theme-5.png) | Night skyline, glowing windows and grid; neon-bordered blocks |

![Timed combo](docs/combo.png)

## Features

10×20 board, seven-bag randomization, remaining-bag preview, hold, ghost piece, wall/floor kicks, lock delay, line clearing, and increasing gravity every ten lines. The next preview shortens until the next seven-piece bag is generated.

Line clears launch an animated light sweep across the actual cleared rows and 12 moving sparks per row. Four-line clears and T-spin clears use purple highlights; effects fade and expire after 24 rendered frames. T-spins and line clears show distinct callouts.

![Four-line clear effect](docs/clear-effect.png)

The artwork is original and TETR.IO-inspired. This is not an affiliated release or a full reproduction: there are no online multiplayer services, accounts, rankings, replays, exact SRS tables, or combo/back-to-back bonuses.

## Build and validate

Python 3.10+ builds the project without Python dependencies or network access:

```sh
python3 tools/build.py
```

The builder writes `dist/stack-flow.sb3`, containing the Scratch blocks and all 119 SVG assets. `stack-flow.sb3` at the repository root is the published download; after rebuilding, copy the output there when preparing a release.

To run the gameplay checks with dependencies outside the checkout:

```sh
npm install --prefix /tmp/stack-flow-check scratch-vm@5.0.300 scratch-storage@4.1.27 --no-audit --no-fund
NODE_PATH=/tmp/stack-flow-check/node_modules node tools/check.cjs
```

All 71 Scratch VM assertions passed, covering board state, collisions, movement, rotation scoring, hold, T-spin eligibility and bonuses, ordinary and four-line clears, animation row tracking/expiry, four-second combo boundaries and bonus scoring, camera shake limits and settling, all five theme palettes and backdrops, theme cycling, preserved game state, and game over. Headless tests intentionally omit a renderer and may emit costume-renderer warnings.

Chromium checks separately exercised A/D/S/W/Z, removal of arrow bindings, key edge handling, hold, hard drop, an actual W-and-Space T-spin, and the rendered four-line effect. They also verified actual 82% scaling, all five number-key and clickable theme selections, T cycling, a timed combo chain scoring 100 then 150 points, four-second real-time expiry, and camera settling. Preview screenshots use deterministic board fixtures.
