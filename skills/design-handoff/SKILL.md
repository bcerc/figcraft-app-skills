---
name: design-handoff
description: "Prepare FigCraft app designs for developer handoff: annotations with pinned live properties and categories, measurements kept on the canvas, dev resource links, Ready for dev status, change comparison, exported assets and a spec summary. Use when: handoff/annotate/spec/redline + design/screen/component in FigCraft, or when preparing designs for developers."
---

# FigCraft App — Design Handoff

The app has a real Dev Mode: annotations, measurements, dev resources, handoff status and change
comparison are stored in the file. Load `figcraft-app:use` first.

## Skill Boundaries

- Annotate and prepare for handoff → this skill.
- Write the code → `figcraft-app:implement-design`.
- Link components to code → `figcraft-app:code-connect`.
- Quality review first → `figcraft-app:design-review`.

## Workflow

### 1. Connect

`inspect_ui {}`, `doc.list`. Targets: the frames the user names, or top-level frames of the page.

### 2. Inspect

Per key element:
- `inspect.properties {id}` — layout (position in its frame), auto layout, typography, fills, strokes,
  effects **with style and variable names** (`token`).
- `get_node {id, depth: 2}` — sizing, padding, gap, radius, `componentProperties`.
- `inspect.code {id, language: "css"}` when a value is easier read as CSS.

Collect: spacing (padding, gap), colours with tokens, typography (family, style, size, line height),
size and radius, layout (direction, sizing, alignment), component property values.

### 3. Annotate

Pinned properties show their **current** values (and token) in Dev Mode, so they never go stale:

```json
{"label": "Handoff annotations", "commands": [
  {"command": "annotation.add", "params": {"id": 120, "label": "Primary CTA. Full width on mobile, 320 max on desktop.",
    "properties": ["height", "padding", "cornerRadius", "fill"], "category": "Development"}},
  {"command": "annotation.add", "params": {"id": 133, "label": "Shows after 3 failed attempts; focus moves here.", "category": "Accessibility"}},
  {"command": "devMode.addMeasurement", "params": {"from": 120, "to": 118}},
  {"command": "devResource.add", "params": {"id": 120, "url": "https://github.com/acme/app/blob/main/src/ui/Button.tsx", "name": "Button.tsx"}}
]}
```

- Pinnable properties: `width`, `height`, `top`, `left`, `rotation`, `opacity`, `cornerRadius`, `direction`,
  `gap`, `padding`, `alignment`, `fontFamily`, `fontStyle`, `fontSize`, `lineHeight`, `letterSpacing`,
  `textAlign`, `fill`, `stroke`, `strokeWeight`, `effects`.
- Categories: Development, Interaction, Accessibility, Content by default; add with
  `annotation.addCategory {name, color}`.
- Read back with `annotation.list {page: "all"}`, `devMode.measurements {page}`, `devResource.list {id}`.

### 4. Mark status

`set_properties {ids: [frame], props: {devStatus: "readyForDev"}}` on top-level frames or sections.
Later edits turn them "Changed": `inspect.readyForDev {status: "changed"}` lists them,
`dev.compare {id}` shows what changed (`width 120 → 136`, `fill #FF0000 → #E03030`), and
`dev.resolveChange {ids, reason}` returns them to Ready for dev.

### 5. Export visual reference and assets

- `export {ids: [frame], format: "png", scale: 2, path: "<dir>/<name>.png"}` per screen.
- `inspect.assets {ids: [frame]}` lists icons (SVG), images (PNG) and layers with export settings;
  `run_command file.exportLayers {ids: [frame], assets: true, dir: "<dir>"}` writes them.

### 6. Spec summary

```markdown
# Handoff — <screen>   (status: Ready for dev)
## Layout   vertical, padding 24/24/48, gap 32; content max width 480
## Colours  bg/primary #FFFFFF · text/primary #111827 · accent/default #0F766E
## Type     Heading/H1 Inter Bold 28/120% · Body/md Inter Regular 16/150%
## Components  Button (Style=Primary, Size=lg, Label "Sign in") · Input ×2 (State=Default)
## Interactions  Sign in → Home (navigate); Forgot password → overlay
## Assets   icons/check.svg, img/hero@2x.png
## Notes    (annotations, by category)
```

### 7. Clean up (optional)

`annotation.remove {id}` (all of a layer's), `devMode.removeMeasurement {from}`, `devResource.remove {id}` —
only when the user asks.

## What to Annotate

Non-obvious spacing, colour tokens and resolved values, typography, interactive states (hover, focus,
disabled), responsive behaviour, and which component properties control what.
