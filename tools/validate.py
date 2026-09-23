"""Sanity-check every workflow.json before it is published.
Checks: valid JSON, unique node names, every connection points to a real node,
no credentials / pinned data, and no personal email addresses."""
import json, glob, re, sys, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ALLOWED_EMAILS = {"you@example.com", "noreply@anthropic.com"}
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}")
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

print(f"\n{problems} problem(s)")
sys.exit(1 if problems else 0)
