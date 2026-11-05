---
name: generate-library
description: "Build or update a design system in the FigCraft app: variable collections with modes (Light/Dark), primitives and semantic aliases with scopes and code syntax, text/effect/paint styles, components with variants and properties, documentation pages, then publish it as a library. Use when creating the system itself, not when using it. Multi-phase with user checkpoints. Do NOT use for building screens (figcraft-app:create-ui / figcraft-app:generate-design)."
---

# FigCraft App — Design System Builder

Load `figcraft-app:use` first. Design direction: `figcraft-app:ui-ux-fundamentals` + `figcraft-app:design-guardian`.

## Skill Boundaries

- Build a design system (variables, styles, components, docs, publish) → this skill.
- Screens → `figcraft-app:create-ui` / `figcraft-app:generate-design`.
- Health check of an existing system → `figcraft-app:design-system-audit`.
- Moving between system versions → `figcraft-app:migration-assistant`.
- Tokens from a DTCG file → `figcraft-app:token-sync`.

## 1. The One Rule

**Never one-shot it.** Many small calls across phases, with a user checkpoint between phases. A shortcut
here costs hours of rework.

Shortcut worth taking: `file.newFromTemplate {template: "design-system"}` builds an editable starter
(colour and text styles, Light/Dark variables, components) in under a second. Offer it when the user has no
existing conventions.

## 2. Phases

```
0 Discovery  →  checkpoint  →  1 Foundations  →  checkpoint  →  2 File structure  →  checkpoint
→  3 Components (one at a time, checkpoint each)  →  4 QA + publish  →  sign-off
```

## 3. Tools Per Phase

### Phase 0 — Discovery

| Task | Call |
|---|---|
| Files, pages | `doc.list`, `page.list`, `inspect_document {depth: 1}` |
| Variables, collections, modes | `variable.list` |
| Styles | `style.list` |
| Components | `component.list`, `component.properties {id}` |
| Libraries already used | `library.list {assets: true}` |
| Tokens in code | read the repo's CSS variables / Tailwind theme / token JSON |

Output: token list, component list, gap analysis. ⛔ "Here's my plan. Approve before I create anything?"

### Phase 1 — Foundations

| Task | Call |
|---|---|
| Collection with modes | `variable.createCollection {name: "Color", modes: ["Light", "Dark"]}` |
| Primitive | `variable.create {collection: "Primitives", name: "blue/500", type: "color", value: "#2563EB"}` |
| Semantic per mode | `variable.create {collection: "Color", name: "bg/primary", type: "color", values: {Light: "#FFFFFF", Dark: "#0B0F19"}}` |
| Alias to a primitive | `variable.set {variable: "bg/accent", mode: "Light", value: {alias: "blue/500"}}` |
| Scopes + code syntax | `variable.update {variable, scopes: ["FRAME_FILL", "SHAPE_FILL"], codeSyntax: {WEB: "var(--bg-primary)", iOS: "bgPrimary", ANDROID: "bg_primary"}}` |
| Number tokens | `variable.create {collection: "Spacing", name: "space/16", type: "number", value: 16}` |
| Bulk import | `variable.import {variables: <local variables JSON>}` (same shape `variable.export {format: "json"}` writes) |
| Text style | `style.create {type: "text", name: "Heading/H1", value: {fontFamily, fontStyle, fontSize, lineHeight: "120%", letterSpacing: "-1%"}}` |
| Effect style | `style.create {type: "effect", name: "Elevation/1", value: [{type: "dropShadow", color: "#0000001A", offset: [0, 2], radius: 8}]}` |
| Bind a variable inside a style | `style.bind {style, field: "fills/0/color", variable}` |

Do the creates in `batch`es of ~20–50 steps. Verify with `variable.list` and
`variable.export {format: "css"}` (readable summary). ⛔ checkpoint: "N collections, M variables, K modes,
these styles. Review before file structure?"

### Phase 2 — File Structure

`page.add {name: "Cover"}`, `"Foundations"`, one page per component family (dividers: names starting with `-`).
Foundations page: swatches bound to the colour variables, a type specimen using the text styles, a spacing
scale. Screenshot → ⛔ checkpoint.

### Phase 3 — Components (one at a time)

