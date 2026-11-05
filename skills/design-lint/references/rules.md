# Lint Rules — FigCraft App

Each rule says what to read in the `get_node` JSON (keys as the app reports them: `type`, `name`,
`width`, `height`, `absoluteBounds`, `fills`, `strokes`, `effects`, `cornerRadius`, `layout {mode, gap,
padding, mainAlign, crossAlign}`, `sizing {horizontal, vertical}`, `characters`, `fontSize`,
`lineHeight`, `fontFamily`, `fontStyle`, `styles {fill, stroke, effect, text, grid}`, `boundVariables`,
`componentProperties`, `mainComponentName`, `visible`, `childCount`) and how to fix it.

"Screen" = a top-level frame named `Screen / …` or sized like a `frame.presets` device.
"Interactive" = a layer named Button/CTA/Link/Input/Tab/Toggle…, an instance of such a component, or a
layer with `interactions`.

## Token Compliance (6)

| Rule | Sev | Check | Fix |
|---|---|---|---|
| `spec-color` | error | Spec mode (a token file or `variable.list` is the reference): a solid colour in `selection.colors` that equals no token value | bind the nearest token: `selection.bindColorVariable` (ΔE / hex distance; tell the user when the nearest is far) |
| `spec-typography` | error | Text whose family/size/weight/line height matches no text style | `style.apply {ids, style}` with the nearest style |
| `spec-border-radius` | error | `cornerRadius` not in the radius tokens (number variables scoped `CORNER_RADIUS`, or the scale 0/4/8/12/16/24/full) | `node.set {cornerRadius}` to nearest, then `variable.bind {field: "cornerRadius"}` when a token exists |
| `hardcoded-token` | heuristic | `selection.colors` entry with `variable: null` and `style: null` while colour variables or paint styles exist | `selection.bindColorVariable` / `selection.applyColorStyle` |
| `no-text-style` | heuristic | TEXT with `styles.text` null while text styles exist | `style.apply` |
| `foreign-style` | heuristic | A style or variable copied from a library other than the one the file is meant to use (`library.list` shows which) | `library.swap {from, to}` or re-apply the right library's style |

## WCAG Accessibility (5)

| Rule | Sev | Check | Fix |
|---|---|---|---|
| `wcag-contrast` | unsafe | Text fill vs the nearest ancestor's solid fill: ratio < 4.5 (< 3 for ≥ 18 px, or ≥ 14 px bold) | report; suggest the nearest token that passes. Change only when asked |
| `wcag-target-size` | heuristic | Interactive layer < 44×44 (hard minimum 24×24) | `minWidth`/`minHeight: 44` with padding |
| `wcag-text-size` | heuristic | `fontSize` < 12 desktop, < 14 mobile body (10 absolute floor for captions) | raise to the minimum |
| `wcag-line-height` | heuristic | `lineHeight` in px < `fontSize`, or percent < 100% | `lineHeight: "auto"` or ≥ 120% (body 140–160%) |
| `wcag-non-text-contrast` | heuristic | Button/input surface (fill or stroke) vs adjacent background < 3:1 | report with suggested colour |

Contrast: for sRGB `c` in 0–1, `L = 0.2126 R + 0.7152 G + 0.0722 B` with each channel
`c ≤ 0.04045 ? c/12.92 : ((c+0.055)/1.055)^2.4`; ratio = `(L1+0.05)/(L2+0.05)`, L1 the lighter.
Translucent fills: blend over the parent's colour first. With variable modes, check every mode
(`variable.list` values per mode).

## Layout & Structure (27)

