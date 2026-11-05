---
name: component-docs
description: "Generate documentation for FigCraft app components — properties, variants, defaults, dimensions, usage guidance, generated code — and audit their structural health (missing descriptions, unexposed text, empty or single-variant sets, unbound properties, variant conflicts). Use when: document/describe/catalog + components/variants/library in FigCraft, or auditing component quality before publishing."
---

# FigCraft App — Component Docs

Load `figcraft-app:use` first.

## Skill Boundaries

- Document and audit existing components → this skill.
- Create components or variants → `figcraft-app:generate-library` / `figcraft-app:create-ui` §5.
- Link components to code → `figcraft-app:code-connect`.
- Overall design quality → `figcraft-app:design-review`.

## Workflow

### 1. Inventory

`run_command component.list` → `[{id, name, type, page, instances, folder, label, library?}]`.
Skip library copies (`library` set) unless asked. Ask which components to document when there are many.

### 2. Audit

Per component or set:

| Read | Gives |
|---|---|
| `component.properties {id}` | properties (`name`, `type`, `default`, variant `options`), `conflicts` (variants sharing one combination), `set` |
| `get_node {id, depth: 4}` | `description`, size, `layout`, children, text layers, `codeLinks`, `annotations` |
| `screenshot {ids: [id]}` | the look of every variant |
| `instances` from the list | usage count (0 = unused) |

Flag:
- ⚠️ Missing description (`description` empty)
- ⚠️ Unexposed text — a TEXT layer that instances would change but no text property binds
- ⚠️ Empty component — no visible children
- ⚠️ Single-variant set — a set with one variant
- ⚠️ Unbound properties — a property no layer uses
- ⚠️ Variant conflicts — `conflicts` not empty
- ⚠️ Unused — 0 instances in this file (fine for a library file; say so)
- ⚠️ Default names inside (`Frame 3`, `Text`)

### 3. Details per component

- Variants: the option lists from `component.properties`.
- Code view: `inspect.componentCode {id, language: "react"}` → `properties [{name, param, type, default}]`
  and the generated definition (or the connected snippet when `codeConnect` is set).
- Try a combination without editing: `component.playground {id, properties: {Size: "lg"}, path: "<scratchpad>/btn-lg.png"}`.

### 4. Write the documentation

```markdown
## Button
<description>

| Property | Type | Values | Default |
|---|---|---|---|
| Style | variant | Primary, Secondary, Ghost | Primary |
| Size | variant | sm, md, lg | md |
| Label | text | — | "Save" |
| Show icon | boolean | — | false |
| Icon | instance swap | preferred: Icon/check, Icon/plus | Icon/check |

**Sizes:** sm 32 h · md 40 h · lg 48 h, padding 12/16/20 horizontal
**Use:** one Primary per view; Ghost for tertiary actions in toolbars.
**Don't:** put two Primary buttons side by side; shorten labels to "OK".
**Code:** `<Button style="Primary" size="md" label="Save" />`
```

Output inline by default; write a file when asked. To put it in the file itself, offer:
`set_properties {ids: [set], props: {description}}` and `annotation.add {id, label, properties: [...]}`.

### 5. Report issues

List the flagged items with ids.

### 6. Suggest fixes

- Add descriptions (`set_properties {props: {description}}`).
- Expose text: `component.addProperty {id, type: "text", name, layer}`.
- Merge or ungroup single-variant sets.
- Bind or delete unused properties (`component.bindProperty`, `component.deleteProperty`).
- Resolve conflicts by renaming variants (`component.editProperty {name, value, newValue}`).

Apply only on the user's go-ahead.
