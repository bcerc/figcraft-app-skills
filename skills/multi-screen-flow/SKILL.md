---
name: multi-screen-flow
description: "Multi-screen flow architecture in the FigCraft app — presentation wrapper, header, flow row, stages with step pills, fixed-size screens, build order, then prototype links. Use when: multi-screen/flow/onboarding/checkout/sign-up + design/create/build in FigCraft, or when creating 3+ screens in a single task."
---

# FigCraft App — Multi-Screen Flow

Flows (sign-in, onboarding, checkout) use a strict hierarchy; skipping a level collapses the layout.
Load `figcraft-app:use` and `figcraft-app:create-ui` first.

## Skill Boundaries

- 3+ screens in one task → this skill.
- One screen or element → `figcraft-app:create-ui`.
- Same content at several widths → `figcraft-app:responsive-design`.

## Hierarchy (do not skip levels)

```
Wrapper  frame, layout vertical, sizing hug/hug, crossAlign min, clip false,
         cornerRadius 20–40, fill #F3F4F6, padding 48, gap 32, name "Flow / <name>"
  ├── Header        layout vertical, hug/hug, gap 8, fill none
  │     ├── Title        text 24, Bold
  │     └── Description  text 16, muted
  └── Flow Row      layout horizontal, hug/hug, clip false, gap 40, fill none
        └── Stage / <label>   layout vertical, hug/hug, clip false, gap 16, fill none
              ├── Step Pill   layout horizontal, hug/hug, cornerRadius 100, fill dark, padding [6,14,6,14], gap 6
              │     ├── Number  "01", accent colour, Bold 13
              │     └── Label   "Sign in", white, Medium 13
              └── Screen / <label>   fixed 402×874 (iOS) or 412×915 (Android), layout vertical,
                                     mainAlign spaceBetween, cornerRadius 28, clip true, padding
                    ├── Top Content     layout vertical, sizing fill/fill
                    └── Bottom Content  layout vertical, sizing fill/hug
```

## Build Order

1. **Skeleton** — one `batch`: Wrapper, Header (title + description), Flow Row, and for each stage the
   Stage, Step Pill (number + label) and an empty Screen, with `"as"` names (`screen1`, `screen2`, …) and
   `{"$ref"}` parents. Note the screen ids from the result.
2. **Check the layout** — `screenshot {ids: [wrapper], scale: 0.3}`: all screens side by side in the Flow Row.
   Don't continue until they are.
3. **Fill screens** — one `batch` per screen (`parent: <screen id>`; Top Content + Bottom Content and their
   children), `screenshot {ids: [screen]}` after each. Icons: `figcraft-app:iconography`.
4. **Wire the prototype** — `proto.interaction.add` from each screen's CTA to the next screen
   (`action: {type: "navigate", dest}`), `back` on back buttons, then `proto.flow.add {start: <screen1>, name}`.
   Flows start at top-level frames: if the flow won't start from a screen nested in the wrapper, keep a
   top-level copy of the screens for the prototype and tell the user.
5. **Lint** — `figcraft-app:design-lint` on the wrapper.

## Key Rules

- Every ancestor of a Screen: `clip: false` (else shadows and pills are cut).
- Name screens `Screen / <label>` — lint and prototype analysis find them by name.
- Screen: `mainAlign: "spaceBetween"` for top/bottom split; its stretching child `sizingV: "fill"`.
- Sizes: iOS 402×874 (`frame.presets` "iPhone 16 Pro"), Android 412×915.
- Wrapper light grey so white screens stand out; a Screen is a page, not a card — no shadow.
- Grouping frames get `fill: "none"` (new frames are white).
