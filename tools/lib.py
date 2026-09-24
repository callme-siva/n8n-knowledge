"""Tiny builder for n8n workflow JSON. Keeps every workflow spec short and consistent."""
import json, os, uuid

GEMINI_MODEL = "models/gemini-2.5-flash"
EMBED_MODEL = "models/gemini-embedding-001"
EMAIL = "you@example.com"


def _id(seed):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))


# Nodes that call an external service. Unless a spec says otherwise they retry 3× (tools/validate.py enforces it).
EXTERNAL = {"httpRequest", "gmail", "googleSheets", "jira", "slack", "telegram", "googleDrive", "googleCalendar", "rssFeedRead"}
RETRY = {"retryOnFail": True, "maxTries": 3, "waitBetweenTries": 3000}


class WF:
    def __init__(self, slug, name):
        self.slug, self.name = slug, name
        self.nodes, self.conns = [], {}

    def add(self, name, type_, ver, params, pos, **extra):
        if "." not in type_:
            type_ = "n8n-nodes-base." + type_
        n = {"parameters": params, "id": _id(self.slug + name), "name": name,
             "type": type_, "typeVersion": ver, "position": list(pos)}
        n.update(extra)
        self.nodes.append(n)
        return name

    def lc(self, name, t, ver, params, pos, **extra):
        return self.add(name, "@n8n/n8n-nodes-langchain." + t, ver, params, pos, **extra)

    def gemini(self, name, pos, temperature=0.2):
        return self.lc(name, "lmChatGoogleGemini", 1,
                       {"modelName": GEMINI_MODEL, "options": {"temperature": temperature}}, pos)

    def note(self, content, pos, w=380, h=300, color=7):
        if tuple(pos) == (0, 0):
            pos = (-40, -320)
        self.add(f"Note {len([n for n in self.nodes if 'stickyNote' in n['type']]) + 1}",
                 "stickyNote", 1, {"content": content, "width": w, "height": h, "color": color}, pos)

    def link(self, src, dst, out=0, inp=0, kind="main"):
        outs = self.conns.setdefault(src, {}).setdefault(kind, [])
        while len(outs) <= out:
            outs.append([])
        outs[out].append({"node": dst, "type": kind, "index": inp})

    def chain(self, *names):
        for a, b in zip(names, names[1:]):
            self.link(a, b)

    def ai(self, src, dst, kind):
        self.link(src, dst, kind=kind)

    def to_json(self):
        for n in self.nodes:   # also covers nodes loaded from exported JSON
            if n["type"].split(".")[-1] in EXTERNAL and n["parameters"].get("operation") != "sendAndWait" \
                    and not n.get("retryOnFail") and n.get("onError") is None:
                n.update(RETRY)
        return {"name": self.name, "nodes": self.nodes, "connections": self.conns,
                "active": False, "settings": {"executionOrder": "v1"},
                "tags": [], "pinData": {}}


# ---------- common parameter helpers ----------
def cond(left, op_type, operation, right=None, cid="c1"):
    c = {"id": cid, "leftValue": left, "operator": {"type": op_type, "operation": operation}}
    if right is not None:
        c["rightValue"] = right
    else:
        c["operator"]["singleValue"] = True
    return c


def conditions(*conds, combinator="and"):
    return {"options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose", "version": 2},
            "conditions": list(conds), "combinator": combinator}


def assign(**kv):
    out = []
    for i, (k, v) in enumerate(kv.items()):
        t = "number" if isinstance(v, (int, float)) and not isinstance(v, bool) else \
            "boolean" if isinstance(v, bool) else "string"
        out.append({"id": f"a{i}", "name": k, "value": v, "type": t})
    return {"assignments": {"assignments": out}, "options": {}}


def gmail_send(to, subject, html):
    return {"sendTo": to, "subject": subject, "emailType": "html", "message": html,
            "options": {"appendAttribution": False}}


