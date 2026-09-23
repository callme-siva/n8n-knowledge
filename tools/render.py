"""Render a workflow JSON into (1) an n8n-style canvas snapshot SVG and (2) a Mermaid architecture diagram."""
import re
from html import escape

# category → (fill, stroke, glyph)
CATS = {
    "trigger": ("#E8F7EE", "#2EA44F", "⚡"),
    "ai":      ("#F1EBFF", "#7C3AED", "✦"),
    "sub":     ("#F7F3FF", "#A78BFA", "◆"),
    "logic":   ("#FFF4E5", "#F59E0B", "⑂"),
    "code":    ("#EEF2F7", "#64748B", "{ }"),
    "data":    ("#EAF3FF", "#2563EB", "▦"),
    "http":    ("#E6FAF8", "#0D9488", "⇄"),
    "msg":     ("#FFEDEF", "#E11D48", "✉"),
}
GLYPH = {"gmail": "✉", "googleSheets": "▦", "googleDrive": "▲", "jira": "◆", "httpRequest": "⇄", "rssFeedRead": "◉",
         "webhook": "⚓", "formTrigger": "☰", "scheduleTrigger": "◷", "manualTrigger": "▶", "gmailTrigger": "✉",
         "errorTrigger": "⚠", "chatTrigger": "💬", "if": "⑂", "switch": "⑃", "filter": "⊻", "merge": "⊕", "code": "{ }",
         "set": "✎", "wait": "⏸", "splitInBatches": "⟳", "limit": "⤓", "removeDuplicates": "⧉", "aggregate": "Σ", "crypto": "#", "quickChart": "▮", "html": "</>", "googleCalendar": "📅", "telegram": "✈", "telegramTrigger": "✈", "slack": "#", "textClassifier": "⑃", "informationExtractor": "✦", "mcpTrigger": "⚡", "toolWorkflow": "↗", "toolSerpApi": "🔍", "splitOut": "⇶", "noOp": "→", "stopAndError": "⛔", "respondToWebhook": "↩", "executeWorkflow": "↗",
         "executeWorkflowTrigger": "↘", "extractFromFile": "⎙", "agent": "🤖", "chainLlm": "✦",
         "lmChatGoogleGemini": "G", "outputParserStructured": "{}", "memoryBufferWindow": "🧠", "toolCalculator": "±",
         "toolWikipedia": "W", "toolHttpRequest": "⇄", "vectorStoreInMemory": "▤", "embeddingsGoogleGemini": "≋",
         "documentDefaultDataLoader": "⎘", "textSplitterRecursiveCharacterTextSplitter": "✂"}


def wrap(text, maxc):
    out, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > maxc:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out or [""]


def short(t):
    return t.split(".")[-1]


MAIN_TARGETS = set()


def cat(n):
    s = short(n["type"])
    if "@n8n/n8n-nodes-langchain" in n["type"]:
        if s in ("agent", "chainLlm") or n["name"] in MAIN_TARGETS:
            return "ai"
        if s.endswith("Trigger"):
            return "trigger"
        return "sub"
    if re.search(r"[Tt]rigger$|^webhook$", s):
        return "trigger"
    if s in ("if", "switch", "filter", "merge", "noOp", "stopAndError", "splitOut", "wait", "splitInBatches", "limit", "removeDuplicates", "aggregate"):
        return "logic"
    if s in ("code", "set"):
        return "code"
    if s in ("googleSheets", "googleDrive", "jira", "extractFromFile"):
        return "data"
    if s in ("httpRequest", "rssFeedRead", "respondToWebhook", "executeWorkflow"):
        return "http"
    return "msg"


def _edges(wf):
    for src, kinds in wf["connections"].items():
        for kind, outs in kinds.items():
            for oi, out in enumerate(outs):
                for c in out or []:
                    yield src, c["node"], kind, oi


