---
name: design-system-audit
description: "Audit the health of a FigCraft app design system: inventory, component structure, token binding rate, variable quality (scopes, code syntax, descriptions, aliasing, orphans), styles, naming, library usage — with a weighted health score. Use when: audit/health check/coverage + design system/library/tokens in FigCraft, or before publishing a library."
---

# FigCraft App — Design System Audit

Load `figcraft-app:use` first. Read-only until the user approves fixes.

## Skill Boundaries

- Whole-system health → this skill.
- New system → `figcraft-app:generate-library`. Single component → `figcraft-app:component-docs`.
- Lint a page → `figcraft-app:design-lint`. Tokens vs a spec → `figcraft-app:spec-compare`.

## Workflow

### 1. Connect

`inspect_ui {}`, `doc.list`.

### 2. Inventory

One call each: `page.list`, `component.list`, `variable.list`, `style.list`, `library.list {assets: true}`.
Summarise: pages, components and sets (per page), collections with mode counts, variables by type, styles
by type, enabled libraries and pending updates (`library.updates`).

### 3. Component health

Run the `figcraft-app:component-docs` audit checks for each component: missing descriptions, unexposed
text, empty, single-variant sets, unbound properties, `conflicts`, default layer names.

### 4. Token coverage

Per component (`get_node {id, depth: 6}` + `selection.colors {ids: [id]}`):
- fills and strokes bound (`boundVariables`, or `variable` in `selection.colors`) or styled (`styles.fill`)
- gap, padding, radius bound (`boundVariables` keys)
- text using text styles (`styles.text`)
- shadows using effect styles (`styles.effect`)

Binding rate = bound bindable values ÷ bindable values × 100%.

### 5. Variable quality

From `variable.list` (all fields in one call — don't fetch variables one by one):
- ⚠️ `scopes` is `ALL_SCOPES` (or null)
- ⚠️ no `codeSyntax`
- ⚠️ empty `description`
- ⚠️ semantic variable holding a raw value that equals a primitive (should be `{alias}`)
- ⚠️ orphan: bound nowhere (search `boundVariables` across pages; `inspect_document {allPages: true, depth}`)
- ⚠️ mixed naming (`bgPrimary` vs `bg/primary` vs `bg-primary`)
- ⚠️ a mode with missing values

Bulk fix after approval: one `batch` of `variable.update {variable, scopes, codeSyntax, description}` and
`variable.set {variable, mode, value: {alias}}` steps.

### 6. Naming

Default names (`Frame 3`, `Rectangle`), inconsistent casing, duplicate component names, pages without
dividers between sections. Fix with `object.batchRename` after approval.

### 7. Library usage (team libraries)

`library.usage {library?, days: 30}` → instances, detaches, insertions per component and file. High
detach counts point at components that don't fit real use.

### 8. Report

```markdown
# Design System Audit — <file>     Health 7.4 / 10
Inventory: 4 pages · 18 sets (126 variants) · 3 collections (Light/Dark) · 142 variables · 24 styles
Components: 5 missing descriptions · 2 unexposed text · 1 single-variant set
Tokens: binding rate 81% (fills 96%, strokes 70%, spacing 62%, radius 88%)
Variables: 31 ALL_SCOPES · 54 no code syntax · 12 raw values duplicating primitives · 7 orphans
Naming: 23 default names
Top fixes: 1) scopes + code syntax (batch)  2) alias duplicated semantics  3) bind button padding
```

## Health Score

| Criterion | Weight |
|---|---|
| Component descriptions | 15% |
| Token binding rate | 25% |
| Variable scopes set | 15% |
| Code syntax set | 10% |
| No default names | 10% |
| No placeholder text | 10% |
| Text styles applied | 10% |
| No empty containers | 5% |

Score each as a percentage, weight, ÷ 10. 8–10 healthy · 5–7 needs attention · < 5 significant gaps.
