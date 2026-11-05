#!/usr/bin/env python3
"""DTCG design tokens <-> FigCraft app local variables JSON.

The FigCraft app's `variable.import` / `variable.export {format: "json"}` use the REST "local
variables" shape: {"meta": {"variableCollections": {...}, "variables": {...}}}.

  to-figcraft  --collection NAME --mode Light=light.json [--mode Dark=dark.json] [-o out.json]
               Variables JSON for variable.import (atomic tokens), plus a styles list for the
               composite tokens (typography, shadow) written next to it as <out>.styles.json.
  from-figcraft EXPORT.json [--collection NAME] [-o tokens.json]
               DTCG tokens from a variable.export JSON (one file; modes under $extensions).
  diff         --collection NAME --mode Light=light.json [...] EXPORT.json
               In-sync / different / missing-on-either-side report.

A DTCG file is one mode. Token paths become slash names: color.bg.primary -> color/bg/primary.
"""
import argparse
import json
import re
import sys

ATOMIC = {"color": "COLOR", "dimension": "FLOAT", "number": "FLOAT", "fontWeight": "FLOAT",
          "duration": "FLOAT", "fontFamily": "STRING", "string": "STRING", "boolean": "BOOLEAN"}
COMPOSITE = {"typography", "shadow", "border", "gradient", "transition", "strokeStyle"}
ALIAS = re.compile(r"^\{([^}]+)\}$")


def walk(node, path=(), inherited_type=None):
    """Yield (path, token) for every token in a DTCG tree."""
    if not isinstance(node, dict):
        return
    t = node.get("$type", inherited_type)
    if "$value" in node:
        yield path, {"type": t, "value": node["$value"], "description": node.get("$description", "")}
        return
    for k, v in node.items():
        if not k.startswith("$"):
            yield from walk(v, path + (k,), t)


def load_modes(pairs):
    modes = {}
    for pair in pairs:
        name, _, file = pair.partition("=")
        if not file:
            sys.exit(f"--mode expects Name=file.json, got {pair!r}")
        with open(file) as f:
            modes[name] = dict(walk(json.load(f)))
    return modes


def hex_to_rgba(value):
    if isinstance(value, dict):  # DTCG 2025 colour object
        comps = value.get("components", [0, 0, 0])
        return {"r": comps[0], "g": comps[1], "b": comps[2], "a": value.get("alpha", 1.0)}
    s = str(value).strip().lstrip("#")
    if len(s) in (3, 4):
        s = "".join(c * 2 for c in s)
    if not re.fullmatch(r"[0-9a-fA-F]{6}([0-9a-fA-F]{2})?", s):
        raise ValueError(f"not a hex colour: {value!r}")
    r, g, b = (int(s[i:i + 2], 16) / 255 for i in (0, 2, 4))
    a = int(s[6:8], 16) / 255 if len(s) == 8 else 1.0
    return {"r": r, "g": g, "b": b, "a": a}


def rgba_to_hex(c):
    h = "#" + "".join(f"{round(c[k] * 255):02X}" for k in ("r", "g", "b"))
    return h + (f"{round(c.get('a', 1) * 255):02X}" if c.get("a", 1) < 1 else "")


def to_number(value):
    if isinstance(value, dict):  # {"value": 16, "unit": "px"}
        return float(value.get("value", 0)) * (16 if value.get("unit") == "rem" else 1)
    s = str(value).strip()
    m = re.fullmatch(r"(-?[\d.]+)(px|rem|ms|s)?", s)
    if not m:
        raise ValueError(f"not a number: {value!r}")
    n = float(m.group(1))
    return n * 16 if m.group(2) == "rem" else n * 1000 if m.group(2) == "s" else n


def guess_scopes(name, rtype):
    n = name.lower()
    if rtype == "COLOR":
        if re.search(r"(^|/)(bg|background|surface|fill|canvas)", n):
            return ["FRAME_FILL", "SHAPE_FILL"]
        if re.search(r"(^|/)(text|fg|foreground|on-|icon)", n):
            return ["TEXT_FILL"] if "icon" not in n else ["SHAPE_FILL", "STROKE_COLOR"]
        if re.search(r"(^|/)(border|stroke|outline|divider)", n):
            return ["STROKE_COLOR"]
        return None
    if rtype == "FLOAT":
        if re.search(r"(space|spacing|gap|padding|inset)", n):
            return ["GAP"]
        if "radius" in n or "radii" in n:
            return ["CORNER_RADIUS"]
        if re.search(r"(font-?size|size/text)", n):
            return ["FONT_SIZE"]
        return None
    return None