def _out_labels(n):
    s, p = short(n["type"]), n["parameters"]
    if s == "if":
        return ["true", "false"]
    if s == "switch":
        labs = [r.get("outputKey", f"{i}") for i, r in enumerate(p.get("rules", {}).get("values", []))]
        if p.get("options", {}).get("fallbackOutput") == "extra":
            labs.append(p["options"].get("renameFallbackOutput", "fallback"))
        return labs
    return []


# ---------------------------------------------------------------- SVG canvas
def _mark(wf):
    MAIN_TARGETS.clear()
    MAIN_TARGETS.update(dst for _, dst, k, _ in _edges(wf) if k == "main")


def _note_rows(p):
    w = p.get("width", 380)
    raw = [l for l in (re.sub(r"[*`#_>]", "", l).strip() for l in p["content"].split("\n")) if l]
    return [(wrap(raw[0], int(w / 8.4)), 15, 700, 22)] + [(wrap(l, int(w / 6.9)), 12.5, 400, 17) for l in raw[1:]]


def _note_h(p):
    return 22 + sum(len(r[0]) * r[3] for r in _note_rows(p)) + 6


FOLD_WIDTH = 1250  # canvases wider than this (in n8n units) are folded into two rows


def _fold(wf, nodes):
    """Fold a very wide workflow into rows. Returns (nodes, row_of, gutters) where gutters[r] is the y of the lane above row r."""
    import math
    main = [n for n in nodes if cat(n) != "sub"]
    xs = sorted({n["position"][0] for n in main})
    if not xs or xs[-1] - xs[0] <= FOLD_WIDTH:
        return nodes, {n["name"]: 0 for n in nodes}, {}
    k = math.ceil((xs[-1] - xs[0]) / FOLD_WIDTH)
    width = (xs[-1] - xs[0]) / k
    # row boundaries snap to real node columns so no column is cut in half
    starts = [xs[0]] + [min(xs, key=lambda x: abs(x - (xs[0] + i * width))) for i in range(1, k)]
    parent = {src: dst for src, dst, kd, _ in _edges(wf) if kd != "main"}
    pos = {n["name"]: n["position"][0] for n in nodes}
    def home_x(n):  # sub-nodes follow the node they plug into
        name = n["name"]
        for _ in range(3):
            name = parent.get(name, name)
        return pos.get(name, n["position"][0])
    row = {n["name"]: max(i for i, st in enumerate(starts) if home_x(n) >= st) for n in nodes}
    out, gutters, y_offset, prev_bottom = [], {}, 0, None
    for r in range(k):
        members = [n for n in nodes if row[n["name"]] == r]
        if not members:
            continue
        top = min(n["position"][1] for n in members)
        if prev_bottom is not None:
            y_offset = prev_bottom + 120 - top
            gutters[r] = prev_bottom + 55
        moved = [dict(n, position=[n["position"][0] - (starts[r] - xs[0]), n["position"][1] + y_offset]) for n in members]
        out += moved
        prev_bottom = max(n["position"][1] + (98 if cat(n) == "sub" else 146) for n in moved)
    return out, row, gutters


