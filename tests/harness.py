"""End-to-end test harness.

Builds a *test copy* of every workflow where
  • nodes that need credentials are replaced by stub Code nodes returning realistic mock data (tests/fixtures.py),
  • event triggers (form, webhook, gmail, chat…) become a Manual Trigger + a stub that emits a sample event,
  • long Wait nodes are shortened to 1 second,
then imports and executes each copy with the real n8n CLI. Everything else — Code, IF/Switch, Merge, loops,
expressions, public HTTP APIs, RSS, HTML extraction, QuickChart — runs for real.

Usage:  N8N_DIR=/path/with/node_modules/n8n  python3 tests/harness.py [slug-prefix …]
"""
import base64, copy, glob, json, os, re, subprocess, sys, tempfile, hashlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from fixtures import FIXTURES, TRIGGERS, EXPECT  # noqa: E402

N8N_DIR = os.environ.get("N8N_DIR", os.getcwd())
N8N = os.path.join(N8N_DIR, "node_modules", ".bin", "n8n")

NEEDS_CREDS = {"gmail", "googleSheets", "googleDrive", "googleCalendar", "jira", "slack", "telegram", "executeWorkflow",
               "chainLlm", "agent", "informationExtractor", "vectorStoreInMemory"}
EVENT_TRIGGERS = {"formTrigger", "webhook", "gmailTrigger", "telegramTrigger", "chatTrigger", "errorTrigger", "executeWorkflowTrigger"}
NOT_RUNNABLE = {"mcpTrigger"}  # tools-only servers: structure-checked, not executed


def short(t):
    return t.split(".")[-1]


def default_stub(n):
    """Mock output for a credentialed node, per item, when no fixture is given."""
    s, p = short(n["type"]), n["parameters"]
    op = p.get("operation", "")
    if s == "gmail":
        if op == "sendAndWait":
            return "each", {"data": {"approved": True}}
        if op == "getAll":
            return "each", {}                      # no messages found
        return "each", {"id": "mock-msg", "threadId": "mock-thread", "labelIds": ["SENT"]}
    if s == "googleSheets" and op in ("append", "appendOrUpdate", "update"):
        return "echo", None
    if s == "jira" and not op:
        return "jira", None
    if s == "jira" and op == "update":
        return "each", {"success": True}
    if s == "googleCalendar":
        return "each", {"id": "evt", "htmlLink": "https://calendar.google.com/mock"}
    if s in ("slack", "telegram"):
        return "each", {"ok": True, "ts": "123.456"}
    if s == "googleDrive":
        return "each", {"id": "drive-file", "name": "file.pdf"}
    if s == "executeWorkflow":
        return "each", {"sent": True}
    if s == "vectorStoreInMemory":
        return "echo", None
    return None, None


def stub_code(mode, data):
    if mode == "echo":
        return {"mode": "runOnceForEachItem", "jsCode": "return { json: $json };"}
    if mode == "each":
        return {"mode": "runOnceForEachItem", "jsCode": f"return {{ json: {json.dumps(data, ensure_ascii=False)} }};"}
    if mode == "jira":
        return {"mode": "runOnceForEachItem", "jsCode": "return { json: { key: 'MOCK-' + ($itemIndex + 1), id: String(10000 + $itemIndex) } };"}
    if mode == "code":
        return {"mode": "runOnceForEachItem", "jsCode": data}
    if mode == "all":  # fixed list of items, all paired to input item 0
        return {"jsCode": f"return {json.dumps(data, ensure_ascii=False)}.map(j => ({{ json: j, pairedItem: 0 }}));"}
    raise ValueError(mode)