def sheet_append(sheet_name="Sheet1"):
    return {"operation": "append",
            "documentId": {"__rl": True, "mode": "url", "value": "PASTE_YOUR_GOOGLE_SHEET_URL"},
            "sheetName": {"__rl": True, "mode": "name", "value": sheet_name},
            "columns": {"mappingMode": "autoMapInputData", "value": {}, "matchingColumns": [], "schema": []},
            "options": {}}


def form_field(label, ftype=None, required=False, options=None, placeholder=None):
    f = {"fieldLabel": label}
    if ftype:
        f["fieldType"] = ftype
    if required:
        f["requiredField"] = True
    if options:
        f["fieldOptions"] = {"values": [{"option": o} for o in options]}
    if placeholder:
        f["placeholder"] = placeholder
    return f


def write(root, wf, doc):
    from render import canvas_svg, mermaid
    d = os.path.join(root, "workflows", wf.slug)
    os.makedirs(d, exist_ok=True)
    data = wf.to_json()
    with open(os.path.join(d, "workflow.json"), "w") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    with open(os.path.join(d, "canvas.svg"), "w") as fh:
        fh.write(canvas_svg(data))
    md = doc if isinstance(doc, str) else render_readme(dict(doc, slug=wf.slug), data, mermaid(data))
    with open(os.path.join(d, "README.md"), "w") as fh:
        fh.write(md.strip() + "\n")


LEVELS = {"🟢": ("Beginner", "2EA44F"), "🟡": ("Integrations", "D4A106"), "🟠": ("AI", "F97316"), "🔴": ("Multi-agent & production", "DC2626"),
          "⚡": ("Quick win", "0EA5E9"), "🏭": ("Real-world project", "7C3AED")}


def badge(label, value, color):
    from urllib.parse import quote
    q = lambda t: quote(t.replace("-", "--").replace("_", "__").replace(" ", "_"))
    return f"![{label}: {value}](https://img.shields.io/badge/{q(label)}-{q(value)}-{color}?style=flat-square)"


def readme(num, title, level, domain, time, story, learn, flow, creds, steps, test, errors, extend):
    return dict(num=num, title=title, level=level, domain=domain, time=time, story=story, learn=learn,
                flow=flow, creds=creds, steps=steps, test=test, errors=errors, extend=extend)


REGISTRY = []


SHEET_TEMPLATES = {}
SAMPLE_FILES = {
    "L06": [("invoice-valid.pdf", "email it to yourself as an attachment")],
    "L13": [("hr-policy.pdf", "upload it in the form")],
    "L18": [("resume-sample.pdf", "upload it in the form")],
    "P01": [("invoice-valid.pdf", "auto-approved → ledger"), ("invoice-large.pdf", "₹1,18,000 → needs approval"), ("invoice-wrong-total.pdf", "subtotal + tax ≠ total → Exceptions")],
}


def starter_files(slug, num):
    rows = SHEET_TEMPLATES.get(slug, [])
    files = SAMPLE_FILES.get(num, [])
    if not rows and not files:
        return []
    L = ["### 📥 Starter files", ""]
    if rows:
        L += ["Create each tab from its template, so column names match exactly: **Google Sheets → File → Import → Upload** the CSV → *Insert new sheet(s)*. The tab takes the file's name.", "",
              "| Tab | Template | Columns |", "|---|---|---|"]
        L += [f"| `{tab}` | [{tab}.csv](../../{path}) | {', '.join(f'`{c}`' for c in cols)} |" for tab, path, cols in rows]
        L.append("")
        L.append("<sub>Columns are generated from what this workflow actually reads and writes in the automated test, so they can't drift from the workflow.</sub>")
        L.append("")
    if files:
        L += ["Sample files: " + " · ".join(f"[{f}](../../templates/files/{f}) ({why})" for f, why in files), ""]
    return L


