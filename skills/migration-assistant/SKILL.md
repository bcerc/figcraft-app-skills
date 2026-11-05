---
name: migration-assistant
description: "Migrate FigCraft app files between design system versions: map old tokens to new, rename and alias variables, swap deprecated components or whole libraries, re-point styles, verify, then clean up. Use when: migrate/upgrade/update + design system/tokens/components/library/version in FigCraft. Incremental, with a version checkpoint and user approvals before anything destructive."
---

# FigCraft App — Migration Assistant

Load `figcraft-app:use` first.

## Skill Boundaries

- Version-to-version migration → this skill.
- New system → `figcraft-app:generate-library`. Health check → `figcraft-app:design-system-audit`.
- Tokens from a spec → `figcraft-app:token-sync`.

## Workflow

### 1. Checkpoint

`run_command version.autosave` then `version.rename {index: <last>, name: "Before migration to vX"}` (read the
index from `version.list`). Rollback later: `version.restore {id}`.

### 2. Discover

`variable.list`, `style.list`, `component.list` (with `instances` counts), `library.list {assets: true}`,
`library.updates`.

### 3. Migration map

Agree the mapping with the user — ⛔ wait for confirmation:

```
Variables:  color/primary → color/accent/default · spacing/md → space/16 (alias)
Components: Button (old, set 120) → Button v2 (library "Core UI"); Style=Filled → Style=Primary
Styles:     Text/Body → Body/md
```

### 4. Variables

| Change | Call |
|---|---|
| Rename | `variable.update {variable, name}` (bindings follow, ids stay) |
| New | `variable.create {collection, name, type, values}` |
| Old → alias of new | `variable.set {variable: old, mode, value: {alias: new}}` (per mode) |
| Scopes / code syntax | `variable.update {variable, scopes, codeSyntax}` |
| Rebind layers | `variable.bind {ids, field, variable: new}` or `selection.bindColorVariable {targets, variable}` |

Verify after each batch: `variable.list`, and `selection.colors` on key screens.

### 5. Components

| Change | Call |
|---|---|
| Whole library v1 → v2 | `library.add {path: v2}` then `library.swap {from: v1, to: v2}` → `{components, styles, variables, unmatched}` (matches by name; overrides kept) |
| One component | `instance.swap {ids, component}` (overrides on same-named layers stay) |
| Property renames | `instance.setProperties {ids, properties}` per instance after the swap |
| Pull library updates | `library.acceptUpdates {ids?}` |

Collect instance ids with `get_node` walks (or `node.find {component: "Button"}` on newer CLIs).
Resolve `unmatched` with the user before continuing.

### 6. Styles

`style.update {style, value}` for value changes; for replacements apply the new style to the old one's users
(`style.apply {ids, style}`), library styles with `library.applyStyle`.

### 7. Verify

- No layer bound to deprecated variables (`selection.colors`, `boundVariables` in `get_node`).
- No instances of deprecated components (`component.list` → `instances: 0` for the old ones).
- No hardcoded values where new tokens exist (`figcraft-app:design-lint` token rules).
- Visual check: `screenshot` of key screens; compare with the checkpoint (`version.preview {id}`,
  then `version.exitPreview`), or `dev.compare {id, version}` for a property-level diff of a frame.

### 8. Clean up

⛔ Ask before every destructive step: `variable.delete` (bound layers keep their values; aliases get the
values), `variable.deleteCollection`, `edit.delete` of old component pages, `library.remove`.

## Strategies

- **Token rename (non-breaking):** create new → alias old to new → rebind gradually → delete old when unused.
- **Value change:** update the variable → check bound layers → re-check contrast in every mode.
- **Component swap:** list instances → swap → re-apply property values → screenshot.
- **Major version:** new collections/components beside the old → migrate screen by screen → verify each →
  remove the old system last.

## Safety

Never delete without explicit confirmation; create before deleting; verify visually after each step;
keep a migration log (old → new, ids) in the scratchpad for rollback.
