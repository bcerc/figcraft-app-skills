---
name: design-lint
description: "Lint FigCraft app designs for compliance and fix the violations: token compliance (hardcoded colours, unstyled text), WCAG (contrast, target size, text size, line height), layout and structure (missing auto layout, empty containers, nesting depth, overflow, fill/hug conflicts, screen shells), naming and content (default names, placeholder text) and component health. Use when: lint/fix/check compliance/clean up + design/page/screen in FigCraft, or after creating UI. The app has no built-in linter: this skill reads the layer tree with get_node / selection.colors / inspect.properties and fixes with batch."
---

# FigCraft App — Design Lint

The FigCraft app has no lint engine. You are the linter: read the tree, apply the rules in
[references/rules.md](references/rules.md), fix in batches, verify. Load `figcraft-app:use` first.

## Skill Boundaries

- Rule checks and fixes → this skill.
- Human-style critique (hierarchy, composition, intent) → `figcraft-app:design-review`.
- Creating UI → `figcraft-app:create-ui`.

## Workflow — Quick Mode (default)

1. **Target** — the selection (`inspect_document {depth: 0}` → `selection`), the ids the user named, or
   every top-level frame on the page.
2. **Collect** (per target, few calls):
   - `get_node {id, depth: 6}` — structure, sizing, layout, text, `boundVariables`, `styles`, `componentProperties`.
     If `truncated`, read the children with further `get_node` calls.
   - `selection.colors {ids: [id]}` — every visible paint with its `style`/`variable` and `targets`.
   - `run_command variable.list` and `style.list` once — what tokens exist.
3. **Check** every rule in `references/rules.md` that applies. Keep a list:
   `{rule, severity, layer id, layer name, found, fix}`.
4. **Fix** what is auto-fixable, in one `batch` per target with `"onError": "continue"`, label `Lint fixes`.
5. **Verify** — re-run the checks on fixed layers and `screenshot {ids: [target]}`. A fix that changes the
   look in a way the user didn't ask for (e.g. a contrast fix) is listed, not silently applied, unless the
   user asked for "fix everything".
6. **Report** — counts by severity, what was fixed, what needs a human (with layer names and ids).

## Workflow — Dry Run

Steps 1–3 and 6 only. Say nothing was changed.

## Workflow — Granular

User picks categories (`token`, `wcag`, `layout`, `naming`, `component`) or rules; check and fix only those.

## Severity

| Level | Meaning | Action |
|---|---|---|
| error | breakage | always fix |
| unsafe | layout bugs visible to users | fix recommended |
| heuristic | best-practice violation | fix when possible |
| style | naming / cosmetic | fix optionally |

## Fix Toolkit

| Problem | Fix |
|---|---|
| Hardcoded colour where a variable exists | `selection.bindColorVariable {targets, variable}` (targets from `selection.colors`) |
| Hardcoded colour where a paint style exists | `selection.applyColorStyle {targets, style}` |
| Text without a text style | `style.apply {ids, style}` with the closest matching style |
| Missing auto layout | `layout.add {ids, direction}` or `layout.suggest {ids}` first |
| Off-scale spacing / radius | `node.set {ids, props: {gap, padding, cornerRadius}}` to the nearest scale value |
| Fill/hug paradox | `node.set` the child to `fixed` or the parent to `fixed` on that axis |
| Small target | `node.set {props: {minWidth: 44, minHeight: 44}}` (padding around the icon) |
| Default names | `object.rename {ids, name}` or `object.batchRename` |
| Placeholder text | `text.set {id, characters}` with real copy (ask for it when unknown) |
| Text overflow | `node.set {props: {sizingH: "fill"}}` or `text.fit {ids, maxLines}` |
| Empty container | `edit.delete {ids}` — only after confirming it isn't a slot or placeholder |
| Unbound component text | `component.addProperty {id, type: "text", name, layer}` |

Every mutating command is undoable; a whole fix batch is one `undo`.

## Integration

Run after `figcraft-app:design-review` to fix what it flagged, or alone as the closing step of
`figcraft-app:create-ui` / `figcraft-app:generate-design`.