def _test_result(slug):
    path = os.path.join(os.path.dirname(__file__), "..", "tests", "results.json")
    try:
        return json.load(open(path)).get(slug)
    except (OSError, ValueError):
        return None


def render_readme(r, data, diagram):
    REGISTRY.append(dict(r, name=data['name']))
    from render import context_mermaid
    from concepts import CONCEPTS
    from decisions import DECISIONS
    from reference import node_reference, placeholders
    lvl_name, color = LEVELS[r["level"][0]]
    nodes = [n for n in data["nodes"] if "stickyNote" not in n["type"]]
    t = _test_result(r.get("slug", ""))
    if t and t.get("status") == "passed":
        tbadge = badge("e2e test", f"passed · {t.get('checks', 0)} checks", "2EA44F") if t.get("checks") else badge("e2e test", "smoke run only", "D4A106")
    elif t and t.get("status") == "structure-only":
        tbadge = badge("e2e test", "structure only", "64748B")
    else:
        tbadge = badge("e2e test", "not run", "9CA3AF")
    tbadge = f"[{tbadge}](https://github.com/callme-siva/n8n-knowledge/actions/workflows/validate.yml)"   # CI re-runs it on every push
    L = ['<div align="center">', "", f"# {r['num']} · {r['title']}", "",
         " ".join([badge("level", lvl_name, color), badge("domain", r["domain"], "334155"),
                   badge("build time", r["time"], "0EA5E9"), badge("nodes", str(len(nodes)), "7C3AED"), tbadge]), "",
         "<img src=\"canvas.svg\" alt=\"Workflow canvas snapshot\" width=\"100%\">", "",
         "</div>", "",
         "> [!NOTE]", f"> **The real-world problem.** {r['story']}", ""]
    c = CONCEPTS.get(r["num"])
    if c:
        L += ["## 💡 Concept first", "",
              f"**📌 Key idea:** {c[0]}", "",
              f"**🧠 Mental model:** {c[1]}", "",
              f"**🚫 When *not* to use it:** {c[2]}", ""]
    L += ["## 🎯 What you'll learn", "", *[f"- {x}" for x in r["learn"]], "",
          "## 🏗️ Architecture", "",
          "**System context:** who and what this workflow talks to, and what crosses each boundary. 🔑 = needs a credential · 🧑 = a human decides.", "",
          context_mermaid(data), "",
          "<details><summary><b>Node-level flow</b> (every node and branch)</summary>", "", diagram, "", "</details>", "",
          "<details><summary>Plain-text flow</summary>", "", "```", r["flow"].strip("\n"), "```", "", "</details>", ""]
    d = DECISIONS.get(r["num"])
    if d:
        L += ["## ⚖️ Design decisions & trade-offs", "", "Why it's built this way, and what it costs.", "",
              "| Decision | Why | Trade-off / alternative |", "|---|---|---|", *[f"| {a} | {b} | {c_} |" for a, b, c_ in d], ""]
    L += ["## 🔑 Credentials", "", "| You need | Where to get it |", "|---|---|"]
    if r["creds"]:
        for c in r["creds"]:
            name, _, rest = c.partition(": ")
            L.append(f"| {name.strip()} | {rest.strip() or '[docs/credentials.md](../../docs/credentials.md)'} |")
    else:
        L.append("| Nothing | Runs with zero setup |")
    L += ["", placeholders(data), *starter_files(r.get("slug", ""), r["num"]), "## 🛠️ Build it step by step", "",
          "> [!TIP]", "> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.", ""]
    L += [f"{i}. {s}" for i, s in enumerate(r["steps"], 1)]
    L += ["", node_reference(data), "## ✅ Test it", ""]
    if t and t.get("status") == "passed":
        L += ["> [!TIP]", f"> **Automated end-to-end test: passed.** {t.get('nodes_ran')}/{t.get('real_nodes', 0) + t.get('mocked_nodes', 0)} nodes executed in real n8n "
              f"({t.get('mocked_nodes')} credentialed or AI nodes replaced by fixtures, so AI output itself isn't tested), {t.get('checks', 0)} behaviour checks. See [tests/](../../tests/README.md).", ""]
    L += [*[f"- [ ] {x}" for x in r["test"]], "",
          "## 🧯 Troubleshooting", "",
          "Problems specific to this workflow are below. For general ones (expressions, items, triggers, AI), see [common mistakes](../../docs/common-mistakes.md).", ""]
    for a, b in r["errors"]:
        L += [f"<details><summary><b>{a.replace('`', '')}</b></summary>", "", b, "", "</details>", ""]
    from exercises import EX
    ex = EX.get(r["num"], [])
    if ex:
        L += ["## 🏋️ Practice", "", "Try each challenge **before** opening the hint. Solutions show the exact expressions and code.", ""]
        for i, (stars, task, hint, sol) in enumerate(ex, 1):
            L += [f"**{'⭐' * stars} Challenge {i}:** {task}", "",
                  "<details><summary>💡 Hint</summary>", "", hint, "", "</details>",
                  "<details><summary>✅ Solution</summary>", "", sol, "", "</details>", ""]
    L += ["## 🚀 Ideas to extend it", "", *[f"- {x}" for x in r["extend"]], "", "---", "", "{{NAV}}"]
    return "\n".join(L)