def to_figcraft(args):
    modes = load_modes(args.mode)
    mode_names = list(modes)
    cid = "VariableCollectionId:import"
    mode_ids = {m: f"{cid}/{i + 1}" for i, m in enumerate(mode_names)}
    names = {}
    for tokens in modes.values():
        for path, tok in tokens.items():
            names.setdefault(path, tok)
    variables, styles, report = {}, [], {"variables": 0, "styles": 0, "skipped": [], "ALL_SCOPES": []}
    vid = {path: f"VariableID:import/{i}" for i, path in enumerate(names)}
    for path, first in names.items():
        name = "/".join(path)
        t = first["type"]
        if t in COMPOSITE:
            styles.append({"name": name, "type": t, "values": {m: modes[m].get(path, {}).get("value") for m in mode_names}})
            continue
        rtype = ATOMIC.get(t)
        if rtype is None:
            report["skipped"].append(f"{name} ($type {t!r})")
            continue
        by_mode = {}
        for m in mode_names:
            tok = modes[m].get(path) or first
            v = tok["value"]
            alias = ALIAS.match(v) if isinstance(v, str) else None
            if alias:
                target = tuple(alias.group(1).split("."))
                if target not in vid:
                    report["skipped"].append(f"{name}: alias to unknown {alias.group(1)}")
                    break
                by_mode[mode_ids[m]] = {"type": "VARIABLE_ALIAS", "id": vid[target]}
            elif rtype == "COLOR":
                by_mode[mode_ids[m]] = hex_to_rgba(v)
            elif rtype == "FLOAT":
                by_mode[mode_ids[m]] = to_number(v)
            elif rtype == "BOOLEAN":
                by_mode[mode_ids[m]] = bool(v)
            else:
                by_mode[mode_ids[m]] = v if isinstance(v, str) else ", ".join(map(str, v))
        else:
            scopes = guess_scopes(name, rtype)
            if scopes is None:
                report["ALL_SCOPES"].append(name)
            variables[vid[path]] = {
                "id": vid[path], "name": name, "resolvedType": rtype, "variableCollectionId": cid,
                "description": first.get("description", ""), "scopes": scopes or ["ALL_SCOPES"],
                "codeSyntax": {"WEB": "var(--" + "-".join(path) + ")"},
                "hiddenFromPublishing": False, "valuesByMode": by_mode,
            }
    out = {"meta": {
        "variableCollections": {cid: {
            "id": cid, "name": args.collection, "defaultModeId": mode_ids[mode_names[0]],
            "modes": [{"modeId": mode_ids[m], "name": m} for m in mode_names],
            "variableIds": list(variables), "hiddenFromPublishing": False}},
        "variables": variables}}
    report["variables"], report["styles"] = len(variables), len(styles)
    text = json.dumps(out, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(text)
        with open(re.sub(r"\.json$", "", args.output) + ".styles.json", "w") as f:
            json.dump(styles, f, indent=2)
    else:
        print(text)
    print(json.dumps(report, indent=2), file=sys.stderr)


def read_export(file, collection=None):
    with open(file) as f:
        data = json.load(f)
    if "text" in data and isinstance(data["text"], str):  # raw MCP result
        data = json.loads(data["text"])
    meta = data.get("meta", data)
    cols, variables = meta["variableCollections"], meta["variables"]
    by_id = {v["id"]: v for v in variables.values()}
    result = {}
    for v in variables.values():
        col = cols[v["variableCollectionId"]]
        if collection and col["name"] != collection:
            continue
        modes = {m["modeId"]: m["name"] for m in col["modes"]}
        vals = {}
        for mid, val in v["valuesByMode"].items():
            if isinstance(val, dict) and val.get("type") == "VARIABLE_ALIAS":
                target = by_id.get(val["id"])
                vals[modes[mid]] = "{" + target["name"].replace("/", ".") + "}" if target else None
            elif v["resolvedType"] == "COLOR":
                vals[modes[mid]] = rgba_to_hex(val)
            else:
                vals[modes[mid]] = val
        result[tuple(v["name"].split("/"))] = {"type": v["resolvedType"], "values": vals}
    return result


def from_figcraft(args):
    tree = {}
    back = {"COLOR": "color", "FLOAT": "number", "STRING": "string", "BOOLEAN": "boolean"}
    for path, v in read_export(args.export, args.collection).items():
        node = tree
        for p in path[:-1]:
            node = node.setdefault(p, {})
        modes = list(v["values"])
        tok = {"$type": back[v["type"]], "$value": v["values"][modes[0]]}
        if len(modes) > 1:
            tok["$extensions"] = {"figcraft.modes": v["values"]}
        node[path[-1]] = tok
    text = json.dumps(tree, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(text)
    else:
        print(text)


def norm(v):
    if isinstance(v, str) and re.fullmatch(r"#?[0-9a-fA-F]{3,8}", v.strip()):
        return rgba_to_hex(hex_to_rgba(v))
    try:
        return round(to_number(v), 3)
    except (ValueError, TypeError):
        return v


def diff(args):
    modes = load_modes(args.mode)
    fig = read_export(args.export, args.collection)
    report = {"inSync": [], "different": [], "missingInFigcraft": [], "missingInDtcg": []}
    paths = set()
    for tokens in modes.values():
        paths |= {p for p, t in tokens.items() if t["type"] not in COMPOSITE}
    for p in sorted(paths):
        name = "/".join(p)
        if p not in fig:
            report["missingInFigcraft"].append(name)
            continue
        changes = []
        for m, tokens in modes.items():
            d = tokens.get(p, {}).get("value")
            f = fig[p]["values"].get(m)
            if norm(d) != norm(f):
                changes.append({"mode": m, "dtcg": d, "figcraft": f})
        (report["different"].append({"name": name, "changes": changes}) if changes else report["inSync"].append(name))
    report["missingInDtcg"] = sorted("/".join(p) for p in fig if p not in paths)
    report["summary"] = {k: len(v) for k, v in report.items()}
    print(json.dumps(report, indent=2))
    print("Note: neither file says which side is newer; decide with the user which wins for each `different` token.", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("to-figcraft")
    a.add_argument("--collection", required=True)
    a.add_argument("--mode", action="append", required=True)
    a.add_argument("-o", "--output")
    a.set_defaults(fn=to_figcraft)
    b = sub.add_parser("from-figcraft")
    b.add_argument("export")
    b.add_argument("--collection")
    b.add_argument("-o", "--output")
    b.set_defaults(fn=from_figcraft)
    c = sub.add_parser("diff")
    c.add_argument("--collection", required=True)
    c.add_argument("--mode", action="append", required=True)
    c.add_argument("export")
    c.set_defaults(fn=diff)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