| Task | Call |
|---|---|
| Base variant | `batch` of `node.create` (frame + children), all paints bound with `variable.bind`, text via `textStyle` |
| Make component | `component.create {ids: [frame]}` |
| Properties | `component.addProperty {id, name, type: text|boolean|instanceSwap|variant|slot, default?, layer?}` |
| Wire a layer later | `component.bindProperty {layer, property, field: characters|visible|mainComponent|slot}` |
| Add variant | `component.addVariant {id, property, value}` (duplicates; first call makes the set) |
| Combine built ones | `component.combineVariants {ids}` |
| Edit/reorder props | `component.editProperty {id, name, newName?, default?, index?}` |
| Slot | `component.makeSlot {id: <frame in main>, preferred?: [ids]}` |
| Expose nested instance | `component.exposeInstance {id}` |
| Description | `set_properties {ids: [set], props: {description: "…"}}` |
| Keep helpers private | name with `.` or `_` prefix, or `component.hideWhenPublishing {ids}` |
| Try combinations | `component.playground {id, properties}` (nothing changes in the file) |
| Code links | `figcraft-app:code-connect` |

After each component: `component.properties {id: set}` (`conflicts` must be empty), `screenshot {ids: [set]}`,
⛔ "Here's Button with N variants. Correct?"

### Phase 4 — QA and Publish

1. Run `figcraft-app:design-system-audit` and fix findings.
2. `library.publish {description: "v1.0 — initial"}` then `save_file` (other files see the version after save).
3. Team library on a server: `library.publishToServer {server: <edit link>}`.
4. ⛔ final checkpoint with per-page screenshots.

## 4. Critical Rules

1. **Variables before components.** No token, no component.
2. **Inspect before creating**; match existing naming.
3. **One page per component family.**
4. **Bind every visual value** — fills, strokes, gap, padding, radius — to variables.
5. **Scopes on every variable** (never `ALL_SCOPES`): backgrounds `FRAME_FILL, SHAPE_FILL`, text `TEXT_FILL`,
   borders `STROKE_COLOR`, spacing `GAP`, radii `CORNER_RADIUS`; primitives `[]` (hidden from pickers).
   Confirm the scope ids your CLI accepts with `list_commands {filter: "variable.update"}`.
6. **Code syntax on every variable**: WEB with `var(--…)`, iOS/Android plain names.
7. **Semantics alias primitives** (`{alias}`) — never duplicate raw values.
8. **Instance swap for icons, slots for free content** — never a variant per icon; ≤ 30 variants per set.
9. **Verify after every create** (`get_node`, `screenshot`).
10. **Never invent ids** — only ids from results.
11. **Name the next phase explicitly** at each checkpoint; never build on rejected work.
12. **Cleanup on failure**: a failed batch left nothing; for partial multi-batch builds, list what exists
    (`variable.list`, `component.list`) and delete orphans (`variable.delete`, `edit.delete`) after asking.

## 5. State Ledger (10+ components)

Write a ledger of created ids to the scratchpad at each phase boundary (collections, variables by name,
styles, component sets, pages) and re-read it at the start of each turn. To resume, rebuild it from
`variable.list`, `style.list`, `component.list`, `page.list`. Before creating anything, check it doesn't
already exist by name.

## 6. Naming

- Variables: slash paths — `blue/500`, `bg/primary`, `text/secondary`, `space/16`, `radius/md`.
- Styles: `Heading/H1`, `Body/md`, `Elevation/1`.
- Components: `Button`, `Input`, `Card`; variants `Property=Value, Property=Value`
  (`Size=md, Style=Primary, State=Default`).

## 7. Token Architecture

| Size | Pattern |
|---|---|
| < 50 tokens | one collection, Light/Dark |
| 50–200 | Primitives (1 mode) + Color semantic (Light/Dark) + Spacing (1 mode) |
| 200+ / multi-brand | several semantic collections, brand × theme modes; see `figcraft-app:multi-brand` |

## 8. Reuse Decision (existing library components)

- **Reuse** when the property API, token model and naming match.
- **Rebuild** when the API or token model is incompatible, or the library can't be edited.
- **Wrap** when the look matches but the API doesn't: a new component with the library instance nested
  inside and a clean API (`component.exposeInstance` for nested properties).