def build_test_copy(wf, slug):
    wf = copy.deepcopy(wf)
    base = slug.split("--")[0]            # "X01-…--solution" uses X01's fixtures
    fx = FIXTURES.get(base, {})
    nodes = {n["name"]: n for n in wf["nodes"]}
    ai_children = {src for src, kinds in wf["connections"].items() for k in kinds if k != "main"}
    mocked, runnable = [], True
    sheets = {n["name"]: {"tab": (n["parameters"].get("sheetName") or {}).get("value"), "op": n["parameters"].get("operation", "read")}
              for n in wf["nodes"] if n["type"].endswith("googleSheets")}
    new_nodes = []
    for n in wf["nodes"]:
        s = short(n["type"])
        if "stickyNote" in n["type"]:
            continue
        if s in NOT_RUNNABLE:
            runnable = False
        if n["name"] in ai_children:
            continue  # AI sub-nodes are dropped; their root is stubbed
        if s == "respondToWebhook":  # no live HTTP caller in tests: still evaluate the response body expression
            body = str(n["parameters"].get("responseBody", "={{ $json }}"))
            inner = body[3:-2].strip() if body.startswith("={{") and body.endswith("}}") else "$json"
            n.update({"type": "n8n-nodes-base.set", "typeVersion": 3.4, "parameters": {"mode": "raw", "jsonOutput": "={{ JSON.stringify(" + inner + ") }}", "options": {}}})
        if s == "scheduleTrigger":  # the CLI can only start from a manual trigger
            n.update({"type": "n8n-nodes-base.manualTrigger", "typeVersion": 1, "parameters": {}})
        if s == "wait" and n["parameters"].get("resume") == "timeInterval":
            n["parameters"].update({"amount": 1, "unit": "seconds"})
        if s in EVENT_TRIGGERS:
            sample = copy.deepcopy(TRIGGERS.get(base) or TRIGGERS.get(s) or [{}])
            for item in sample:  # "_binary": {"key": {"file": "x.pdf"}} → embed the real sample file
                for b in (item.get("_binary") or {}).values():
                    if "file" in b:
                        b["data"] = base64.b64encode(open(os.path.join(ROOT, "templates", "files", b.pop("file")), "rb").read()).decode()
            start = f"__test_start_{len(mocked)}"
            new_nodes.append({"id": start, "name": start, "type": "n8n-nodes-base.manualTrigger", "typeVersion": 1, "position": [n["position"][0] - 200, n["position"][1]], "parameters": {}})
            wf["connections"][start] = {"main": [[{"node": n["name"], "type": "main", "index": 0}]]}
            # "_binary" in a sample becomes a real binary attachment (tiny placeholder file)
            n.update({"type": "n8n-nodes-base.code", "typeVersion": 2, "parameters": {"jsCode":
                f"return {json.dumps(sample, ensure_ascii=False)}.map(({{ _binary, ...j }}) => ({{ json: j, binary: Object.fromEntries(Object.entries(_binary || {{}}).map(([k, b]) => [k, {{ data: Buffer.from('placeholder').toString('base64'), ...b }}])) }}));"}})
            mocked.append(n["name"])
        elif s == "textClassifier":
            route = fx.get(n["name"], 0)
            outs = len(n["parameters"]["categories"]["categories"]) + (1 if n["parameters"].get("options", {}).get("fallback") == "other" else 0)
            n.update({"type": "n8n-nodes-base.switch", "typeVersion": 3.2, "parameters": {"mode": "expression", "numberOutputs": outs, "output": f"={route}"}})
            mocked.append(n["name"])
        elif n["name"] in fx or s in NEEDS_CREDS or (s == "httpRequest" and n["parameters"].get("authentication")) or (s == "googleSheets"):
            cols = n["parameters"].get("columns", {})
            if s == "googleSheets" and cols.get("mappingMode") == "defineBelow" and n["name"] not in fx:
                # evaluate the inline column mapping for real (it contains expressions worth testing)
                n.update({"type": "n8n-nodes-base.set", "typeVersion": 3.4, "parameters": {"assignments": {"assignments": [
                    {"id": k, "name": k, "value": v, "type": "string"} for k, v in cols["value"].items()]}, "options": {}}})
                for k in ("retryOnFail", "maxTries", "waitBetweenTries", "alwaysOutputData", "executeOnce", "onError"):
                    n.pop(k, None)
                mocked.append(n["name"]); new_nodes.append(n); continue
            if n["name"] in fx:
                mode, data = fx[n["name"]]
            else:
                mode, data = default_stub(n)
            if mode is None:
                raise SystemExit(f"{slug}: no mock for node '{n['name']}' ({s}). Add it to tests/fixtures.py")
            keep = {k: n[k] for k in ("onError",) if k in n}
            for k in ("retryOnFail", "maxTries", "waitBetweenTries", "alwaysOutputData", "executeOnce", "onError"):
                n.pop(k, None)
            n.update({"type": "n8n-nodes-base.code", "typeVersion": 2, "parameters": stub_code(mode, data)})
            if keep.get("onError") == "continueErrorOutput":
                n["onError"] = "continueErrorOutput"
            mocked.append(n["name"])
        new_nodes.append(n)
    kept = {n["name"] for n in new_nodes}
    conns = {}
    for src, kinds in wf["connections"].items():
        if src not in kept:
            continue
        main = kinds.get("main")
        if main:
            conns[src] = {"main": [[c for c in out if c["node"] in kept] for out in main]}
    wf.update({"nodes": new_nodes, "connections": conns, "pinData": {}, "active": False,
               "id": "t" + hashlib.md5(slug.encode()).hexdigest()[:15], "name": "TEST " + wf["name"]})
    wf["_sheets"] = sheets
    return wf, mocked, runnable