def canvas_svg(wf):
    _mark(wf)
    nodes = [n for n in wf["nodes"] if "stickyNote" not in n["type"]]
    notes = [n for n in wf["nodes"] if "stickyNote" in n["type"]]
    nodes, row, gutter = _fold(wf, nodes)
    by = {n["name"]: n for n in nodes}
    top = min(n["position"][1] for n in nodes)
    notes = [dict(n, position=[n["position"][0], top - 40 - _note_h(n["parameters"])]) for n in notes]
    S = 100  # main node size
    size = lambda n: 64 if cat(n) == "sub" else S
    xs, ys = [], []
    for n in nodes:
        x, y = n["position"]; s = size(n)
        xs += [x - 20, x + s + 40]; ys += [y - 20, y + s + 46]
    for n in notes:
        x, y = n["position"]; p = n["parameters"]
        xs += [x, x + p.get("width", 380)]; ys += [y, y + _note_h(p)]
    pad = 40
    minx, miny = min(xs) - pad, min(ys) - pad - 36
    W, H = max(xs) - minx + pad, max(ys) - miny + pad
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{minx} {miny} {W} {H}" width="{min(W, 1400)}" font-family="Inter,Segoe UI,Helvetica,Arial,sans-serif">',
         '<defs><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#D5D9E0"/></pattern>'
         '<filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity=".10"/></filter>'
         '<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#94A3B8"/></marker></defs>',
         f'<rect x="{minx}" y="{miny}" width="{W}" height="{H}" rx="14" fill="#F8FAFC"/>',
         f'<rect x="{minx}" y="{miny}" width="{W}" height="{H}" rx="14" fill="url(#dots)"/>',
         f'<rect x="{minx}" y="{miny}" width="{W}" height="36" rx="14" fill="#1F2937"/><rect x="{minx}" y="{miny + 20}" width="{W}" height="16" fill="#1F2937"/>',
         f'<circle cx="{minx + 20}" cy="{miny + 18}" r="5" fill="#FF5F57"/><circle cx="{minx + 38}" cy="{miny + 18}" r="5" fill="#FEBC2E"/><circle cx="{minx + 56}" cy="{miny + 18}" r="5" fill="#28C840"/>',
         f'<text x="{minx + 76}" y="{miny + 23}" font-size="13" fill="#E5E7EB" font-weight="600">{escape(wf["name"])}</text>']
    # sticky notes
    for n in notes:
        x, y = n["position"]; p = n["parameters"]; w = p.get("width", 380)
        rows, h = _note_rows(p), _note_h(p)
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#FFF8DB" stroke="#F2D675"/>')
        ty = y + 28
        for lines, fs, fw, lh in rows:
            for c in lines:
                o.append(f'<text x="{x + 14}" y="{ty}" font-size="{fs}" fill="#5B4B12" font-weight="{fw}">{escape(c)}</text>')
                ty += lh
    # edges
    for src, dst, kind, oi in _edges(wf):
        if src not in by or dst not in by:
            continue
        a, b = by[src], by[dst]
        if kind == "main":
            nout = max(1, len(wf["connections"][src]["main"]))
            sy = a["position"][1] + S * (oi + 1) / (nout + 1)
            x1, y1 = a["position"][0] + S, sy
            x2, y2 = b["position"][0], b["position"][1] + (S / 2 if cat(b) != "sub" else 32)
            if x2 < x1 + 10 or row.get(src) != row.get(dst):  # backwards, loop, or changes row → route through a gutter lane
                gy = gutter.get(row.get(dst)) if row.get(src) != row.get(dst) and row.get(dst) in gutter else max(a["position"][1], b["position"][1]) + S + 60
                path = f"M{x1},{y1} H{x1 + 24} Q{x1 + 34},{y1} {x1 + 34},{y1 + 10} V{gy - 10} Q{x1 + 34},{gy} {x1 + 24},{gy} H{x2 - 34} Q{x2 - 44},{gy} {x2 - 44},{gy + (10 if y2 > gy else -10)} V{y2 + (-10 if y2 > gy else 10)} Q{x2 - 44},{y2} {x2 - 34},{y2} H{x2 - 4}"
            else:
                dx = max(40, abs(x2 - x1) / 2)
                path = f"M{x1},{y1} C{x1 + dx},{y1} {x2 - dx},{y2} {x2 - 4},{y2}"
            o.append(f'<path d="{path}" stroke="#94A3B8" stroke-width="2" fill="none" marker-end="url(#arr)"/>')
            labs = _out_labels(a)
            if len(labs) > oi and nout > 1:
                o.append(f'<text x="{x1 + 8}" y="{y1 - 5}" font-size="11" fill="#64748B">{escape(labs[oi])}</text>')
        else:
            s = size(a)
            x1, y1 = a["position"][0] + s / 2, a["position"][1]
            x2 = b["position"][0] + (32 if cat(b) == "sub" else S / 2)
            y2 = b["position"][1] + (S + 34 if cat(b) != "sub" else 98)
            o.append(f'<path d="M{x1},{y1} C{x1},{(y1 + y2) / 2} {x2},{(y1 + y2) / 2} {x2},{y2 + 2}" stroke="#A78BFA" stroke-width="1.6" stroke-dasharray="5 4" fill="none"/>')
    # nodes
    for n in nodes:
        x, y = n["position"]; c = cat(n); fill, stroke, _ = CATS[c]; g = GLYPH.get(short(n["type"]), CATS[c][2])
        if c == "sub":
            o.append(f'<circle cx="{x + 32}" cy="{y + 32}" r="32" fill="{fill}" stroke="{stroke}" stroke-width="2" filter="url(#sh)"/>')
            o.append(f'<text x="{x + 32}" y="{y + 39}" font-size="19" text-anchor="middle" fill="{stroke}" font-weight="700">{escape(g)}</text>')
            cx, ty = x + 32, y + 84
        else:
            rx = "10"
            o.append(f'<rect x="{x}" y="{y}" width="{S}" height="{S}" rx="{rx}" fill="#FFFFFF" stroke="{stroke}" stroke-width="2" filter="url(#sh)"/>')
            if c == "trigger":
                o.append(f'<path d="M{x + 30},{y} H{x + 10} A10,10 0 0 0 {x},{y + 10} V{y + S - 10} A10,10 0 0 0 {x + 10},{y + S} H{x + 30}" fill="none" stroke="{stroke}" stroke-width="5"/>')
            o.append(f'<rect x="{x + 22}" y="{y + 18}" width="56" height="56" rx="12" fill="{fill}"/>')
            o.append(f'<text x="{x + 50}" y="{y + 55}" font-size="{24 if len(g) < 3 else 16}" text-anchor="middle" fill="{stroke}" font-weight="700">{escape(g)}</text>')
            cx, ty = x + S / 2, y + S + 20
        parts = wrap(n["name"], 13 if c == "sub" else 18)[:2]
        for i, p in enumerate(parts):
            p = p if len(p) <= 20 else p[:19] + "…"
            o.append(f'<text x="{cx}" y="{ty + i * 15}" font-size="12.5" text-anchor="middle" fill="#1F2937" font-weight="600">{escape(p)}</text>')
    o.append("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------- Mermaid
def mermaid(wf):
    _mark(wf)
    nodes = [n for n in wf["nodes"] if "stickyNote" not in n["type"]]
    ids = {n["name"]: f"n{i}" for i, n in enumerate(nodes)}
    lab = lambda s: s.replace('"', "'")
    main = [n for n in nodes if cat(n) != "sub"]
    L = ["```mermaid", "flowchart " + ("TB" if len(main) > 5 else "LR")]
    for n in nodes:
        i, c, s = ids[n["name"]], cat(n), lab(n["name"])
        shape = {"trigger": f'{i}(["{s}"])', "ai": f'{i}[["{s}"]]', "sub": f'{i}("{s}")',
                 "logic": f'{i}{{"{s}"}}' if short(n["type"]) in ("if", "switch", "filter") else f'{i}["{s}"]'}.get(c, f'{i}["{s}"]')
        L.append(f"  {shape}:::{c}")
    by = {n["name"]: n for n in nodes}
    for src, dst, kind, oi in _edges(wf):
        if src not in ids or dst not in ids:
            continue
        if kind == "main":
            labs = _out_labels(by[src])
            L.append(f'  {ids[src]} -->|"{lab(labs[oi])}"| {ids[dst]}' if len(labs) > oi and len(wf["connections"][src]["main"]) > 1 else f"  {ids[src]} --> {ids[dst]}")
        else:
            L.append(f'  {ids[src]} -.->|{kind.replace("ai_", "")}| {ids[dst]}')
    for c, (fill, stroke, _) in CATS.items():
        L.append(f"  classDef {c} fill:{fill},stroke:{stroke},stroke-width:2px,color:#1F2937")
    L.append("```")
    return "\n".join(L)
