# SciencePlots contribution staging

Candidate styles to upstream to [SciencePlots](https://github.com/garrettj403/SciencePlots),
extracted from this repo's `paper.mplstyle` / `slides.mplstyle` / `sizes/` and
rewritten in SciencePlots' file conventions. Preview them stacked on the real
base styles with:

```bash
python preview.py   # renders into preview/, prints size + fonttype checks
```

## The three proposed additions

| Files | What they add | SciencePlots today |
|---|---|---|
| `sizes/*.mplstyle` + `slides.mplstyle` + `fontsize.mplstyle` | Composable figure sizes: double-column grid heights named by grid shape (`1x1`/`1x2`/`1x3`/`2x3`, with a `-square` variant each; `height = width x panel_aspect x rows/cols`, golden + square) and a slide-scale style with paste-into-PowerPoint-at-true-size export (`figure.dpi` 96, `savefig.dpi` 300, `savefig.bbox` standard). Every size patch carries `savefig.bbox: standard` + constrained layout so the saved file is exactly `figsize` even though the base `science` style sets `tight`. Plus `fontsize.mplstyle`, a standalone journal-scale (~5-7 pt) type hierarchy to pair with the print size patches — `science` sets no font sizes, so figures otherwise keep matplotlib's 10 pt default. | One `figure.figsize` per journal style, `savefig.bbox: tight` (already commented out in their `nature.mplstyle` for this very reason); `notebook` is the only non-print medium; no style sets a font-size hierarchy. |
| `editable-text.mplstyle` | TrueType (Type 42) fonts in PDF/PS + text-as-text SVG, so journal production can edit labels. Only affects the mathtext path (`no-latex`). | Not set anywhere — PDFs embed Type 3. |
| `short-legend.mplstyle` | Frameless legend with each label coloured like its line. | Only `legend.frameon: False`. |

Square size patches need `ax.set_box_aspect(1)` on each panel — without it
constrained layout shrinks the panels instead of filling the width.

## Suggested PR split

1. Open an issue first (their README asks for one before any new style) sketching all three.
2. PR 1: `sizes/` + docs table with the height rule.
3. PR 2: `slides.mplstyle` (+ the three widths `slides-full`/`slides-half`/`slides-third`).
4. PR 3: `editable-text` + `short-legend` (small, uncontroversial).

Naming note: SciencePlots registers styles flat by file stem, so the final
names must not collide with existing ones (`1x1`, `2x3`, `slides`, ... are
free as of 2026-06). The grid names carry no width token because every grid
patch here is double-column width — the comment in each file states the
180 mm width and the height rule.
