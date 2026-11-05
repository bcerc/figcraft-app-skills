---
name: design-review
description: "Review existing FigCraft app designs against design quality rules and output a structured violation report with fixes. Use when: review/audit/check/critique/analyze/inspect/diagnose + design/screen/page/component in FigCraft, or to analyze why a design looks off. Reads the layer tree and screenshots; then hands the fixes to figcraft-app:design-lint."
---

# FigCraft App — Design Review

A structured critique with concrete fixes. Forms the loop
`figcraft-app:create-ui` → **review** → `figcraft-app:design-lint`. Load `figcraft-app:use` first.

## Skill Boundaries

- Critique and report → this skill.
- Rule checks and auto-fixes → `figcraft-app:design-lint`.
- Creating UI → `figcraft-app:create-ui`. Code from a design → `figcraft-app:implement-design`.
- Accessibility-only audit → this skill with the Accessibility category, or the `design:accessibility-review` skill.

## Workflow (run every step without stopping)

### 1. Connect

`inspect_ui {}`; on a connection error tell the user to start the app with
`open -a FigCraft --args --control 7979` and stop. `doc.list` → pin the `document`.

### 2. Targets

The selection, the ids the user named, or the page's top-level frames (`inspect_document {depth: 1}`).

### 3. Read

Per target, in this order and no more than needed:

1. `screenshot {ids: [id], maxSize: 1400}` — look first.
2. `get_node {id, depth: 5}` — structure, sizing, text, bindings.
3. `selection.colors {ids: [id]}` — palette and which colours are tokens.
4. `variable.list`, `style.list`, `component.list` once — what the system offers (decides mode below).
5. Only for specific suspects: `inspect.properties {id}` (resolved tokens), `screenshot` of one child at `scale: 2`.

Don't `get_node` each child separately when one deeper call covers them.

### 4. Apply Rules

Mode: the file has styles/variables/components or an enabled library → **library mode**
(`figcraft-app:design-guardian`); otherwise **creator mode** (`figcraft-app:design-creator`). Always
`figcraft-app:ui-ux-fundamentals`.

Library mode focus:
- Colours/fonts bound to tokens? Hardcoded values where tokens exist?
- Clear hierarchy and focal point; intentional composition (no uniform grids of equal cards)?
- Spacing from tokens or the 4 px scale; consistent rhythm?
- Real content, no placeholders? Icons one style? ≤ 3 shadow levels?
- Instances used where components exist (`mainComponentName` present)?
- Contrast ≥ 4.5:1 in every mode, targets ≥ 44?

Creator mode focus:
- A clear design intent, not defaults (Inter + blue + centred without reason)?
- ≤ 5 colours, 60% dominant, one accent; fonts chosen on purpose?
- Rhythmic spacing on a base unit; focal point; real content; consistent icons and shadows; accessibility.

Categories for focused reviews: `color`, `typography`, `spacing`, `layout`, `composition`, `content`,
`accessibility`, `buttons`, `inputs` — use the matching sections of `figcraft-app:ui-ux-fundamentals`.

### 5. Report

Per violation:

```
[severity] <rule or category> — <layer name> (id <n>)
  Found:  <what is there, with values>
  Why:    <the rule it breaks>
  Fix:    <exact change: prop/command and value>
```

### 6. Summarize

Counts by severity and category, the three changes with the biggest effect, and an overall verdict.

### 7. Fix

Offer to apply the fixes through `figcraft-app:design-lint` (same targets). Leave subjective changes
(composition, copy tone) to the user.

## Optional: Put the Review on the Canvas

With the user's OK, pin findings where they are: `comment.add {x, y, text, anchor: <layer id>}`
(the app signs it as the agent). They then show in the app's Comments panel and can be worked
through with the server's `fix_comments` prompt.
