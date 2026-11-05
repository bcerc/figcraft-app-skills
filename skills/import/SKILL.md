---
name: import
description: "Bring outside designs into the FigCraft app as editable layers: SVG (shapes, gradients, masks, text), .fig and FigJam .jam files, Sketch files, Figma REST API file JSON with its variables, images, and HTML pages (via an SVG or screenshot reference, since the app has no HTML converter). Use when: import/convert/open + svg/fig/sketch/figma file/html/webpage/image in FigCraft."
---

# FigCraft App — Import

Load `figcraft-app:use` first. All imports are best effort: read the `warnings` in every result and tell
the user what was left out.

## Skill Boundaries

- Getting outside files in → this skill. Building from scratch → `figcraft-app:create-ui`.
- Linking code components → `figcraft-app:code-connect`.

## Formats

| Source | As a new document | Into the current page |
|---|---|---|
| `.svg` | `open_file {path}` | `run_command file.import {path, x?, y?, center?}` or `{data (base64), name}` |
| `.fig` | `open_file {path}` (`summary` + `warnings`/`repairs`) | — |
| FigJam `.jam` | `open_file {path}` (opens as a board) | — |
| `.sketch` (48+) | `open_file {path}` | — |
| Figma REST file JSON | `open_file {path, variables?}` | `file.import {path, variables?}` (variables JSON as object, text or path) |
| PNG/JPG/WebP/GIF | `open_file {path}` | `image.place {path, x?, y?, parent?, mode?}` or `file.placeImage {path}`; on an existing layer: `image.place {path, target}` |
| `.figcraft` | `open_file {path}` | copy/paste between open files keeps instances linked |

`figcraft-cli info <file> --json` (shell) previews a file and lists what wasn't imported, without opening it.

## SVG Details

Comes in editable: groups named from `id`, rects/circles/ellipses/lines as real shapes, the rest as vectors;
strokes, dashes, caps; linear/radial gradients; clip paths as masks; shadows and blurs as effects; text as
text layers (installed fonts); images as image fills. Left out (listed in `warnings`): other filters,
rotated repeating patterns, external linked files.

## HTML / Web Pages

The app has no HTML importer. Choose with the user:

1. **Rebuild (default)** — read the HTML/CSS (or the running page) and rebuild it with
   `figcraft-app:create-ui` / `figcraft-app:generate-design`: editable, token-bound, auto layout.
   Use a screenshot of the page as reference:
   `image.place {path: "<page.png>", x, y}`, `set_properties {props: {opacity: 0.4, locked: true}}`,
   build beside or over it, then delete the reference.
2. **SVG snapshot** — when the page can be exported to SVG (a static SVG export or a design tool's copy-as-SVG),
   `file.import {path}` gives editable vectors and text, but no auto layout or tokens.

## Workflow

1. Confirm the source path and where it should go (new document vs current page).
2. Large `.fig`/`.sketch`: `figcraft-cli info` first; warn about what won't come over.
3. Import; read `warnings`.
4. `screenshot` the result; `text.missingFonts` — missing families render in a fallback.
5. Clean up: rename default layer names, add auto layout where it should flow (`layout.suggest`), turn
   repeated pieces into components (`component.create`), bind colours to variables
   (`selection.colors` → `selection.bindColorVariable`).
6. Run `figcraft-app:design-lint` when the import will be built on.

With `--automation-read-root` set, files outside the read roots are refused; ask the user to move the file
or widen the roots.
