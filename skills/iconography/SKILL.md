---
name: iconography
description: "Icon rules for the FigCraft app: getting real vector icons in (library icon components, an icon-set file, SVG import from the project's icon package, vector paths), ordering in auto layout (child index = visual order), sizing, spacing, colour, style consistency. Use when: icon/icons + create/place/add/order/position in FigCraft, or when icons appear in the wrong place or as text characters."
---

# FigCraft App — Iconography

The app has no icon search. Icons come from a component library, an SVG you supply, or a vector path.
Load `figcraft-app:use` first. General icon rules are in `figcraft-app:ui-ux-fundamentals`.

## Skill Boundaries

- Icon sourcing, placement, ordering, sizing, colour → this skill.
- Token-first choices with a library → `figcraft-app:design-guardian`.

## Getting Icons In (in this order)

1. **Icon components in the file or a library** — `component.list` / `library.list {assets: true}`; look for
   `Icon/…` names. Place with `instance.create {component, parent}` or `library.place` + `node.reparent`.
   Best: theme-aware, swappable via an instance-swap property.
2. **SVG from the project** — an icon package already on disk (`node_modules/lucide-static/icons/*.svg`,
   `@tabler/icons/icons/*.svg`, the repo's own `assets/icons/`). Ask before downloading a package.
   Import, then move it into place:

   ```json
   {"label": "Icon: search", "commands": [
     {"command": "file.import", "as": "ic", "params": {"path": "/abs/node_modules/lucide-static/icons/search.svg", "x": 0, "y": 0}},
     {"command": "node.reparent", "params": {"ids": [{"$ref": "ic"}], "parent": 120, "index": 0}},
     {"command": "node.set", "params": {"ids": [{"$ref": "ic"}], "props": {"name": "Icon/search", "width": 20, "height": 20}}}
   ]}
   ```

   `file.import` also takes `data` (base64 SVG) + `name` for markup you wrote. Import once, make it a
   component (`component.create`), then use instances everywhere.
3. **Vector path** — simple glyphs: `create_node {type: "vector", parent, path: "M4 12 L10 18 L20 6", width: 16, height: 16, props: {fill: "none", stroke: "#111827", strokeWeight: 2}}`.
4. **Starter set** — `file.newFromTemplate {template: "icon-set"}` opens a file of editable icon components
   (synthetic; copy what you need).

Never use text characters as icons (">", "…", "←", "×").

## Ordering — child index = visual order (CRITICAL)

In auto layout, index 0 is first in the flow (leftmost in horizontal, top in vertical). New children go
**last**. Place a leading icon with `node.reparent {ids, parent, index: 0}` or `create_node {parent, index: 0}`;
move one later with `node.reorder {id, index}`.

| Pattern | Children order | Icon index |
|---|---|---|
| Search input | [search icon, text] | 0 |
| Password input | [lock, text, eye] | lock 0, eye last |
| Nav / settings row | [icon, label, chevron/toggle] | icon 0, trailing last |
| Button, leading icon | [icon, label] | 0 |
| Button, trailing icon | [label, icon] | last |
| List item | [thumbnail, content, action] | thumbnail 0 |
| Tab bar item (vertical) | [icon, label] | 0 |
| Back navigation | [arrow-left, title] | 0 |

Plan every icon before building the frame; a search field without its icon is the most common miss.

## Sizing

| Context | Size | Gap to text |
|---|---|---|
| Inline body text | 16 | 4–6 |
| Input field | 20 | 8 |
| Navigation / toolbar | 24 | 8–12 |
| Button | 20 (match text) | 8 |
| Feature / empty state | 32–64 | 12–16 |
| Tab bar | 24 | 4 (vertical) |
| Avatar placeholder | 40–80 | — |

## Alignment and Targets

- Parent row: `crossAlign: "center"`.
- Icon container: a `frame` with `layout`, `mainAlign: "center"`, `crossAlign: "center"` (never a rectangle).
- Icon-only buttons: `minWidth: 44`, `minHeight: 44` around a 24 px icon.

## Colour

- Bind the icon's colour to a token: stroke icons `variable.bind {ids: [vectorIds], field: "stroke", variable}`,
  filled icons `field: "fill"`. An imported SVG is a frame of vectors — bind the vectors (from `get_node`),
  or recolour all at once with `selection.colors {ids: [icon]}` → `selection.bindColorVariable {targets, variable}`.
- Unbound icons don't follow Light/Dark modes.

## Consistency

One icon set and one style (outline, filled or duotone) per design; stroke weight matching the type weight;
no decorative icons without meaning.

## Pitfalls

| Pitfall | Prevention |
|---|---|
| Leading icon ended up after the text | `index: 0` on reparent/create |
| Text glyph as icon | import an SVG or use an icon component |
| Rectangle as container | `frame` |
| Imported SVG lands on the page, not in the row | always `node.reparent` in the same batch |
| Wrong size after import | set `width`/`height` (keeps proportions for vectors) |
| Colour stuck on dark backgrounds | bind stroke/fill to a variable |
| Mixed sets or styles | one package, one style |
| Tiny target | 44 × 44 min via `minWidth`/`minHeight` |
| Misaligned with text | parent `crossAlign: "center"` |
