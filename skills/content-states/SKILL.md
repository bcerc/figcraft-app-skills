---
name: content-states
description: "Design patterns for empty, loading, and error states. Use when: empty state/loading/skeleton/error/no data + design/screen/component, or when ensuring data-driven views handle all states."
---

# Content States — Empty, Loading, Error Patterns

Design patterns for the three critical content states every data-driven view must handle: empty, loading (skeleton), and error. Ensures no view is left without guidance when data is absent or unavailable.

## Skill Boundaries

- Use this skill for **content state design patterns** (empty, loading, error).
- If the task is **creating the full UI**, switch to `figcraft-app:create-ui` and reference this skill for state patterns.
- If the task is **reviewing existing designs for missing states**, switch to `figcraft-app:design-review`.

## Design Direction

Design direction comes from `figcraft-app:ui-ux-fundamentals`, plus `figcraft-app:design-guardian` when the file has its own styles, variables or components or an enabled library, else `figcraft-app:design-creator`.


## Empty State

```
Container (vertical, fill/hug, crossAlign: center, padding: 40–60)
  ├── Illustration (120–160px, subtle fill or SVG)
  ├── Heading ("No items yet" / "Get started") — 20px, semibold
  ├── Body ("Add your first item to see it here") — 14–16px, muted
  └── CTA Button ("Add Item") — primary style
```

Rules:
- Center vertically and horizontally in container
- Use encouraging, action-oriented language (not error language)
- CTA should directly trigger the creation action
- NEVER leave a list/grid container with zero children and no empty state

## Loading State (Skeleton)

```
Same structure as loaded state, but:
  ├── Text → gray rectangles (cornerRadius: 4, fill: gray-200, height matching line-height)
  ├── Images → gray rectangles (same dimensions, fill: gray-100)
  ├── Avatar → gray circle (same size)
  └── All skeleton elements: no stroke, uniform gray palette
```

Rules:
- Match the loaded layout exactly — skeleton IS the layout with gray placeholders
- NEVER use a centered spinner for content with a known layout
- Spinner only for indeterminate operations (file upload, search)

## Error State

```
Container (vertical, fill/hug, crossAlign: center, padding: 40–60)
  ├── Error icon (48–64px, warning/error color)
  ├── Heading ("Something went wrong") — 20px, semibold
  ├── Body ("We couldn't load your data. Please try again.") — 14–16px, muted
  └── Retry Button ("Try Again") — secondary or outline style
```

Rules:
- Use neutral, non-blaming language
- Always provide a retry action
- Don't use red for the entire error state — red for icon/accent only

## Workflow

When designing a data-driven view:

1. Design the loaded state first (primary content)
2. Create the empty state variant (no data yet)
3. Create the loading state (skeleton matching loaded layout)
4. Create the error state (recovery-focused)
5. Verify all four states fit within the same container dimensions

## Building States in the FigCraft App

- Make the view a component and the states its variants, so screens switch state with one property:
  `component.create {ids: [view]}` → `object.rename {ids: [view], name: "State=Loaded"}` →
  `component.addVariant {id: view, property: "State", value: "Empty"}` (again for `Loading`, `Error`) → edit each variant's layers.
- Skeleton blocks are `rectangle` layers (`create_node {type: "rectangle", parent, props: {fill: "#E5E7EB", cornerRadius: 4}}`) sized like the text they stand for; inside auto layout set `sizingH: "fill"` for full-width lines.
- Place a state on a screen with `instance.create {component: <set id>, parent}` then `instance.setProperties {ids: [inst], properties: {State: "Empty"}}`.
- Check every state: `screenshot {ids: [setId]}` shows all variants at once.
