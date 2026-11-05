---
name: responsive-design
description: "Responsive web design rules — breakpoints, auto-layout strategy, sizing patterns. Use when: responsive/breakpoint/mobile/tablet/desktop + design/layout/screen, or when creating multi-breakpoint web designs."
---

# Responsive Design — Web Breakpoint Rules

Rules and patterns for creating responsive web designs in FigCraft across mobile, tablet, and desktop breakpoints. Covers auto-layout strategy, sizing patterns, and common pitfalls.

## Skill Boundaries

- Use this skill for **responsive web layout decisions** (breakpoints, column grids, sizing).
- If the task is **iOS-specific design** (safe areas, HIG), switch to `figcraft-app:platform-ios`.
- If the task is **Android-specific design** (Material, 48dp), switch to `figcraft-app:platform-android`.
- If the task is **creating UI**, switch to `figcraft-app:create-ui` and reference this skill for responsive rules.

## Design Direction

Design direction comes from `figcraft-app:ui-ux-fundamentals`, plus `figcraft-app:design-guardian` when the file has its own styles, variables or components or an enabled library, else `figcraft-app:design-creator`.


## Breakpoints

| Breakpoint | Width | Columns | Padding |
|-----------|-------|---------|---------|
| Mobile | 375px | 1 | 16px |
| Tablet | 768px | 2 | 24px |
| Desktop | 1280px | 3–4 | 32–64px |

## Auto-Layout Strategy

- Mobile: `layout: "vertical"` stack, 1 column, children `sizingH: "fill"`
- Tablet: mix horizontal rows (2-col) + vertical sections
- Desktop: horizontal main layout with sidebar + content area (or `layout: "grid"` with `columnTracks: [240, "1fr"]`)

## Sizing Patterns

| Context | Horizontal | Vertical |
|---------|-----------|----------|
| Page container | FIXED (breakpoint width) | HUG |
| Content area | FILL | HUG |
| Sidebar | FIXED (240–300px) | FILL |
| Cards in grid | layoutGrow: 1 (equal width) | HUG |
| Full-width sections | FILL | HUG |

## Key Rules

- NEVER use fixed pixel widths for content children at mobile — use FILL
- SHOULD use maxWidth constraints for text readability (600–800px at desktop)
- Breakpoint frames are FIXED width; their children adapt via fill/hug
- Cards: `sizingH: "fill"` on each card in a horizontal row for equal distribution (fill children share space like CSS flex)
- Navigation: horizontal on desktop, bottom tab bar on mobile

## Workflow for Multi-Breakpoint Designs

### Step 1: Create Breakpoint Frames

Build one frame per breakpoint, side by side:

```
Wrapper  (frame, layout horizontal, gap 40, sizingH/V hug, clip false)
  ├── Mobile / <page>   (width 375, sizingV hug, layout vertical)
  ├── Tablet / <page>   (width 768, sizingV hug, layout vertical)
  └── Desktop / <page>  (width 1280, sizingV hug, layout vertical)
```

Build the wrapper and the three empty frames in one `batch` with `"as"` names and `{"$ref": …}` parents.
Give matching layers **the same names** in every breakpoint frame: `inspect.code {id: <desktop>, language: "tailwind", mobile: <mobile id>}` then writes one mobile-first component, with the desktop differences behind `lg:`.

### Step 2: Build Mobile First

Design the mobile layout first — it forces content prioritization.

### Step 3: Adapt to Tablet

Expand to 2-column layouts where appropriate. Keep single-column for forms and focused content.

### Step 4: Adapt to Desktop

Add sidebar navigation, expand grids to 3–4 columns, increase padding.

### Step 5: Verify

For each breakpoint frame: `screenshot {ids: [frameId]}` to look, then `get_node {id, depth: 3}` to check numbers (no child wider than its parent, text `sizing.horizontal` is `fill` inside fluid containers, nothing clipped). Then run `figcraft-app:design-lint` on the wrapper.

To check that a layout really reflows, resize a copy instead of the original: `batch` → `edit.duplicate {ids: [frameId]}` (as `copy`) → `node.set {ids: [{"$ref": "copy", "field": "ids/0"}], props: {width: 320}}` → `screenshot` → `undo`.
