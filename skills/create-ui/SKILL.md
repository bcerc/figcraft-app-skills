---
name: create-ui
description: "Create UI in the FigCraft app (screens, pages, sections, single components with variants) when there is no design system to reuse. Use when: create/design/build/make + screen/page/component/button/card/variant in FigCraft. Builds with batch + node.create + auto layout props, then verifies with get_node and screenshot. Do NOT use when the file or an enabled library already has components/styles/variables to reuse (use figcraft-app:generate-design) or for building a full design system (use figcraft-app:generate-library)."
---

# FigCraft App — Create UI

Build UI declaratively: one `batch` per screen or section, every layer a `node.create` with auto layout
props, `{"$ref"}` for parents. Load `figcraft-app:use` first.

## Skill Boundaries

- **New UI without a design system** (this skill). Also covers new reusable components (§5).
- File has components, styles or variables, or an enabled library → `figcraft-app:generate-design`.
- Full design system (variables + components + theming) → `figcraft-app:generate-library`.
- Reviewing existing designs → `figcraft-app:design-review`.
- Code from a design → `figcraft-app:implement-design`.
- 3+ screens in one flow → also `figcraft-app:multi-screen-flow`.

## Workflow

1. **Connect and pin the file** — `inspect_ui {}` (attached) and `run_command doc.list` → keep the `document` id.
2. **Check for a design system** — `component.list`, `style.list`, `variable.list`, `library.list`.
   Anything useful there → switch to `figcraft-app:generate-design`.
3. **Design preflight** (blocking) — decide and state, then ⛔ **wait for the user's confirmation**:
   - Purpose and the one primary action of the view
   - Platform and frame size (`frame.presets`: `iPhone 16 Pro` 402×874, `Android Compact` 412×917, `Desktop` 1440×1024)
   - Language (load `figcraft-app:ux-writing`), content density, tone
   - Palette (1 dominant + 1 accent, ≤ 5 colours) and type scale (≤ 3 tiers, ≤ 3 weights), with reasons —
     follow `figcraft-app:ui-ux-fundamentals` + `figcraft-app:design-creator`
4. **Find a free spot** — `inspect_document {depth: 1}`; place new top-level frames to the right of the
   rightmost `absoluteBounds` + 100 (`frame.create {preset}` without `x`/`y` does this for you).
5. **Build** — one `batch` per screen (or per section for large screens). See §2.
6. **Look** — `screenshot {ids: [screenId], maxSize: 1200}`. Fix what's wrong before the next screen.
7. **Check** — `get_node {id: screenId, depth: 3}` for sizing; run `figcraft-app:design-lint`.

## 1. Translation From Figma Habits

| Figma / plugin habit | FigCraft app |
|---|---|
| `layoutMode: "VERTICAL"` | `layout: "vertical"` |
| `itemSpacing` | `gap` |
| `primaryAxisAlignItems` / `counterAxisAlignItems` | `mainAlign` / `crossAlign` |
| `layoutSizingHorizontal: "FILL"` | `sizingH: "fill"` |
| `clipsContent` | `clip` |
| `create_frame` with nested `children` | `batch` of `node.create` steps with `{"$ref": parent}` |
| `role: "screen"` | name the frame `Screen / <name>`; there is no role prop |
| `icon_create` | see `figcraft-app:iconography` |
| `export_image` | `screenshot` (look) / `export` (files) |
| `lint_fix_all` | `figcraft-app:design-lint` |

## 2. Screen Recipe

