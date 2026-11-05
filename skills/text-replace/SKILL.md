---
name: text-replace
description: "Bulk replace text content in FigCraft app designs — localization, real data filling, copy updates, A/B variants, repeating a template frame per data row. Use when: replace/update/translate/localize + text/content/copy in FigCraft, or when filling designs with real data. Works in chunks with screenshots so nothing overflows."
---

# FigCraft App — Text Replace

Load `figcraft-app:use` first. Copy rules: `figcraft-app:ux-writing`.

## Skill Boundaries

- Replace existing text in bulk → this skill.
- New UI with text → `figcraft-app:create-ui`.
- Placeholder detection → `figcraft-app:design-review` / `figcraft-app:design-lint`.
- Styling text (font, size, colour) → `text.style {id, start, end, …}` or `set_properties` directly.

## Pick the Tool

| Job | Call |
|---|---|
| Same string everywhere ("Sign In" → "Sign in") | `run_command edit.findReplace {find, replace}` (all text layers; `layerNames: true` for names too) |
| One layer | `text.set {id, characters}` or `type_text {id, text}` |
| Many layers, different strings | `batch` of `text.set` steps, `"onError": "continue"` |
| Component text | `instance.setProperties {ids, properties: {Label: "…"}}` on instances — not their inner text |
| One frame per data row (cards, posts, carousel) | `data.fill {id, rows, gap?, dir?, formats?}` |
| Text must fit its box | `text.fit {ids, maxLines?, minSize?}`, or `{"fit": {"maxLines": 2}}` per field in `data.fill` |

## Workflow

### 1. Scan

`get_node {id: <frame>, depth: 8}` and collect every `TEXT` (`id`, `name`, `characters`, `width`,
`sizing.horizontal`, `textAutoResize`, `fontSize`) and every instance's `componentProperties`.
(`node.find {root, type: "TEXT"}` does it in one call on newer CLIs.)

Sort by role: headings, body, labels, placeholders, CTAs.

### 2. Chunk

- ≤ 30 text layers: one pass.
- More: chunks of 10–15, grouped by parent frame. Headings first, then body, then labels/CTAs.

### 3. Replace per chunk

```json
{"label": "Copy: Settings", "onError": "continue", "commands": [
  {"command": "text.set", "params": {"id": 41, "characters": "Notifications"}},
  {"command": "text.set", "params": {"id": 44, "characters": "Choose what we email you about."}},
  {"command": "instance.setProperties", "params": {"ids": [52], "properties": {"Label": "Save changes"}}}
]}
```

- Fixed-width text (`sizing.horizontal: "fixed"`, `textAutoResize: "none"`) needs similar or shorter copy.
- Localization grows 30–50% (EN → DE/FR) and CJK shrinks; plan widths, use `sizingH: "fill"` and
  `text.fit` where length can't be controlled.
- Missing glyphs or fonts: `text.missingFonts` after replacing CJK/Arabic/etc.

### 4. Verify per chunk

`screenshot {ids: [parentFrame], scale: 2}`. Check: no truncation or clipping, natural line breaks (no
single-word orphan lines in headings), layout didn't shift. Fix (copy, container width, `text.fit`)
before the next chunk.

### 5. Final QA

`screenshot` of every touched frame at `scale: 1`, and list the layers whose copy you couldn't verify.

## Data Filling With `data.fill`

Name the template's text layers after the data keys (`Title`, `Price`, `Badge`), then:

```json
{"command": "data.fill", "params": {"id": 80, "gap": 40, "rows": [
  {"name": "Card / Kyoto", "Title": "Kyoto in autumn", "Price": "$1,240", "Badge": {"visible": true}},
  {"name": "Card / Lisbon", "Title": {"text": "Lisbon long weekend", "fit": {"maxLines": 2}}, "Price": "$860", "Badge": {"visible": false}}
]}}
```

Returns `{ids, missing}` — `missing` lists keys no layer is named; fix names and rerun (`undo` first).
`dir` exports every copy as a file; `formats: [{name, width, height}]` makes each row in several sizes
(auto layout frames reflow).

## Screenshot Scale

| Purpose | `scale` |
|---|---|
| Whole page | 1 (or `maxSize` 1600) |
| Section | 2 |
| One text layer | 3 |
