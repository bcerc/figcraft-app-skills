---
name: create-design-system-rules
description: "Generate project-specific rules (CLAUDE.md, AGENTS.md, .cursor/rules) that tell agents how to turn FigCraft app designs into code for this codebase: where components live, how tokens map, which inspect.code language to use, asset handling, and the required FigCraft MCP flow. Use when the user says 'create design system rules', 'set up FigCraft design rules for this project', or wants project conventions for FigCraft-to-code work."
---

# FigCraft App — Create Design System Rules

Write rules once so every design-to-code task in this repo follows the same path. Load `figcraft-app:use`.

## Skill Boundaries

- Project rule files → this skill. One-off implementation → `figcraft-app:implement-design`.
- Component links → `figcraft-app:code-connect` (rules should tell agents to keep them current).

## Workflow

### 1. Find the rule file

Use what the repo has: `CLAUDE.md`, `AGENTS.md` (check whether it's generated from another file before
editing), `.cursor/rules/*.mdc`, `.claude/rules/*.md`. Ask before creating a new one.

### 2. Analyze the codebase

- Framework and styling (React + Tailwind, Vue + CSS modules, SwiftUI…) → the matching `inspect.code` language.
- Component library location and naming; existing token source (CSS variables, Tailwind theme, JSON).
- Asset folders and formats (SVG icons, image sizes).
- Existing `figcraft.connect.json`.

### 3. Read the FigCraft side

`component.list`, `variable.list` (names, `codeSyntax`), `style.list`, `library.list` — so the rules name
real collections and components.

### 4. Write the rules

Essential (always):

```markdown
## FigCraft → code

- Designs live in `<path>.figcraft` (library: `<path>`). Use the FigCraft app MCP (`figcraft-app` attached,
  `figcraft` headless); never Figma tools.
- IMPORTANT flow, do not skip: get_node on the frame → screenshot → inspect.code {language: "tailwind"} →
  map to components in `src/components/ui/` → tokens from `src/styles/tokens.css` → compare with the screenshot.
- Never hardcode colours or spacing; FigCraft variables map 1:1 to CSS variables via codeSyntax.WEB.
- Components with Code Connect links (figcraft.connect.json) must be used as generated, never rebuilt.
- Icons: export SVG with file.exportLayers {assets: true} into `src/assets/icons/`; images @2x PNG.
```

Recommended: component naming map (design → code), breakpoints (`mobile` frames for `lg:`), how to handle
variants missing in code, when to ask the designer (comment with `comment.add` on the frame).

Optional: platform rules (SwiftUI/Compose names via `codeSyntax.iOS/ANDROID`), Storybook, test expectations.

### 5. Save and validate

Save to the rule file (with its mirror, if the repo keeps one). Validate by running one small
implementation with the rules and checking the agent followed the flow; tighten wording where it didn't.

## Best Practices

Start small and iterate; be specific (paths, names); make rules actionable; mark critical rules
IMPORTANT; give the reason for non-obvious rules; update them when the design system changes.