# ---------- helpers added for the Quick-wins and Projects tracks ----------
def slack_post(channel, text):
    return {"select": "channel", "channelId": {"__rl": True, "mode": "name", "value": channel}, "text": text, "otherOptions": {}}


def slack_post_id(text):
    """Post to the channel ID stored in ⚙️ Config (IDs survive channel renames)."""
    return {"select": "channel", "channelId": {"__rl": True, "mode": "id", "value": "={{ $('⚙️ Config').first().json.slack_channel_id }}"}, "text": text, "otherOptions": {}}


def sheet_read(sheet_name, lookup_column=None, lookup_value=None):
    p = {"documentId": {"__rl": True, "mode": "url", "value": "PASTE_YOUR_GOOGLE_SHEET_URL"},
         "sheetName": {"__rl": True, "mode": "name", "value": sheet_name}, "options": {}}
    if lookup_column:
        p["filtersUI"] = {"values": [{"lookupColumn": lookup_column, "lookupValue": lookup_value}]}
    return p


def sheet_upsert(sheet_name, key):
    return {"operation": "appendOrUpdate",
            "documentId": {"__rl": True, "mode": "url", "value": "PASTE_YOUR_GOOGLE_SHEET_URL"},
            "sheetName": {"__rl": True, "mode": "name", "value": sheet_name},
            "columns": {"mappingMode": "autoMapInputData", "value": {}, "matchingColumns": [key], "schema": []},
            "options": {}}


def approval(to, subject, html, days=3):
    return {"operation": "sendAndWait", "sendTo": to, "subject": subject, "message": html,
            "approvalOptions": {"values": {"approvalType": "double"}},
            "options": {"limitWaitTime": {"values": {"limitType": "afterTimeInterval", "resumeAmount": days, "resumeUnit": "days"}}}}


def sheet_set(sheet_name, key, **values):
    """Append-or-update one row with explicitly mapped values (no Set node needed)."""
    schema = [{"id": k, "displayName": k, "type": "string", "required": False, "display": True,
               "canBeUsedToMatch": True, "defaultMatch": False, "removed": False} for k in values]
    return {"operation": "appendOrUpdate",
            "documentId": {"__rl": True, "mode": "url", "value": "PASTE_YOUR_GOOGLE_SHEET_URL"},
            "sheetName": {"__rl": True, "mode": "name", "value": sheet_name},
            "columns": {"mappingMode": "defineBelow", "value": values, "matchingColumns": [key], "schema": schema},
            "options": {}}
