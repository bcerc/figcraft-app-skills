# FigCraft App Skills

A Claude Code plugin that teaches agents to design with the **FigCraft app** through its MCP server
(`figcraft-cli mcp`): build screens and components, create and audit design systems, lint and review
designs, sync DTCG tokens, analyse prototypes, prepare handoff and turn designs into code.

The skills are adapted from the skill set of the FigCraft **Figma plugin**
([DivikWu/figcraft](https://github.com/DivikWu/figcraft)), rewritten to use the FigCraft app's tools and
command catalog ([storytold/figcraft `docs/mcp.md`](https://github.com/storytold/figcraft/blob/main/docs/mcp.md)).
They don't use Figma or the plugin's tools.

## Requirements

- The FigCraft app, and `figcraft-cli` of the **same version** on your `PATH`
  (`figcraft-cli --version`). Install it from the release matching your app.
- For the attached server, start the app with its control port:

  ```bash
  open -a FigCraft --args --control 7979
  ```

  Launched from the Dock, the port stays closed and the attached server fails with `CONNECTION_CLOSED`.
  The headless server works without the app.
- `python3` for the token converter (`figcraft-app:token-sync`, `figcraft-app:spec-compare`).

## Install

```bash
claude plugin marketplace add bcerc/figcraft-app-skills
```

```bash
claude plugin install figcraft-app@figcraft-app-skills
```

From a local clone instead of GitHub:

```bash
claude plugin marketplace add /path/to/figcraft-app-skills
```

Restart Claude Code afterwards; skills and MCP servers load at session start.

### Already registered the servers by hand?

The plugin registers two servers, `figcraft` (headless) and `figcraft-app` (attached). If you added
servers with the same names via `claude mcp add`, you'll have both copies. They work side by side, but
remove your own to avoid confusion:

```bash
claude mcp remove figcraft -s user
```

```bash
claude mcp remove figcraft-app -s user
```

`figcraft-cli` not on your `PATH` (e.g. in `~/.local/bin`)? Add that folder to `PATH`, or keep your own
`claude mcp add` registrations with the absolute path and ignore the plugin's.

## Skills

Start with `figcraft-app:use`; every other skill builds on it.

| Group | Skills |
|---|---|
| Foundation | `use`, `ui-ux-fundamentals`, `design-creator`, `design-guardian` |
| Create | `create-ui`, `generate-design`, `generate-library`, `import` |
| Quality | `design-review`, `design-lint`, `component-docs`, `prototype-analysis`, `text-replace`, `token-sync`, `spec-compare` |
| Patterns | `responsive-design`, `content-states`, `iconography`, `multi-screen-flow`, `design-handoff`, `platform-ios`, `platform-android`, `ux-writing` |
| Advanced | `design-system-audit`, `migration-assistant`, `multi-brand` |
| Code | `implement-design`, `code-connect`, `create-design-system-rules` |

Each is invoked as `figcraft-app:<name>`. How they map to the Figma plugin's skills:
[`skills/use/references/skill-map.md`](skills/use/references/skill-map.md).

## Version notes

The skills were checked against `figcraft-cli` 0.12.1. Features `docs/mcp.md` describes that 0.12.1 lacks
(`node.find`, `fields`/`outline`, `$var` in props, `comment.prompt`, Code Connect ternaries, …) are listed
with fallbacks in `figcraft-app:use` §9.

## Other agents

Each `skills/<name>/SKILL.md` follows the Agent Skills format, so tools that read it (Codex, Cursor, …) can
load the folders directly. Cross-references use the `figcraft-app:<name>` form.

## License

MIT — see [LICENSE](LICENSE). Portions adapted from DivikWu/figcraft (MIT).
