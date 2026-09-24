"""Draw assets/learning-path.svg: a metro-map roadmap of all three tracks."""
from html import escape

SHORT = {
    "L01": "Hello n8n", "L02": "Schedule + API", "L03": "API auth", "L04": "IF / Switch", "L05": "Code node",
    "L06": "Gmail → Drive", "L07": "Forms + Sheets", "L08": "Jira + JQL", "L09": "Webhook API", "L10": "Form → Jira",
    "L11": "LLM chain", "L12": "Structured output", "L13": "RAG chatbot", "L14": "Agent + tools", "L15": "Human approval",
    "L16": "4 agents", "L17": "5 agents", "L18": "Document AI", "L19": "Error handler", "L20": "Sub-workflows", "L21": "Monitoring", "L22": "Capstone",
    "Q01": "Daily agenda", "Q02": "Price tracker", "Q03": "Telegram bot", "Q04": "Stale PRs", "Q05": "KPI chart",
    "Q06": "Invoice reminders", "Q07": "AI labeler", "Q08": "Autopost",
    "P01": "Invoice pipeline", "P02": "Support copilot", "P03": "Incident response", "P04": "Sales sequence",
    "P05": "Bulk AI, checkpoints", "P06": "Multi-level approval", "P07": "Onboarding", "P08": "Sheets ⇄ Jira sync",
    "P09": "Research agent", "P10": "MCP server", "P11": "PII-safe gateway", "P12": "Exec KPI report",
}
LEVEL_COLOR = [("L01", "L05", "#22C55E"), ("L06", "L10", "#EAB308"), ("L11", "L15", "#F97316"), ("L16", "L22", "#EF4444")]
W = 1280


def color_for(num):
    if num[0] == "Q":
        return "#0EA5E9"
    if num[0] == "P":
        return "#A855F7"
    for a, b, c in LEVEL_COLOR:
        if a <= num <= b:
            return c


def station(o, x, y, num, below=True):
    c = color_for(num)
    o.append(f'<circle cx="{x}" cy="{y}" r="19" fill="#0B1220" stroke="{c}" stroke-width="4"/>')
    o.append(f'<text x="{x}" y="{y + 4.5}" font-size="10" font-weight="800" fill="#F8FAFC" text-anchor="middle">{num}</text>')
    words, lines, cur = SHORT[num].split(), [], ""
    for w_ in words:
        if cur and len(cur) + len(w_) > 11:
            lines.append(cur); cur = w_
        else:
            cur = (cur + " " + w_).strip()
    lines.append(cur)
    base = y + 36 if below else y - 28 - 15 * (len(lines) - 1)
    for i, l in enumerate(lines[:2]):
        o.append(f'<text x="{x}" y="{base + i * 15}" font-size="12" fill="#CBD5E1" text-anchor="middle">{escape(l)}</text>')


def line(o, pts, color, width=8):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    o.append(f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>')


def build(path):
    H = 1010
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" font-family="Inter,Segoe UI,Helvetica,Arial,sans-serif">',
         '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0F172A"/><stop offset="1" stop-color="#1E1B4B"/></linearGradient>'
         '<pattern id="g" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#1E293B" stroke-width="1"/></pattern></defs>',
         f'<rect width="{W}" height="{H}" rx="20" fill="url(#bg)"/><rect width="{W}" height="{H}" rx="20" fill="url(#g)" opacity=".7"/>',
         '<text x="56" y="62" font-size="30" font-weight="800" fill="#F8FAFC">Learning roadmap</text>',
         '<text x="56" y="90" font-size="15" fill="#94A3B8">Core path in order · Quick wins any time after L07 · Real-world projects after L15</text>']
    # legend
    lx = 740
    for i, (label, c) in enumerate([("Basics", "#22C55E"), ("Integrations", "#EAB308"), ("AI", "#F97316"), ("Multi-agent", "#EF4444"), ("Quick wins", "#0EA5E9"), ("Projects", "#A855F7")]):
        x = lx + (i % 3) * 170; y = 52 + (i // 3) * 30
        o.append(f'<rect x="{x}" y="{y}" width="26" height="8" rx="4" fill="{c}"/><text x="{x + 34}" y="{y + 9}" font-size="13" fill="#E2E8F0">{label}</text>')

    # ---- core path: serpentine, row 1 L01-L11 (left→right), row 2 L12-L22 (right→left)
    core = [f"L{i:02d}" for i in range(1, 23)]
    x0, x1, y1, y2 = 90, 1190, 190, 380
    step = (x1 - x0) / 10
    pos = {n: (x0 + i * step, y1) for i, n in enumerate(core[:11])}
    pos.update({n: (x1 - i * step, y2) for i, n in enumerate(core[11:])})
    o.append(f'<text x="56" y="140" font-size="14" font-weight="700" fill="#F8FAFC" letter-spacing="2">CORE PATH · 22 LESSONS</text>')
    for a, b, c in LEVEL_COLOR:
        seg = [n for n in core if a <= n <= b]
        pts = [pos[n] for n in seg]
        nxt = core.index(seg[-1]) + 1
        if nxt < len(core):
            pts.append(pos[core[nxt]])
        if "L11" in seg and "L12" in seg:  # the turn on the right
            i = seg.index("L11")
            pts = [pos[n] for n in seg[:i + 1]] + [(x1 + 50, y1), (x1 + 50, y2), pos["L12"]] + [pos[n] for n in seg[i + 2:]] + ([pos[core[nxt]]] if nxt < len(core) else [])
        line(o, pts, c)
    for n in core:
        station(o, *pos[n], n, below=True)
    o.append(f'<circle cx="{pos["L22"][0]}" cy="{pos["L22"][1]}" r="24" fill="none" stroke="#EF4444" stroke-width="2" stroke-dasharray="4 4"/>')
    o.append(f'<text x="{pos["L22"][0] - 34}" y="{pos["L22"][1] + 5}" font-size="18" text-anchor="end">🏁</text>')

    # ---- quick wins
    qy = 560
    o.append(f'<text x="56" y="{qy - 50}" font-size="14" font-weight="700" fill="#F8FAFC" letter-spacing="2">⚡ QUICK WINS · 15 MIN EACH · ANY ORDER</text>')
    qs = [f"Q{i:02d}" for i in range(1, 9)]
    qstep = (x1 - x0) / 7
    line(o, [(x0, qy), (x1, qy)], "#0EA5E9")
    for i, n in enumerate(qs):
        station(o, x0 + i * qstep, qy, n)

    # ---- projects: two rows of 6
    py1, py2 = 760, 920
    o.append(f'<text x="56" y="{py1 - 50}" font-size="14" font-weight="700" fill="#F8FAFC" letter-spacing="2">🏭 PROJECTS · REAL BUSINESS PROCESSES</text>')
    ps = [f"P{i:02d}" for i in range(1, 13)]
    pstep = (x1 - x0) / 5
    ppos = {n: (x0 + i * pstep, py1) for i, n in enumerate(ps[:6])}
    ppos.update({n: (x1 - i * pstep, py2 - 20) for i, n in enumerate(ps[6:])})
    line(o, [ppos[n] for n in ps[:6]] + [(x1 + 50, py1), (x1 + 50, py2 - 20)] + [ppos[n] for n in ps[6:]], "#A855F7")
    for n in ps:
        station(o, *ppos[n], n)
    o.append("</svg>")
    open(path, "w").write("\n".join(o))
