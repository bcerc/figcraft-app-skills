# FigCraft App Skills — Map

Ported from the skills of the FigCraft **Figma plugin** (`DivikWu/figcraft`, `skills/`), rewritten for the
FigCraft **app**'s MCP server (`storytold/figcraft`, `docs/mcp.md`). The plugin's tools (`get_mode`,
`create_frame`, `lint_fix_all`, `use_figma`, `icon_create`, `search_design_system`, …) don't exist in the app.

| App skill | Plugin skill | Notes |
|---|---|---|
| **Foundation** | | |
| `figcraft-app:use` | `figcraft-use`, `figcraft-create-new-file` | MCP rules replace the Figma Plugin API rules |
| `figcraft-app:ui-ux-fundamentals` | `ui-ux-fundamentals` | rules carried over |
| `figcraft-app:design-creator` | `design-creator` | no-system mode |
| `figcraft-app:design-guardian` | `design-guardian` | system/library mode |
| **Create** | | |
| `figcraft-app:create-ui` | `figma-create-ui` | `batch` + `node.create` instead of `create_frame` |
| `figcraft-app:generate-design` | `figcraft-generate-design` | discovery via `component.list`, `variable.list`, `library.list` |
| `figcraft-app:generate-library` | `figcraft-generate-library` | variables, styles, components, `library.publish` |
| `figcraft-app:import` | `figcraft-html-import` | SVG/.fig/.sketch/REST JSON; HTML is rebuilt |
| **Quality** | | |
| `figcraft-app:design-review` | `design-review` | |
| `figcraft-app:design-lint` | `design-lint` | the 41 rules, checked by the agent |
| `figcraft-app:component-docs` | `component-docs` | |
| `figcraft-app:prototype-analysis` | `prototype-analysis` | graph built from `interactions` |
| `figcraft-app:text-replace` | `text-replace` | plus `data.fill`, `text.fit` |
| `figcraft-app:token-sync` | `token-sync` | `scripts/dtcg.py` + `variable.import` |
| `figcraft-app:spec-compare` | `spec-compare` | `dtcg.py diff` |
| **Patterns** | | |
| `figcraft-app:responsive-design` | `responsive-design` | |
| `figcraft-app:content-states` | `content-states` | |
| `figcraft-app:iconography` | `iconography` | SVG import / icon components, no icon search |
| `figcraft-app:multi-screen-flow` | `multi-screen-flow` | |
| `figcraft-app:design-handoff` | `design-handoff` | the app's Dev Mode: annotations, measurements, status |
| `figcraft-app:platform-ios` | `platform-ios` | |
| `figcraft-app:platform-android` | `platform-android` | |
| `figcraft-app:ux-writing` | `ux-writing` | |
| **Advanced** | | |
| `figcraft-app:design-system-audit` | `design-system-audit` | |
| `figcraft-app:migration-assistant` | `migration-assistant` | `library.swap`, version checkpoints |
| `figcraft-app:multi-brand` | `multi-brand` | modes + extended collections |
| **Code** | | |
| `figcraft-app:implement-design` | `figcraft-implement-design` | `inspect.code` generates the first draft |
| `figcraft-app:code-connect` | `figcraft-code-connect` | `codeConnect.set` templates, `figcraft.connect.json` |
| `figcraft-app:create-design-system-rules` | `figcraft-create-design-system-rules` | |

Quality loop: `figcraft-app:create-ui` → `figcraft-app:design-review` → `figcraft-app:design-lint`.
