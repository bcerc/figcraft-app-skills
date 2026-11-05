---
name: use
description: "MANDATORY prerequisite for every call to the FigCraft app's MCP tools (the figcraft-app server, attached to the running app, and the figcraft server, headless; as mcp__figcraft-app__* / mcp__figcraft__* or, when this plugin provides them, mcp__plugin_figcraft-app_figcraft-app__* / mcp__plugin_figcraft-app_figcraft__*). Load it before the first create_node, set_properties, run_command, batch, inspect_document, get_node, export or screenshot call of a task. Covers which server to use, the coordinate and auto layout model, props, batching with step references, finding layers, verification, files and templates, and the gaps in older figcraft-cli versions. FigCraft here is the native design app (figcraft-cli), not the FigCraft Figma plugin."
---

# FigCraft App — MCP Ground Rules

The FigCraft app is a native design tool with its own engine. Its MCP server is `figcraft-cli mcp`.
It is **not** Figma and **not** the "FigCraft" Figma plugin from `DivikWu/figcraft`: tools like
`get_mode`, `create_frame`, `lint_fix_all`, `use_figma`, `search_design_system` or `icon_create` do not
exist here. Everything is done with the tools below plus the app's command catalog.

Authoritative docs: `docs/mcp.md` in `storytold/figcraft` (`gh api repos/storytold/figcraft/contents/docs/mcp.md -H 'Accept: application/vnd.github.raw'`).
Live docs from the server itself: `list_commands {filter}`, the resource `figcraft://command/<id>`, and the prompts below.

## Skill Boundaries

- Load this skill first for **any** FigCraft app task; the other `figcraft-app:*` skills assume it.
  Which skill does what: [references/skill-map.md](references/skill-map.md).
- Building UI → `figcraft-app:create-ui` (no design system) or `figcraft-app:generate-design` (reuse one).
- Building a design system → `figcraft-app:generate-library`.
- Checking quality → `figcraft-app:design-review` (critique) and `figcraft-app:design-lint` (rule checks + fixes).

## 1. Pick the Server

| Server | Command | Use when |
|---|---|---|
| `figcraft-app` | `figcraft-cli mcp --attach 7979` | The user wants to see the work in their open app, or the work is on a file they have open. Changes show live. |
| `figcraft` | `figcraft-cli mcp` | Scratch work, exports, experiments, CI-style renders. One untitled in-process document; nothing is visible to the user until saved. |

- Tool names carry the server name: `mcp__figcraft-app__…` when registered by hand, `mcp__plugin_figcraft-app_figcraft-app__…`
  when this plugin registers it. If both exist: the two attached servers reach the same app, but two
  headless servers are two separate in-process documents — keep one task on one server.
- Check the attached app first: `inspect_ui {}` (large; read `status` — file, path, page, selection,
  `dirty` — and `presenting`). A `CONNECTION_CLOSED` or "request was not sent" error means
  the app isn't listening. Tell the user to start it with the control port and **stop**; don't silently move
  their task to headless:

  ```bash
  open -a FigCraft --args --control 7979
  ```

- Headless work is lost unless saved: finish with `save_file {path: "<abs>.figcraft"}` or `export {path}`.
- An attached call that failed in transport **may have been applied**. Inspect before retrying an edit; never
  blindly resend.
- The attached app answers while minimised; only `screenshot {window: true}` needs the window on screen.

## 2. Name the Document

With the app attached, the user can click another tab mid-task. Pin every call to one file:

1. `run_command {command: "doc.list"}` → each open file's `id`, name and state.
2. Pass `document: <id or path>` to `run_command`, `batch`, `create_node`, `set_properties`, `get_node`,
   `inspect_document`, `select`, `export`, `screenshot`, `save_file`, `undo`, `redo`.

Skip this only for headless sessions with one document.

## 3. Model You Must Respect

- Page units, 1 unit = 1 px at 100%, **x right, y down**.
- `create_node` / `set_properties` `x`, `y` are **relative to the parent frame** (the page when there is none).
  Groups have no coordinate space; `absoluteBounds` in `get_node` is page coordinates.
- Children of an auto layout frame are placed by the layout. Set `layout`, `gap`, `padding`, `mainAlign`,
  `crossAlign`, `sizingH`, `sizingV` instead of `x`/`y`.
- `layout` applies before the keys that tune it in the same call: `{"layout": "vertical", "gap": 8}` is fine.
- `sizingH` / `sizingV`: `fixed`, `hug` (auto layout frames and text), `fill` (children of auto layout).
  A child can't fill an axis its parent hugs: setting `fill` turns the parent `fixed` on that axis.
- Every mutation is one undo step; `batch` makes many one step. A failing command changes nothing.
- Every menu action is a command (`list_commands {filter}`); most act on `ids`, else the selection.
  New layers become the selection.
- Colours are `"#RRGGBB"` / `"#RRGGBBAA"`. Gradients: `{"type": "linearGradient", "stops": ["#7048E8", "#1098AD"]}`.
- Programmatic calls never open dialogs.
- Text made by `create_node` is black (white on a dark page when attached) unless `props` names a `fill`.
  Always set text `fill` explicitly.

