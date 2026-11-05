# FigCraft App — `props` Cheat Sheet

`create_node {props}`, `set_properties {ids, props}` and `node.set {ids, props}` take the same keys.
Full list: `list_commands {filter: "node.set"}`. Read back what a layer has with `get_node`.

## Geometry and Appearance

| Key | Values |
|---|---|
| `name`, `visible`, `locked`, `opacity` (0–1), `rotation` (deg) | |
| `x`, `y`, `width`, `height` | `x`/`y` relative to the parent frame |
| `fill` / `stroke` | `"#RRGGBB[AA]"`, `"none"` or `null` |
| `fills` / `strokes` | list, bottom first: `[{"type": "solid", "color": "#FFF"}, {"type": "linearGradient", "stops": ["#7048E8", "#1098AD"]}]` |
| `strokeWeight`, `strokeAlign` (`inside`/`center`/`outside`), `strokeSides` `[t,r,b,l]`, `dashes` | |
| `cornerRadius` | `n` or `[tl, tr, br, bl]`; `cornerSmoothing` 0–1 |
| `effects` | `[{"type": "dropShadow", "color": "#00000026", "offset": [0, 4], "radius": 16, "spread": 0}]`; also `innerShadow`, `layerBlur`, `backgroundBlur`, `noise`, `texture`, `glass` |
| `clip` | frames clip their children (default true for new frames) |
| `blend` | `"multiply"`, `"pass through"`, … |
| `constraints` | `{horizontal, vertical}` for children outside auto layout |

## Style and Variable Links

| Key | Effect |
|---|---|
| `fillStyle`, `strokeStyle`, `textStyle`, `effectStyle`, `gridStyle` | link a style by id or name (`"Body/md"`) |
| `{"fill": {"$var": "Theme/surface"}}` | bind a colour variable at creation (newer CLIs only; else `variable.bind`) |

A style link set in the same call wins over the values it sets. Editing a styled value later unlinks it.
Bind non-paint fields with `variable.bind {ids, field, variable}`: `fill`, `stroke`, `fills/<i>/color`,
`effects/<i>/radius`, `layoutGrids/<i>/gutter`, `componentProperties/<name>`, and number fields such as
`width`, `cornerRadius`, `gap`, `padding*` (check `list_commands {filter: "variable.bind"}`).

## Auto Layout (frames and components)

| Key | Values |
|---|---|
| `layout` | `"horizontal"`, `"vertical"`, `"grid"`, `null` |
| `gap`, `crossGap` (wrapped rows) | px |
| `padding` | `n` or `[t, r, b, l]`; or `paddingTop`/`Right`/`Bottom`/`Left` |
| `mainAlign` | `min`, `center`, `max`, `spaceBetween`, `spaceAround`, `spaceEvenly` |
| `crossAlign` | `min`, `center`, `max`, `baseline` (horizontal) |
| `wrap`, `contentAlign` | wrapping rows / columns |
| `sizingH`, `sizingV` | `fixed`, `hug`, `fill` |
| `minWidth`, `maxWidth`, `minHeight`, `maxHeight` | px, `null` removes |
| `absolute` | `true` takes a child out of the flow |
| `strokesIncluded`, `reverseZ` | |
| Grid | `gridColumns`, `gridRows`, `columnTracks`/`rowTracks` (`[120, "1fr", "auto"]`), `columnGap`/`rowGap`; children `gridColumn`, `gridRow`, `gridColumnSpan`, `gridRowSpan`, `gridAlignH`, `gridAlignV` |

Rules: a child can't `fill` an axis its parent `hug`s. Text inside a fixed or fill-width container that
should wrap needs `sizingH: "fill"` (or a fixed `width`). A screen frame is `fixed`/`fixed`.

## Text

`characters`, `fontFamily`, `fontStyle` (`"Regular"`, `"Medium"`, `"Semi Bold"`, `"Bold"` — check
`text.fonts {family}`), `fontSize`, `lineHeight` (`"auto"`, px, `"150%"`), `letterSpacing` (px or `"2%"`),
`textAlign`, `textAlignVertical`, `textAutoResize` (`widthAndHeight`, `height`, `none`, `truncate`),
`textCase`, `textDecoration`, `paragraphSpacing`, `listStyle`, `maxLines`, `features` (`{"tnum": true}`),
`fontVariations` (`{"wght": 550}`).

Character ranges: `text.style {id, start, end, fontStyle, textFills, …}`. Replace content:
`text.set {id, characters}` or `type_text {id, text}`.

## Other

`pluginData {key: value}` (strings, read back by `get_node`), `devStatus` (`none`, `readyForDev`,
`completed`; top-level frames and sections), `description` (components), `interactions`, `overflow`,
`isMask`, `maskType`, `path` (vector SVG path data), `pointCount`, `innerRadius`, `arcStart`, `arcSweep`.

## Commands That Pair With Props

| Need | Command |
|---|---|
| Move into a parent / reorder | `node.reparent {ids, parent, index?}`, `node.reorder {id, index}` (index counts bottom first; in auto layout, first in flow) |
| Duplicate | `edit.duplicate {ids, map?: true}` → `{ids, map}` |
| Delete | `edit.delete {ids}` |
| Group / frame | `object.group`, `object.convertToFrame`, `object.wrapInSection {ids, name}` |
| Auto layout on existing layers | `layout.add {ids, direction}`, `layout.suggest {ids}` |
| Align / distribute / space | `align.left`…, `distribute.horizontal`, `arrange.spacing {ids, horizontal?, vertical?}` |
| Fit text to its box | `text.fit {ids, maxLines?, minSize?}` |
| Repeat a frame per data row | `data.fill {id, rows, gap?, dir?}` |
| Rename many | `object.batchRename {ids, find?, replace?, name?, regex?}` |