```json
{"label": "Screen / Sign in", "commands": [
  {"command": "frame.create", "as": "screen", "params": {"preset": "iPhone 16 Pro", "name": "Screen / Sign in",
    "props": {"fill": "#FFFFFF", "layout": "vertical", "mainAlign": "spaceBetween", "sizingH": "fixed", "sizingV": "fixed", "padding": [80, 24, 48, 24]}}},
  {"command": "node.create", "as": "top", "params": {"type": "frame", "name": "Top Content", "parent": {"$ref": "screen"},
    "props": {"fill": "none", "layout": "vertical", "gap": 32, "sizingH": "fill", "sizingV": "hug"}}},
  {"command": "node.create", "params": {"type": "text", "parent": {"$ref": "top"}, "text": "Welcome back",
    "props": {"fontSize": 28, "fontStyle": "Bold", "fill": "#111827", "sizingH": "fill"}}},
  {"command": "node.create", "params": {"type": "text", "parent": {"$ref": "top"}, "text": "Sign in to see your saved trips.",
    "props": {"fontSize": 16, "lineHeight": "150%", "fill": "#4B5563", "sizingH": "fill"}}},
  {"command": "node.create", "as": "bottom", "params": {"type": "frame", "name": "Bottom Content", "parent": {"$ref": "screen"},
    "props": {"fill": "none", "layout": "vertical", "gap": 16, "sizingH": "fill", "sizingV": "hug"}}},
  {"command": "node.create", "as": "cta", "params": {"type": "frame", "name": "Button / Primary", "parent": {"$ref": "bottom"},
    "props": {"fill": "#0F766E", "cornerRadius": 12, "layout": "horizontal", "mainAlign": "center", "crossAlign": "center",
      "padding": [14, 20, 14, 20], "sizingH": "fill", "sizingV": "hug", "minHeight": 48}}},
  {"command": "node.create", "params": {"type": "text", "parent": {"$ref": "cta"}, "name": "Label", "text": "Sign in",
    "props": {"fontSize": 16, "fontStyle": "Semi Bold", "fill": "#FFFFFF"}}}
]}
```

## 3. Layout Rules (the ones that break screens)

- Screen frames: `sizingH: "fixed"`, `sizingV: "fixed"`. Containers inside: `sizingH: "fill"`, `sizingV: "hug"`.
- A `spaceBetween` screen splits its children top/bottom; give the stretching child `sizingV: "fill"` when
  it should take the remaining height.
- Text that should wrap: `sizingH: "fill"` inside auto layout, or a fixed `width` (`textAutoResize: "height"`).
- Wrapper frames that only group should have `fill: "none"` (new frames are white).
- Placeholders for logos, avatars, charts: `frame` (can hold children), not `rectangle`.
- Touch targets ≥ 44×44: `minHeight: 44` / `minWidth: 44` on buttons and icon buttons.
- Spacing from the scale (4, 8, 12, 16, 24, 32, 48, 64…); radius nests as outer − padding.
- Use `layout: "grid"` with `columnTracks` for dashboards and card grids instead of nested rows.
- Real copy only — no "Lorem ipsum", "Button", "Title".

## 4. Updating an Existing Screen

1. `get_node {id: screenId, depth: 3}` — current structure and ids.
2. Edit with `set_properties {ids, props}` or a `batch` of `node.set`; replace text with `text.set {id, characters}`.
3. Add sections with `node.create {parent: screenId, index}` (index = position in the flow).
4. Remove with `edit.delete {ids}` — confirm with the user first if they didn't ask for the removal.
5. `screenshot` after each change.

## 5. New Reusable Components

1. Build the default variant as a frame (batch above), named `Property=Value` (e.g. `Style=Primary, Size=md`).
2. `component.create {ids: [frame]}` — the frame becomes a component (same id).
3. Properties: `component.addProperty {id, name: "Label", type: "text", default: "Save", layer: <text id>}`;
   `{type: "boolean", name: "Show icon", layer: <icon id>}`; `{type: "instanceSwap", default: <component>}`
   for icons; `component.makeSlot {id: <frame inside the component>}` for free content.
4. Variants: `component.addVariant {id, property: "Style", value: "Secondary"}` duplicates the variant into a
   set (the first call turns the component into a set); then edit the new variant's layers.
   Or build several components and `component.combineVariants {ids}`.
5. Rename the set (`object.rename`) to the component name (`Button`), and give it a `description`.
6. Verify: `component.properties {id: setId}` (check `conflicts` is empty), `screenshot {ids: [setId]}`,
   and `component.playground {id: setId, properties: {...}}` to try combinations without editing the file.
7. Place: `instance.create {component: setId, parent}` then
   `instance.setProperties {ids: [inst], properties: {Style: "Secondary", Label: "Cancel"}}`.

**≥ 8 variants:** write the variant matrix first (variant × fill × text colour × padding × structure),
and define each distinct structure as a tree. Structural variants (Loading = spinner only) are built
separately, not by hiding layers of the default.

## 6. Error Recovery

- A failed `batch` created nothing; read the error (it names the step), fix it, resend the whole batch.
- An unknown prop error lists the valid spelling; check `references/props.md` in `figcraft-app:use`.
- Something looks wrong but numbers look right → `screenshot {ids: [childId]}` at a higher `scale`.
- Undo a whole batch with `undo` (one step).
