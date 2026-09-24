"""Sanity-check every workflow.json before it is published.
Checks: valid JSON, unique node names, every connection points to a real node,
no credentials / pinned data, no personal email addresses or secrets, no unauthenticated webhooks,
retry (or explicit error handling) on every external call, and at least one behaviour check per runnable workflow."""
import json, glob, re, sys, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ALLOWED_EMAILS = {"you@example.com", "noreply@anthropic.com"}
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}")
SECRET_RE = re.compile(r"AIza[0-9A-Za-z_-]{30,}|sk-[A-Za-z0-9_-]{20,}|xox[bpas]-[A-Za-z0-9-]{10,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY")
EXTERNAL = {"httpRequest", "gmail", "googleSheets", "jira", "slack", "telegram", "googleDrive", "googleCalendar", "rssFeedRead"}
sys.path.insert(0, os.path.join(ROOT, "tests"))
from fixtures import EXPECT  # noqa: E402
STRUCTURE_ONLY = {"P10-mcp-server-business-tools"}   # MCP trigger: called by AI clients, not runnable from the CLI
problems = 0

for path in sorted(glob.glob(os.path.join(ROOT, "workflows", "*", "workflow.json"))):
    rel = os.path.relpath(path, ROOT)
    errs = []
    try:
        raw = open(path).read(); wf = json.loads(raw)
    except Exception as e:
        print(f"✗ {rel}: invalid JSON: {e}"); problems += 1; continue
    names = [n["name"] for n in wf["nodes"]]
    if len(names) != len(set(names)):
        errs.append("duplicate node names")
    for src, kinds in wf["connections"].items():
        if src not in names:
            errs.append(f"connection from missing node '{src}'")
        for outs in kinds.values():
            for out in outs:
                for c in out or []:
                    if c["node"] not in names:
                        errs.append(f"'{src}' → missing node '{c['node']}'")
    for n in wf["nodes"]:
        if "credentials" in n:
            errs.append(f"'{n['name']}' still has credentials attached")
        if not n.get("type") or "typeVersion" not in n:
            errs.append(f"'{n['name']}' missing type/typeVersion")
        s = n["type"].split(".")[-1]
        if s in EXTERNAL and n["parameters"].get("operation") != "sendAndWait" and not n.get("retryOnFail") and n.get("onError") is None:
            errs.append(f"'{n['name']}' calls an external service with no retryOnFail / onError")
    for n in wf["nodes"]:
        if n["type"].endswith(".webhook") and n["parameters"].get("authentication", "none") == "none":
            errs.append(f"webhook '{n['name']}' has no authentication (use headerAuth / basicAuth / jwtAuth)")
    for m in SECRET_RE.findall(raw):
        errs.append(f"possible secret / API key in the file: {m[:8]}…")
    slug = os.path.basename(os.path.dirname(path))
    if slug not in STRUCTURE_ONLY and not EXPECT.get(slug):
        errs.append("no behaviour check in tests/fixtures.py EXPECT (add at least one)")
    if wf.get("pinData"):
        errs.append("pinData present (may leak real data)")
    for e in {x for x in EMAIL_RE.findall(raw) if not x.endswith("@example.com")} - ALLOWED_EMAILS:
        errs.append(f"personal email found: {e}")
    real = [n for n in wf["nodes"] if "stickyNote" not in n["type"]]
    triggers = [n for n in real if re.search(r"[Tt]rigger$|webhook$|formTrigger|errorTrigger", n["type"])]
    if not triggers:
        errs.append("no trigger node")
    if not os.path.exists(os.path.join(os.path.dirname(path), "README.md")):
        errs.append("README.md missing")
    status = "✓" if not errs else "✗"
    print(f"{status} {rel}  ({len(real)} nodes)" + "".join(f"\n    - {e}" for e in errs))
    problems += len(errs)

# every relative link / image in every markdown file must resolve
for md in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
    if "/.preview/" in md or "/node_modules/" in md:
        continue
    for m in re.finditer(r'\]\(([^)\s]+)\)|href="([^"]+)"|src="([^"]+)"', open(md).read()):
        link = next(g for g in m.groups() if g)
        if re.match(r"(https?:|mailto:|#)", link) or "{" in link or not link.split("#")[0]:
            continue
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(md), link.split("#")[0]))):
            print(f"✗ broken link in {os.path.relpath(md, ROOT)}: {link}")
            problems += 1

print(f"\n{problems} problem(s)")
sys.exit(1 if problems else 0)
