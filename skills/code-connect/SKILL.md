---
name: code-connect
description: "Link FigCraft app components to the project's real code components (React, Leptos, Vue, SwiftUI, Compose, ArkUI, Flutter) with codeConnect.set templates, import/export figcraft.connect.json for the repo, and check the snippets Dev Mode now generates. Use when the user mentions Code Connect, mapping design components to code, connected components, or figcraft.connect.json."
---

# FigCraft App — Code Connect

The app stores component → code links in the file and uses them in `inspect.code`: connected instances
become the project's own snippet with its import. No CLI, parser or `.figma.tsx` files are involved.
Load `figcraft-app:use` first.

## Skill Boundaries

- Map components to code → this skill.
- Generate screen code → `figcraft-app:implement-design` (after mapping).
- Document components → `figcraft-app:component-docs`.

## Workflow

### 1. Find unmapped components

`component.list` → for each set/component, `get_node {id, depth: 0}` → `codeLinks` (empty = unmapped).
Focus on components with instances in use.

### 2. Read each component's API

`component.properties {id}` (variant, boolean, text, instance-swap, slot properties) and
`inspect.componentCode {id, language: "react"}` (generated param names and types).

### 3. Find the code component

Search the codebase for the component (name, props). Read its props and defaults. Note the import path
the project uses (`@acme/ui`, `@/components/ui/button`).

### 4. Write the link

```json
{"command": "codeConnect.set", "params": {"id": 120, "language": "react", "importPath": "@/components/ui/button",
  "name": "Button",
  "template": "<Button variant={Style} size={Size} icon={showIcon ? \"check\" : \"none\"}>{Label}</Button>"}}
```

Template rules (templates are text, never executed):
- `{Property}` (name or param name) → the instance's value, escaped for the language. Write it **without
  quotes** in React/Leptos: `size={size}` → `size="Large"`, `disabled={disabled}` → `disabled={true}`.
  `size="{size}"` produces `size="{"Large"}"`.
- `{param ? "a" : "b"}` inserts one of two strings (use the param name, e.g. `showIcon`). **figcraft-cli 0.12.1
  leaves ternaries unexpanded** — check the returned `code`; on older CLIs map booleans with `{showIcon}`
  (`icon={true}`) instead.
- Any other `{…}` stays as written; the result's `unknown` lists placeholders that aren't properties —
  fix those.
- Vue: `:prop={value}` takes an expression; static attributes take plain text.
- An instance-swap property inserts the swapped component (itself connected or generated).

Variants link through their set. One link per language; `codeConnect.remove {id, language?}` removes.

### 5. Check

- Result of `codeConnect.set`: `{component, language, code, unknown}` — `code` is the default instance's snippet.
- `inspect.code {id: <an instance>, language: "react"}` → `connected: true`, import line + snippet.
- `inspect.componentCode {id}` → `connected: {importPath, name, template, import, code}`.
- A screen: `inspect.code {id: <screen>, language: "tailwind"}` should now use the real components.

### 6. Keep it in the repo

- `codeConnect.export {path: "<repo>/figcraft.connect.json"}` → `{version: 1, links: [...]}`, sorted, for
  version control.
- In another file: `codeConnect.import {path}` links every component or set with each entry's name
  (one undo step; invalid entries skipped with `warnings`).

## Limits

≤ 5,000 links and 4 MB per import; templates ≤ 4,000 chars; names ≤ 100; import paths ≤ 300.

## Pitfalls

- Mapping by name only — check the code component's props match the variant axes; rename with
  `component.editProperty` or adapt the template.
- Boolean property that controls an icon: the ternary form on CLIs that expand it, else `{showIcon}` as a
  boolean prop. A property name with a space isn't a valid placeholder inside a ternary; use its param name.
- Library copies (read-only) — set links in the library file and publish.
