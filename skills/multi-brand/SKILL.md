---
name: multi-brand
description: "Multi-brand and white-label theming in the FigCraft app with variable modes and extended collections: set up brand modes, populate values, apply a brand to screens, verify contrast and completeness in every brand, and build side-by-side brand comparisons. Use when: multi-brand/theme/white-label/brand switch + tokens/variables/design system in FigCraft."
---

# FigCraft App — Multi-Brand

Each brand is a mode (or an extended collection) with its own values; bound layers switch when the mode
changes. Load `figcraft-app:use` first.

## Skill Boundaries

- Brand modes and verification → this skill.
- Single-brand system → `figcraft-app:generate-library`. Tokens from DTCG → `figcraft-app:token-sync`.
- Health check → `figcraft-app:design-system-audit`.

## Key Concept

```
Collection "Brand"   modes: Acme | Globex | Initech
  color/accent       #0F766E | #7C3AED | #DC2626
  radius/control     8       | 999     | 4
```

Components bound to these switch per brand. Two ways to hold brands:
- **Modes in one collection** — simple; every brand lives in the file.
- **Extended collections** — a library publishes the base collection; each brand file
  `library.extendCollection {library, collection, name: "Acme"}` and overrides only what differs
  (`variable.set` on the inheriting variable; `variable.resetOverride` goes back). Library updates flow in;
  overrides stay. (Extending a collection of the same file, `variable.extendCollection`, needs a newer CLI.)

## Workflow

### 1. Checkpoint

`version.autosave` → `version.rename {index, name: "Before brands"}`.

### 2. Discover

`variable.list` — collections, modes, which collections already vary by brand.

### 3. Set up brand modes

- New: `variable.createCollection {name: "Brand", modes: ["Acme", "Globex"]}`.
- Add: `variable.addMode {collection, name: "Initech", from: "Acme"}` (copies Acme's values to start).
- Rename / reorder: `variable.renameMode {collection, mode, name}`, `variable.moveMode {collection, mode, to}`
  (index 0 is the default mode).

### 4. Populate values

One `batch` per brand of `variable.set {variable, mode: "Globex", value}`. Multi-mode DTCG files →
`figcraft-app:token-sync` with `--mode Acme=acme.json --mode Globex=globex.json`.

### 5. Apply a brand to screens

`variable.setMode {ids: [screen], collection: "Brand", mode: "Globex"}` (library collections:
`library.setVariableMode`). `mode: null` returns the frame to Auto (inherits).

### 6. Verify every brand

For each brand mode:
1. Contrast — text vs backgrounds ≥ 4.5:1 (rules and formula in `figcraft-app:design-lint` references).
2. Readability of text on brand-specific surfaces.
3. Components don't break (`screenshot` of a component sheet in each mode).
4. Completeness — every variable has a value in every mode (`variable.list` `values` per mode id).

### 7. Brand comparison

```json
{"label": "Brand comparison", "commands": [
  {"command": "edit.duplicate", "as": "g", "params": {"ids": [300]}},
  {"command": "variable.setMode", "params": {"ids": [{"$ref": "g", "field": "ids/0"}], "collection": "Brand", "mode": "Globex"}},
  {"command": "edit.duplicate", "as": "i", "params": {"ids": [300]}},
  {"command": "variable.setMode", "params": {"ids": [{"$ref": "i", "field": "ids/0"}], "collection": "Brand", "mode": "Initech"}}
]}
```

Then `screenshot` each copy, or `export {ids, format: "png", path}` for stakeholders. Rename copies
`<screen> — <brand>`.

## Architecture Patterns

- **Simple (2–3 brands):** only colour varies; spacing and radius shared.
- **Standard (3–5):** brand-specific primitives; semantic tokens alias them and vary by Light/Dark.
- **Advanced (5+ × Light/Dark):** primitives (brand) → semantic (theme) → component tokens (stable API);
  brand and theme as separate collections so each frame sets both modes.

## Cross-Brand Checklist

- [ ] Every variable has values for all brand modes
- [ ] WCAG AA contrast in every brand (and every theme)
- [ ] Icons and illustrations work with every brand palette
- [ ] Hover/active/disabled states work in every brand
- [ ] Logos and brand assets swap via an instance-swap property, not variants

## Safety

Never remove a brand mode (`variable.removeMode`) without explicit confirmation; re-check contrast after
colour changes; give new variables values in every mode.
