# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A small uv-managed Python tool, kept in the `qr-codes/` subdirectory of the `melbpy-identity` repo (MelbPy logos and brand material; see `../README.md` for brand colours and fonts). It generates QR codes with the MelbPy icon (`logo.svg`) in the centre, for promo material.

## Commands

```bash
uv sync              # install deps (cairosvg, segno); Python 3.11
uv run qr.py         # interactive: prompts for URL, then output name (extension ignored)
```

`qr.py` writes `<name>.svg` and a 1000×1000 `<name>.png` to the current directory. For example, `survey-2027.*` and `get-involved.*` are committed outputs. `cairosvg` needs the system Cairo library.

There are no tests, linter or formatter configured. `main.py` is the unused `uv init` stub. The real entry point is `qr.py`.

## How `qr.py` works

- `segno` builds the QR code with error correction `"h"` (~30% recovery). This is what lets the logo cover the middle and the code still scan. If you raise `LOGO_FRACTION` or `PAD`, the covered area grows, so test that the result still scans.
- The SVG is rendered at `scale=1`, so the coordinate system is in **modules** (`n` = symbol width including the 4-module border). Logo position and size, and `PAD`, are all in module units. The `width`/`height` attributes are then set to `SIZE` pixels.
- The logo is embedded by parsing `logo.svg` with ElementTree and copying its children into a nested `<svg>` that reuses the logo's `viewBox`, placed on a white backing rect. Inkscape namespaces in `logo.svg` are carried through (they show up as `ns1`/`ns2` prefixes in the output). `logo.svg` must keep a valid `viewBox`.
- The PNG is rasterised from the same SVG bytes via `cairosvg`, so both outputs always match.