Full prop list with examples: [references/props.md](references/props.md).

## 4. Build in Batches

`batch {label, commands: [{command, params, as?}]}` runs `node.create`, `node.set`, `variable.bind`, … as one
undo step. Name a step with `"as"` and refer to its `id` later with `{"$ref": "name"}`;
`{"$ref": "name", "field": "ids/0"}` reads another part of the result. `{"$step": n}` refers by position.

```json
{"label": "Card", "commands": [
  {"command": "node.create", "as": "card", "params": {"type": "frame", "name": "Card", "width": 320,
    "props": {"fill": "#FFFFFF", "layout": "vertical", "padding": 24, "gap": 12, "sizingV": "hug", "cornerRadius": 16}}},
  {"command": "node.create", "params": {"type": "text", "parent": {"$ref": "card"}, "text": "Ada Lovelace",
    "props": {"fontSize": 24, "fontStyle": "Bold", "fill": "#111827", "sizingH": "fill"}}}
]}
```

- Default `onError: "abort"` rolls the whole batch back and names the failing step. Fix that step and resend
  the whole batch; nothing from the failed attempt exists.
- `"onError": "continue"` returns `{step, ok, result|error}` per step, for bulk edits where one bad layer
  shouldn't block the rest.
- After one failure, check every remaining planned payload for the same mistake before retrying.
- Never guess ids. Use ids from results, `get_node`, `inspect_document` or `doc.list`.

## 5. Find Layers

- `inspect_document {depth}` for the current page tree; `get_node {id, depth}` for one subtree.
  Large trees come back shallower with a `truncated` object; drill down with `get_node` instead of raising depth.
- `node.find {root?, type?, name?, text?, component?, limit?}` searches without changing the selection
  (needs a newer figcraft-cli, see §9). Fallback: walk `get_node` and filter yourself.
- `component.list`, `style.list {type?}`, `variable.list`, `page.list`, `library.list {assets: true}` for assets.
- `selection.colors {ids}` lists every paint under a layer with its style/variable (`null` = hardcoded).
- `inspect.properties {id}` gives layout, typography, fills, strokes and effects with their token names.

## 6. Verify Every Step

1. Numbers: `get_node {id, depth: 2}` — sizes, `sizing`, `layout`, `boundVariables`, `componentProperties`.
2. Pixels: `screenshot {ids: [id], maxSize: 1200}` after each screen or component. Look at it.
3. Rules: `figcraft-app:design-lint` on finished screens.

Never report a design as done without at least one screenshot of it.

## 7. Files, Templates and Pages

| Task | Call |
|---|---|
| New blank file | `run_command file.new {name}` |
| Start from a template | `run_command template.list`, then `file.newFromTemplate {template}` (`mobile-app`, `landing-page`, `dashboard`, `design-system`, `wireframe-kit`, `social-posts`, `slides`, `icon-set`) |
| Board (FigJam-like) file | `run_command file.newBoard {name}`, then `board.*` commands |
| Open | `open_file {path}` (`.figcraft`, `.fig`, `.jam`, `.sketch`, `.svg`, REST `.json`, images) |
| Save | `save_file {path}` (first save of a new file needs a path) |
| Pages | `page.add {name}`, `page.list`, `page.rename`, `page.duplicate` |
| Device-sized frame | `frame.create {preset: "iPhone 16 Pro", name}` (`frame.presets` lists all) |
| Checkpoint before big edits | `version.autosave`, then `version.rename {index, name}`; roll back with `version.restore` |

Ask before overwriting or deleting the user's files, pages, components, variables or versions.

## 8. Built-in Prompts

The server ships step-by-step plans (`prompts/get`): `mobile_screen`, `design_system`, `landing_page`,
`prototype_flow`, `fix_comments`, `watch_comments`. Use them as a cross-check of tool order.

## 9. Version Gaps

The doc tracks `main`; the installed CLI may be older (`figcraft-cli --version`). Verified missing in 0.12.1:

| Doc feature | Fallback on older CLIs |
|---|---|
| `node.find` | `get_node`/`inspect_document` and filter by `type`, `name`, `characters` |
| `fields` / `outline` on `inspect_document` / `get_node` | Lower `depth`; read subtrees with `get_node` |
| `{"$var": "Collection/name"}` inside `fill`/`stroke` props | Create with a hex colour, then `variable.bind {ids, field: "fill", variable}` in the same batch |
| `comment.prompt` | `comment.list {page: "all", filter: "open"}` |
| `image.replace`, `image.crop` | `image.place {path, target: <layer>}`; edit the paint's `crop` with `fill.set` |
| `variable.extendCollection` | `library.extendCollection` (library collections only) or duplicate the collection |
| `library.check` | `library.updates` |
| `{prop ? "a" : "b"}` in `codeConnect.set` templates | plain `{prop}` placeholders |

Unknown command → `list_commands {filter}` to find the current id before giving up.
