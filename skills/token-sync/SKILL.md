---
name: token-sync
description: "Sync DTCG (W3C design token) JSON into FigCraft app variables and styles, or export FigCraft variables back to DTCG / CSS / Tailwind / Dart. Use when: sync/push/import + tokens/DTCG + FigCraft, updating FigCraft variables from a token spec file, or exporting tokens for code. Converts with the bundled scripts/dtcg.py, then imports with variable.import (idempotent, multi-mode)."
---

# FigCraft App — Token Sync

Atomic tokens (colour, dimension, number, string, boolean) become **variables**; composite tokens
(typography, shadow) become **styles**. Load `figcraft-app:use` first.

Converter: `scripts/dtcg.py` in this skill's base directory (the path Claude Code shows when the skill
loads; below, `<skill-dir>`). Run it with `python3 -I` and an absolute path; `--help` lists the commands.

## Skill Boundaries

- DTCG → FigCraft (this skill), and FigCraft → DTCG/CSS/Tailwind/Dart (§Reverse).
- Compare only, no changes → `figcraft-app:spec-compare`.
- Whole design system (tokens + components) → `figcraft-app:generate-library`.
- Brand × theme modes → also `figcraft-app:multi-brand`.

## Workflow

### 1. Connect and get the files

`inspect_ui {}` / `doc.list`. Ask for the DTCG file path(s). **One DTCG file is one mode**
(`light.json`, `dark.json`); a single file is a single-mode collection. Ask for the target collection name
(default `Design Tokens`).

### 2. Convert and preview

```bash
python3 -I <skill-dir>/scripts/dtcg.py to-figcraft \
  --collection "Design Tokens" --mode Light=tokens/light.json --mode Dark=tokens/dark.json \
  -o <scratchpad>/vars.json
```

Writes `vars.json` (for `variable.import`) and `vars.styles.json` (composite tokens), and prints a report:
counts, skipped tokens (unknown `$type`, broken aliases) and variables it couldn't scope (`ALL_SCOPES`).
Show the user: total tokens, by type, skipped ones.

Conversion rules: `color.bg.primary` → `color/bg/primary`; `{color.blue.500}` → alias; `px` stays px,
`rem` × 16, `s` → ms; WEB code syntax `var(--color-bg-primary)`; scopes guessed from names (bg/surface →
fills, text/fg → text fill, border → stroke, space/gap → gap, radius → corner radius).

### 3. Check the current state

`run_command variable.export {format: "json", path: "<scratchpad>/before.json"}`, then

```bash
python3 -I <skill-dir>/scripts/dtcg.py diff \
  --collection "Design Tokens" --mode Light=tokens/light.json --mode Dark=tokens/dark.json <scratchpad>/before.json
```

Tell the user what will be created (`missingInFigcraft`), changed (`different`) and left alone (`inSync`,
`missingInDtcg` — the import never deletes). ⛔ Wait for a go-ahead when anything changes.

### 4. Import

`run_command variable.import {variables: "<scratchpad>/vars.json"}` → `{collections, variables, updated, warnings}`.
Collections join the file's collection of the same name, values by mode name; new modes and variables are
added. Running it twice changes nothing the second time.

Then fix scopes the converter couldn't guess: primitives → `variable.update {variable, scopes: []}` (hidden
from pickers), others → the right scope list. Add iOS/Android code names if the project uses them:
`variable.update {variable, codeSyntax: {iOS, ANDROID}}`.

### 5. Composite tokens → styles

For each entry of `vars.styles.json` (default mode values):

| `type` | Call |
|---|---|
| typography | `style.create {type: "text", name, value: {fontFamily, fontStyle, fontSize, lineHeight: "150%", letterSpacing}}` (`fontWeight` 400 → `fontStyle` "Regular", 500 "Medium", 600 "Semi Bold", 700 "Bold"; check `text.fonts {family}`) |
| shadow | `style.create {type: "effect", name, value: [{type: "dropShadow", color, offset: [x, y], radius: blur, spread}]}` |

An existing style of that name → `style.update {style, value}` instead. Bind a style's field to a variable
where the token aliases one: `style.bind {style, field: "fontSize", variable}`.
Per-mode composite values can't live in a style; tell the user which ones differ by mode.

### 6. Report and verify

Report created / updated / unchanged / skipped. Verify with `variable.list` and
`variable.export {format: "css"}`. Run `figcraft-app:design-lint` (token rules) on screens that use them.

## Reverse — FigCraft → Code

| Want | Call |
|---|---|
| DTCG | `variable.export {format: "json", path}` then `dtcg.py from-figcraft <path> [--collection]` (modes under `$extensions."figcraft.modes"`) |
| CSS custom properties | `variable.export {format: "css", path}` (default mode on `:root`, others on `[data-<collection>="<mode>"]`) |
| Tailwind v4 theme | `variable.export {format: "tailwind", path}` |
| Flutter | `variable.export {format: "dart", path}` |

## Key Points

- Atomic → variables, composite → styles (variables hold no compound values).
- The import is idempotent and additive; deletions are a separate, confirmed step (`variable.delete`).
- Aliases are kept as aliases, so semantic tokens follow their primitives.
