---
name: spec-compare
description: "Compare a DTCG design token spec against the FigCraft app's variables (local or an enabled library's) and report drift: in sync, different, missing in FigCraft, missing in the spec. Use when: compare/diff/check + tokens/spec/DTCG + FigCraft variables, or when auditing token drift between code and the FigCraft file. Read-only; hands syncing to figcraft-app:token-sync."
---

# FigCraft App — Spec Compare

Read-only diff between DTCG files and FigCraft variables. Load `figcraft-app:use` first.

## Skill Boundaries

- Compare → this skill. Sync → `figcraft-app:token-sync`. Create variables from scratch →
  `figcraft-app:generate-library`.

## Workflow

1. **Connect** — `inspect_ui {}` / `doc.list`. Ask for the DTCG file(s) (one file per mode) and the
   collection to compare.
2. **Export FigCraft's side** — `run_command variable.export {format: "json", collections: ["<name>"], path: "<scratchpad>/figcraft.json"}`.
   Library variables aren't exported by this; for an enabled library, open the library file
   (`open_file {path}`) and export there, or compare against `library.list {assets: true}` by hand.
3. **Diff** — the converter ships with the `figcraft-app:token-sync` skill: `<token-sync-dir>` is the
   `token-sync` folder next to this skill's base directory (`<this skill's base directory>/../token-sync`).


   ```bash
   python3 -I <token-sync-dir>/scripts/dtcg.py diff \
     --collection "<name>" --mode Light=tokens/light.json [--mode Dark=tokens/dark.json] <scratchpad>/figcraft.json
   ```

   Composite tokens (typography, shadow) aren't in the diff: compare them with `style.list`
   (text styles' `font_family`, `font_size`, `line_height`; effect styles' `effects`).
4. **Report**

   ```
   Token drift — <collection>          in sync N · different N · missing in FigCraft N · missing in spec N
   Different:   color/bg/primary   Dark: spec #0B0F19 · FigCraft #111111
   Missing in FigCraft:  space/72, radius/xl
   Missing in spec:      color/legacy/teal
   Styles:      Heading/H1 lineHeight spec 120% · FigCraft 125%
   ```

   Recommend per category:
   - different → decide per token which side wins (neither file records which is newer)
   - missing in FigCraft → `figcraft-app:token-sync`
   - missing in spec → add it to the spec, or delete it in FigCraft (`variable.delete`, after asking)
   - spec should follow FigCraft → `variable.export` + `dtcg.py from-figcraft`
5. **Offer to sync** — on yes, hand off to `figcraft-app:token-sync`.

Mode names must match between the DTCG `--mode` names and the collection's modes (`variable.list`);
a mismatch shows every token as different.
