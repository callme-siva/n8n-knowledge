"""Tiny builder for n8n workflow JSON. Keeps every workflow spec short and consistent."""
import json, os, uuid

GEMINI_MODEL = "models/gemini-2.5-flash"
EMBED_MODEL = "models/gemini-embedding-001"
EMAIL = "you@example.com"


def _id(seed):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))


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


def write(root, wf, readme):
    d = os.path.join(root, "workflows", wf.slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "workflow.json"), "w") as fh:
        json.dump(wf.to_json(), fh, indent=2, ensure_ascii=False)
    with open(os.path.join(d, "README.md"), "w") as fh:
        fh.write(readme.strip() + "\n")


def readme(num, title, level, domain, time, story, learn, flow, creds, steps, test, errors, extend):
    L = [f"# {num} · {title}", "",
         f"**Level:** {level} · **Domain:** {domain} · **Build time:** {time}", ""]
    L += ["## The real-world problem", story, "",
          "## What you will learn", *[f"- {x}" for x in learn], "",
          "## How it flows", "```", flow.strip("\n"), "```", "",
          "## Credentials you need", *([f"- {c}" for c in creds] or ["- None — this one runs with zero setup."]), "",
          "## Build it step by step",
          "> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).", ""]
    L += [f"{i}. {s}" for i, s in enumerate(steps, 1)]
    L += ["", "## Test it", *[f"- {t}" for t in test], "",
          "## Common errors", "| Symptom | Fix |", "|---|---|", *[f"| {a} | {b} |" for a, b in errors], "",
          "## Level up (try these next)", *[f"- {x}" for x in extend], "",
          "---", "[← Back to the learning path](../../README.md)"]
    return "\n".join(L)