def run(slugs):
    tmp = tempfile.mkdtemp(prefix="n8n-e2e-")
    env = dict(os.environ, N8N_USER_FOLDER=os.path.join(tmp, "home"), N8N_DIAGNOSTICS_ENABLED="false",
               N8N_LOG_LEVEL="info", N8N_RUNNERS_ENABLED="true", GENERIC_TIMEZONE="Asia/Kolkata")
    plans = []
    # debug challenges ship a broken workflow.json plus a fixed solution.json: both are run
    paths = sorted(glob.glob(os.path.join(ROOT, "workflows", "*", "workflow.json")) + glob.glob(os.path.join(ROOT, "workflows", "*", "solution.json")))
    for path in paths:
        slug = os.path.basename(os.path.dirname(path)) + ("--solution" if path.endswith("solution.json") else "")
        if slugs and not any(slug.startswith(p) for p in slugs):
            continue
        wf, mocked, runnable = build_test_copy(json.load(open(path)), slug)
        f = os.path.join(tmp, slug + ".json")
        sheets = wf.pop("_sheets")
        json.dump(wf, open(f, "w"))
        wf["_sheets"] = sheets
        plans.append((slug, wf, mocked, runnable, f))
    imp = os.path.join(tmp, "imp"); os.makedirs(imp)
    for slug, wf, *_rest, f in plans:
        os.link(f, os.path.join(imp, slug + ".json"))
    subprocess.run([N8N, "import:workflow", "--separate", f"--input={imp}"], env=env, capture_output=True, text=True, check=True)
    results = {}
    for slug, wf, mocked, runnable, f in plans:
        real = [n["name"] for n in wf["nodes"] if n["name"] not in mocked and not n["name"].startswith("__test_start")]
        if not runnable:
            results[slug] = {"status": "structure-only", "reason": "MCP server trigger (called by AI clients, not runnable from CLI)"}
            print(f"◻ {slug}: structure-only"); continue
        p = subprocess.run([N8N, "execute", f"--id={wf['id']}"], env=env, capture_output=True, text=True, timeout=300)
        out = p.stdout + p.stderr
        ok = p.returncode == 0 and "Execution error" not in out
        ran, run_data = [], {}
        mark = p.stdout.find("=" * 10)
        if mark != -1:
            try:
                data, _ = json.JSONDecoder().raw_decode(p.stdout[p.stdout.index("{", mark):])
                run_data = data.get("data", {}).get("resultData", {}).get("runData") or {}
                ran = list(run_data.keys())
            except ValueError:
                pass
        err = ""
        if not ok and os.environ.get("HARNESS_DEBUG"):
            print(out[-3000:])
        if not ok:
            em = re.search(r"Execution error:\s*\n(?:=+\s*\n)?(.*)", out)
            err = (em.group(1) if em else out.strip().splitlines()[-1] if out.strip() else "unknown")[:300]
        results[slug] = {"status": "passed" if ok else "failed", "real_nodes": len(real), "mocked_nodes": len(mocked),
                         "nodes_ran": len([r for r in ran if not r.startswith("__test_start")]),
                         "ran": sorted(r for r in ran if not r.startswith("__test_start")), "error": err}
        base = slug.split("--")[0]
        broken = not slug.endswith("--solution") and os.path.exists(os.path.join(ROOT, "workflows", slug, "solution.json"))
        checks = [] if broken else EXPECT.get(base, [])
        if broken:   # must fail, and with the ✅ Check node's bug list (not some unrelated error)
            if ok:
                ok, err = False, "debug challenge ran clean: its bugs are missing"
            elif "bug(s) left" in out:
                ok, err = True, re.search(r"🐞 [^\n]*", out).group(0)[:300]
            results[slug].update(status="passed" if ok else "failed", error=err, expected_failure=True)
        failures = []
        for chk in checks if ok and not broken else []:
            kind, node = chk[0], chk[1]
            runs = run_data.get(node, [])
            outs = [r.get("data", {}).get("main", []) for r in runs]
            if kind == "count":
                got = sum(len(o[chk[2]] or []) for o in outs if len(o) > chk[2])
                if got != chk[3]:
                    failures.append(f"{node}[out {chk[2]}] emitted {got} item(s), expected {chk[3]}")
            else:
                blob = json.dumps(outs, ensure_ascii=False, separators=(",", ":"))
                if (kind == "contains") != (chk[2] in blob):
                    failures.append(f"{node} {'should' if kind == 'contains' else 'must not'} contain {chk[2]!r}")
        results[slug]["checks"] = len(checks)
        # record the exact rows each Google Sheets node read or wrote (used to generate templates/)
        sheet_io = {}
        for node, meta in wf.get("_sheets", {}).items():
            items = [it.get("json", {}) for r in run_data.get(node, []) for out in r.get("data", {}).get("main", [])[:1] for it in (out or [])]
            if items:
                sheet_io.setdefault(meta["tab"], {"reads": [], "writes": []})["reads" if meta["op"] == "read" else "writes"].extend(items[:5])
        if sheet_io:
            results[slug]["sheets"] = sheet_io
        if failures:
            ok = False
            results[slug].update(status="failed", error="; ".join(failures))
        n_ran = results[slug]["nodes_ran"]
        if ok and n_ran == 0:
            results[slug]["status"] = "failed"; results[slug]["error"] = "no nodes executed"; ok = False
        print(f"{'✓' if ok else '✗'} {slug}: ran {n_ran}/{len(real) + len(mocked)} nodes ({len(mocked)} mocked), " + ("fails with its bug list, as intended" if broken else f"{len(checks)} behaviour checks") + ("" if ok else f"\n    → {results[slug]['error']}"))
    return results


if __name__ == "__main__":
    res = run(sys.argv[1:])
    out = os.path.join(ROOT, "tests", "results.json")
    old = json.load(open(out)) if os.path.exists(out) else {}
    old.update(res)
    json.dump(old, open(out, "w"), indent=2, sort_keys=True)
    failed = [k for k, v in res.items() if v["status"] == "failed"]
    print(f"\n{len(res) - len(failed)}/{len(res)} ok, {len(failed)} failed")
    sys.exit(1 if failed else 0)
