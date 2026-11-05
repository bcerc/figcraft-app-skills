---
name: generate-design
description: "Create or update screens in the FigCraft app by REUSING an existing design system: the file's own components, styles and variables, or an enabled library (.figcraft library file or team library). Use when: 'create a screen using the design system', 'build a landing page from our components', 'push this page to FigCraft', 'update the screen'. Extends figcraft-app:create-ui with a mandatory discovery phase. Do NOT use for no-library creation (figcraft-app:create-ui) or for building the system itself (figcraft-app:generate-library)."
---

# FigCraft App — Build Screens From a Design System

Use the system's components, variables and styles instead of drawing primitives with hardcoded values.
Creation mechanics (batch, props, layout rules) are in `figcraft-app:create-ui`; load it and
`figcraft-app:use` first. Design direction: `figcraft-app:ui-ux-fundamentals` + `figcraft-app:design-guardian`.

## Skill Boundaries

| When | Use |
|---|---|
| Build or update a screen from existing components/tokens | this skill |
| No design system anywhere | `figcraft-app:create-ui` |
| Create new components or the token set | `figcraft-app:generate-library` |
| Code from a design | `figcraft-app:implement-design` |

## Step 0: Connect

`inspect_ui {}` (attached), `run_command doc.list` → keep the `document` id. Present the design preflight
from `figcraft-app:create-ui` → ⛔ wait for confirmation.

## Step 1: Understand the Screen

From the user's description or source code: list sections (Header, Hero, Content, Pricing, Footer…) and
the components each needs. In code, read component defaults (`<Button size="small">` may default to
`variant="primary"`).

## Step 2: Discover Assets

Three sources, in priority order: **this file → enabled libraries → create new (ask first)**.

### 2a. Components

- `run_command component.list` → `[{id, name, type, page, instances, folder, label, library?}]`.
  `folder` tells the category ("Forms" vs "Avatars"); property names like "Size" appear everywhere.
- `run_command library.list {assets: true}` → each enabled library's components, styles, collections and
  variables. No libraries but the user has a library file → `library.add {path}` (ask first).
- Details: `component.properties {id}` (variant axes, defaults, text/boolean/swap/slot properties).

Write a component map before building:

```
Button  → set 120 (local)        Style=Primary|Secondary|Ghost, Size=sm|md|lg; Label (text); Icon (swap)
Input   → "Input" in "Core UI"   State=Default|Focus|Error; Label, Placeholder (text)
Card    → component 88 (local)   no variants; Content (slot)
```

### 2b. Variables

- `run_command variable.list` → collections (with modes) and variables (`name`, `resolvedType`, `scopes`, values).
- Library variables are only in `library.list {assets: true}`; an empty `variable.list` doesn't mean the
  system has none.
- Note semantic names (surface, text/primary, border, accent) and spacing/radius numbers.

### 2c. Styles

`run_command style.list` → text, paint, effect and grid styles by name and id.

## Step 3: Build

Follow `figcraft-app:create-ui` §2, with these swaps:

| Instead of | Use |
|---|---|
| Hand-built button/input/card frames | `instance.create {component, parent}` (local) or `library.place {library, component}` then `node.reparent {ids, parent, index}` |
| Variant choice | `instance.setProperties {ids, properties: {Style: "Secondary", Label: "Learn more"}}` |
| Hex fills | create with a hex, then `variable.bind {ids, field: "fill", variable: "surface/primary"}` in the same batch (library: `library.bindVariable {library, variable, field, ids}`) |
| Font props | `textStyle: "Heading/H1"` in props (library: `library.applyStyle {library, style, ids}`) |
| Shadow arrays | `effectStyle: "Elevation/2"` |
| Free content inside a component | `instance.slotInsert {id: <slot>, component, index}` |

Example section (local system):

```json
{"label": "Hero", "commands": [
  {"command": "node.create", "as": "hero", "params": {"type": "frame", "name": "Hero", "parent": 14,
    "props": {"fill": "#FFFFFF", "layout": "vertical", "gap": 24, "padding": 64, "crossAlign": "center", "sizingH": "fill", "sizingV": "hug"}}},
  {"command": "variable.bind", "params": {"ids": [{"$ref": "hero"}], "field": "fill", "variable": "surface/primary"}},
  {"command": "node.create", "as": "h1", "params": {"type": "text", "parent": {"$ref": "hero"}, "text": "Plan trips together",
    "props": {"textStyle": "Heading/H1", "fill": "#111827", "textAlign": "center"}}},
  {"command": "variable.bind", "params": {"ids": [{"$ref": "h1"}], "field": "fill", "variable": "text/primary"}},
  {"command": "node.create", "as": "row", "params": {"type": "frame", "name": "Actions", "parent": {"$ref": "hero"},
    "props": {"fill": "none", "layout": "horizontal", "gap": 16, "sizingH": "hug", "sizingV": "hug"}}},
  {"command": "instance.create", "as": "b1", "params": {"component": 120, "parent": {"$ref": "row"}}},
  {"command": "instance.setProperties", "params": {"ids": [{"$ref": "b1"}], "properties": {"Style": "Primary", "Label": "Get started"}}},
  {"command": "instance.create", "as": "b2", "params": {"component": 120, "parent": {"$ref": "row"}}},
  {"command": "instance.setProperties", "params": {"ids": [{"$ref": "b2"}], "properties": {"Style": "Secondary", "Label": "See pricing"}}}
]}
```

Theming: set a collection's mode on a screen with `variable.setMode {ids: [screen], collection, mode: "Dark"}`
(library: `library.setVariableMode`).

## Step 4: Validate

- `screenshot {ids: [screenId]}` — wrong variants, placeholder labels, cropped text.
- `selection.colors {ids: [screenId]}` — any entry with `variable: null` and `style: null` is a hardcoded
  colour; bind it with `selection.bindColorVariable {targets, variable}`.
- `get_node {id, depth: 3}` — instances show `mainComponentName` and `componentProperties`.
- Run `figcraft-app:design-lint`.

## Step 5: Updating an Existing Screen

1. `get_node {id: screenId, depth: 3}`.
2. Swap components: `instance.swap {ids, component}` (overrides with matching names stay).
3. Change variants/text: `instance.setProperties`.
4. Add sections: `node.create {parent: screenId, index}`; remove: `edit.delete {ids}` (confirm first).
5. `screenshot` after each change.

## Build Manually vs Reuse

| Build manually | Reuse from the system |
|---|---|
| Page wrapper, section frames, layout rows/grids | Components → instances |
| Dividers, decorative shapes | Colours, spacing, radius → `variable.bind` |
| | Typography → `textStyle` |
| | Shadows → `effectStyle` |

**Never hardcode a colour or spacing value when a variable for it exists.** When none matches, use the
closest scale value and tell the user which values are unbound.
