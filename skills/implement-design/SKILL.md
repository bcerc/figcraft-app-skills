---
name: implement-design
description: "Translate FigCraft app designs into production code with 1:1 visual fidelity, using the app's Dev Mode code generation (inspect.code for CSS, HTML, React, Tailwind, Vue, Leptos, SwiftUI, Jetpack Compose, ArkUI, Flutter), component code, variable exports and asset export, then adapting it to the project's conventions. Use when: implement design / generate code / build this screen / code from FigCraft."
---

# FigCraft App — Implement Design

The app generates code itself. Treat it as a precise starting point, then rewrite it into the project's
components and tokens. Load `figcraft-app:use` first.

## Skill Boundaries

- Code from a design → this skill.
- Linking design components to code components → `figcraft-app:code-connect` (do it first when the
  project has a component library: generated code then uses the real components).
- Annotating for someone else to build → `figcraft-app:design-handoff`.

## Workflow

### 1. Target

The frame/component the user names, the selection (`inspect_document {depth: 0}` → `selection`), or
`inspect.readyForDev {}` for frames marked Ready for dev. Pin the `document` (`doc.list`).

### 2. Context

- `get_node {id, depth: 4}` — structure, sizing, auto layout, component instances and their properties.
- `inspect.properties {id}` on key layers — values with **token names**.
- `annotation.list {id}` and `devResource.list {id}` — the designer's notes and links.
- `dev.compare {id}` when the frame is "Changed" — what moved since it was marked ready.

Large frames: work section by section (`get_node` per child) instead of one huge read.

### 3. Visual reference

`screenshot {ids: [id], maxSize: 1600}` — keep it open while implementing.

### 4. Generate code

| Project | Call |
|---|---|
| React + Tailwind v4 | `inspect.code {id, language: "tailwind"}` (fluid boxes, bound variables as theme utilities; with `mobile: <mobile frame id>` mobile-first + `lg:`) |
| React / Vue / Leptos | `inspect.code {id, language: "react"|"vue"|"leptos"}` (whole tree) |
| Plain web | `inspect.code {id, language: "html"}` or `"css"`; `unit: "rem"`, `rootFontSize: 16` |
| iOS / Android / HarmonyOS / Flutter | `inspect.code {id, language: "swiftui"|"compose"|"arkui"|"flutter"}` |
| A component's API | `inspect.componentCode {id, language}` → props with types and defaults, definition, usage |

Instances of components linked with Code Connect come out as the project's own snippets with their imports.

### 5. Tokens and assets

- `variable.export {format: "css"|"tailwind"|"dart", path}` — the token layer the generated code refers to.
  If the project already has tokens, map instead of duplicating (`variable.list` → `codeSyntax`).
- `inspect.assets {ids: [id]}` → icons (SVG), images (PNG), layers with export settings;
  `file.exportLayers {ids: [id], assets: true, dir: "<project assets dir>"}` writes them.
  Single exports: `export {ids, format: "svg"|"png", scale: 2, path}`.

### 6. Translate to project conventions

- Replace generated markup with the project's components where one exists (check source code, not only names).
- Replace literal values with the project's tokens (`bg-accent`, `var(--space-16)`, theme objects).
- Keep the generated layout logic (flex direction, gaps, padding, fill/hug → `flex-1`/`w-full`/`w-fit`).
- Follow the project's file structure, naming, state handling and accessibility patterns.
- Don't copy absolute positions for content that flows.

### 7. Visual parity

Compare the running UI with the screenshot: spacing, type, colours, radius, shadows, alignment, wrapping.
Where you deviate on purpose (accessibility, existing component), say why.

### 8. Validate

- Every state the design shows (variants: `component.properties`; `component.playground` renders others).
- Responsive frames if the design has them.
- Copy matches exactly (`characters` in `get_node`).

## Rules

- Reuse over recreation; design system first; tokens over literals.
- Validate incrementally — one section at a time, screenshot against the reference.
- Document deviations from the design in the PR or reply.
- Variable names don't match project tokens → map via `codeSyntax` (`variable.update {codeSyntax: {WEB}}`)
  so the next export lines up, after asking the designer.