| Rule | Sev | Check | Fix |
|---|---|---|---|
| `screen-shell-invalid` | error | Screen without `layout.mode: "vertical"` or not `fixed`/`fixed` | `node.set {layout: "vertical", sizingH: "fixed", sizingV: "fixed"}` |
| `root-misclassified-interactive` | error | A screen named or built like a button/input (Button in its name, single text child, interactions on the root) | report; rename / restructure |
| `nested-interactive-shell` | error | Interactive layer inside another interactive layer (button in a clickable card) | report; unwrap |
| `no-autolayout` | heuristic | FRAME with ≥ 2 children and no `layout` whose children don't overlap on purpose | `layout.suggest {ids}` → `layout.add {ids, direction}` |
| `empty-container` | verbose | FRAME/GROUP with `childCount` 0 (or only invisible children), not a slot, not a placeholder with a fill | report; delete after confirmation |
| `spacer-frame` | style | Empty frame with no fill/stroke between siblings in auto layout | delete it and set the parent `gap` |
| `max-nesting-depth` | verbose | Depth > 6 below the screen | report; flatten wrappers that only hold one child |
| `button-solid-structure` | heuristic | Filled button not auto layout, padding < 1/3 height horizontally, or height < 44 | `layout: "horizontal"`, `mainAlign/crossAlign: "center"`, padding, `minHeight: 44` |
| `button-outline-structure` | heuristic | Outline button without a visible stroke, auto layout, padding or height | add stroke, layout, padding, `minHeight` |
| `button-ghost-structure` | heuristic | Transparent button without padding | add padding to reach the target size |
| `button-text-structure` | heuristic | Text button whose tap area < 44 tall | wrap in an auto layout frame with vertical padding |
| `button-icon-structure` | heuristic | Icon-only button < 24×24 (44 recommended) or no descriptive name | `minWidth/minHeight`, rename (`Button / Close`) |
| `link-standalone-structure` | heuristic | Standalone link text with line box < 24 tall on mobile | `lineHeight` / padding wrapper |
| `text-overflow` | heuristic | TEXT `absoluteBounds` past its clipping ancestor, or fixed-width text with `textAutoResize: "none"` cut off | `sizingH: "fill"`, `textAutoResize: "height"`, or `text.fit` |
| `form-consistency` | heuristic | Form children (inputs, buttons) with different widths | `sizingH: "fill"` on each |
| `cta-width-inconsistent` | heuristic | Primary CTA in a form noticeably narrower than the fields | `sizingH: "fill"` |
| `overflow-parent` | unsafe | Child `absoluteBounds` outside the parent's bounds (not `absolute`, not a shadow) | resize parent to hug, or child to fill |
| `unbounded-hug` | unsafe | Parent `sizing` hug on an axis where a child is `fill` (the app turns one fixed; check what it did) | make the parent `fixed` or the child `hug` |
| `section-spacing-collapse` | heuristic | Vertical stack of sections with `gap` < 24 | raise `gap` to 32–64 |
| `screen-bottom-overflow` | unsafe | Content bottom past the screen's height (unless the screen scrolls on purpose) | report; trim or allow scroll (`overflow`) |
| `social-row-cramped` | heuristic | Row of social sign-in buttons whose children shrink or clip | stack vertically or widen |
| `nav-overcrowded` | heuristic | Nav row with > 7 items or items narrower than their text | reduce items / move to a menu |
| `stats-row-cramped` | heuristic | Metric cards narrower than ~120 px each | wrap (`wrap: true`) or use a grid |
| `input-field-structure` | heuristic | Input not an auto layout frame with stroke, radius, padding and a text child | rebuild with those |
| `mobile-dimensions` | style | Mobile screen not 402×874 (iOS) / 412×915 (Android) or another `frame.presets` device size | `node.set {width, height}` |
| `elevation-consistency` | verbose | Siblings mixing shadowed and flat cards | report; pick one |
| `elevation-hierarchy` | heuristic | Child shadow radius/offset larger than its parent's | report |

## Naming & Content (2)

| Rule | Sev | Check | Fix |
|---|---|---|---|
| `default-name` | verbose | `name` like `Frame 12`, `Rectangle`, `Group 3`, `Text`, `Component 1`, `Vector` | `object.rename` / `object.batchRename` with a role name |
| `placeholder-text` | verbose | `characters` "Lorem ipsum…", "Title", "Button", "Label", "Text", "Placeholder" | `text.set` with real copy (ask for it) |

## Component (1)

| Rule | Sev | Check | Fix |
|---|---|---|---|
| `component-bindings` | style | `component.properties` lists a property no layer uses, or a text layer in a component that varies between instances has no text property | `component.bindProperty` / `component.addProperty {type: "text", layer}` |
