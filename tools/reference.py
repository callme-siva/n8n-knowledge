"""Generate the per-lesson 'Node-by-node reference' and 'Values to replace' sections from workflow.json."""
import json

# short type → (friendly name, what it does)
TYPES = {
    "manualTrigger": ("Manual Trigger", "Starts the workflow when you click *Execute workflow*. For testing only."),
    "scheduleTrigger": ("Schedule Trigger", "Starts the workflow on a timer or cron expression. Only fires when the workflow is **active**."),
    "formTrigger": ("n8n Form Trigger", "Hosts a web form; each submission starts one execution. Field labels become JSON keys."),
    "webhook": ("Webhook", "Gives the workflow its own URL. Any HTTP call to it starts an execution."),
    "gmailTrigger": ("Gmail Trigger", "Polls Gmail on an interval and starts once per matching email."),
    "errorTrigger": ("Error Trigger", "Starts when *another* workflow that points here as its error workflow fails."),
    "chatTrigger": ("Chat Trigger", "Opens a chat window; each message starts an execution with `chatInput` and a `sessionId`."),
    "executeWorkflowTrigger": ("Execute Workflow Trigger", "Makes this workflow callable from other workflows, like a function."),
    "set": ("Edit Fields (Set)", "Creates, renames or overwrites fields without code."),
    "code": ("Code", "Runs JavaScript. *Run once for all items* sees every item; *for each item* sees one at a time."),
    "httpRequest": ("HTTP Request", "Calls any REST API. Use it whenever there's no dedicated node."),
    "if": ("If", "Splits items into a **true** and a **false** branch."),
    "switch": ("Switch", "Routes items to one of many named outputs."),
    "filter": ("Filter", "Keeps only items that match; drops the rest."),
    "merge": ("Merge", "Waits for several inputs and combines them into one stream."),
    "splitOut": ("Split Out", "Turns one item holding an array into one item per array element."),
    "noOp": ("No Operation", "Does nothing. Marks a branch that intentionally ends."),
    "stopAndError": ("Stop and Error", "Fails the execution on purpose with your message, which triggers the error workflow."),
    "respondToWebhook": ("Respond to Webhook", "Sends the HTTP response (status code and body) back to the webhook caller."),
    "executeWorkflow": ("Execute Workflow", "Calls another workflow (a sub-workflow) and waits for its result."),
    "rssFeedRead": ("RSS Read", "Reads an RSS/Atom feed; outputs one item per article."),
    "gmail": ("Gmail", "Sends, reads or labels email. `sendAndWait` pauses the workflow for a human reply."),
    "googleSheets": ("Google Sheets", "Reads, appends or updates rows in a spreadsheet."),
    "googleDrive": ("Google Drive", "Uploads, downloads or moves files in Drive."),
    "jira": ("Jira Software", "Creates, searches or updates Jira issues."),
    "extractFromFile": ("Extract From File", "Pulls text or data out of a binary file (PDF, CSV, XLSX…)."),
    "stickyNote": ("Sticky Note", "Documentation on the canvas. Doesn't run."),
    "agent": ("AI Agent", "An LLM that can call tools, use memory and loop until it has an answer."),
    "chainLlm": ("Basic LLM Chain", "Sends one prompt to a model and returns the answer. Simplest AI node."),
    "lmChatGoogleGemini": ("Google Gemini Chat Model", "The language model plugged into a chain or agent."),
    "outputParserStructured": ("Structured Output Parser", "Forces the model's answer into JSON matching your schema."),
    "memoryBufferWindow": ("Simple Memory", "Remembers the last N chat messages per session."),
    "toolCalculator": ("Calculator Tool", "Lets an agent do exact arithmetic."),
    "toolWikipedia": ("Wikipedia Tool", "Lets an agent look things up on Wikipedia."),
    "toolHttpRequest": ("HTTP Request Tool", "Lets an agent call an API. `{placeholders}` in the URL are filled in by the model."),
    "vectorStoreInMemory": ("In-Memory Vector Store", "Stores embeddings (insert mode) or searches them (retrieve mode)."),
    "embeddingsGoogleGemini": ("Gemini Embeddings", "Turns text into vectors for semantic search."),
    "documentDefaultDataLoader": ("Default Data Loader", "Loads binary or JSON data as documents for a vector store."),
    "textSplitterRecursiveCharacterTextSplitter": ("Recursive Text Splitter", "Cuts documents into overlapping chunks."),
}

# node-level settings (the node's Settings tab) worth pointing out
SETTINGS = {
    "retryOnFail": "Retry on fail",
    "maxTries": "Max tries",
    "waitBetweenTries": "Wait between tries (ms)",
    "onError": "On error",
    "alwaysOutputData": "Always output data",
    "executeOnce": "Execute once",
}
ON_ERROR = {"continueRegularOutput": "Continue (regular output)", "continueErrorOutput": "Continue (error output)", "stopWorkflow": "Stop workflow"}
PLACEHOLDERS = ("PASTE_YOUR", "REPLACE_", "you@example.com", "YOUR_", "your-link", "YOUR-SITE")


def _short(t):
    return t.split(".")[-1]


def _fmt(v, limit=90):
    if isinstance(v, bool):
        return "✅ on" if v else "off"
    s = str(v)
    if s.startswith("="):
        s = s[1:]
    s = s.replace("\n", " ").replace("|", "\\|").strip()
    return s if len(s) <= limit else s[:limit - 3] + "…"


def _flatten(obj, prefix=""):
    """Yield (path, value) for leaf settings, collapsing n8n's resource-locator and list wrappers."""
    if isinstance(obj, dict):
        if obj.get("__rl"):
            yield prefix, obj.get("value", "")
            return
        if isinstance(obj.get("conditions"), list) and "combinator" in obj:
            OPS = {"equals": "=", "notEquals": "≠", "gt": ">", "gte": "≥", "lt": "<", "lte": "≤", "true": "is true",
                   "false": "is false", "exists": "exists", "contains": "contains", "isEmpty": "is empty", "notEmpty": "is not empty"}
            parts = []
            for c in obj["conditions"]:
                op = c.get("operator", {}).get("operation", "?")
                parts.append(f"{str(c.get('leftValue', '')).lstrip('=')} {OPS.get(op, op)} {str(c.get('rightValue', '')).lstrip('=')}".strip())
            yield f"{prefix}condition", f" {obj['combinator'].upper()} ".join(parts)
            return
        for k, v in obj.items():
            if k in ("jsCode", "jsonSchemaExample", "inputSchema"):
                lines = str(v).count("\n") + 1
                label = "JavaScript" if k == "jsCode" else "JSON schema"
                yield f"{prefix}{k}", f"({label}, {lines} lines, shown below)"
                continue
            if k in ("schema", "matchingColumns") and not v:
                continue
            yield from _flatten(v, f"{prefix}{k}.")
    elif isinstance(obj, list):
        if obj and all(isinstance(x, dict) and "name" in x and "value" in x for x in obj):
            for x in obj:
                yield f"{prefix}{x['name']}", x["value"]
        elif obj and all(isinstance(x, dict) and "fieldLabel" in x for x in obj):
            yield prefix.rstrip("."), ", ".join(x["fieldLabel"] + (" *" if x.get("requiredField") else "") for x in obj)
        elif obj and all(isinstance(x, dict) and "option" in x for x in obj):
            yield prefix.rstrip("."), ", ".join(x["option"] for x in obj)
        elif obj and all(isinstance(x, (str, int, float)) for x in obj):
            yield prefix.rstrip("."), ", ".join(map(str, obj))
        else:
            for i, x in enumerate(obj):
                yield from _flatten(x, prefix if len(obj) == 1 else f"{prefix}{i + 1}.")
    else:
        if obj in ("", None, {}, []):
            return
        yield prefix.rstrip("."), obj


def _clean_path(p):
    for junk in ("values.", "parameters.", "assignments.assignments.", "conditions.conditions.", "messageValues.", "options.", "value."):
        p = p.replace(junk, "")
    return p.strip(".") or "value"


def node_reference(wf):
    nodes = [n for n in wf["nodes"] if "stickyNote" not in n["type"]]
    L = ["## 🔍 Node-by-node reference", "",
         "Every node in this workflow and every setting inside it, generated from [`workflow.json`](workflow.json). Click a node to expand it.", ""]
    for i, n in enumerate(nodes, 1):
        s = _short(n["type"])
        friendly, what = TYPES.get(s, (s, ""))
        L += [f"<details><summary><b>{i}. {n['name']}</b> · <code>{friendly}</code> v{n['typeVersion']}</summary>", "",
              f"> {what}" if what else "", ""]
        rows = []
        for path, val in _flatten(n["parameters"]):
            if path.endswith(".id") or path == "id" or path.endswith("typeValidation") or path.endswith("caseSensitive") or path.endswith("leftValue") and val == "":
                continue
            if path.endswith(".version") and isinstance(val, int):
                continue
            rows.append((_clean_path(path).replace("rules.", "rule ").replace("conditions.condition", "condition"), val))
        for k, label in SETTINGS.items():
            if k in n:
                rows.append((f"⚙️ {label}", ON_ERROR.get(n[k], n[k]) if k == "onError" else n[k]))
        if rows:
            L += ["| Property | Value |", "|---|---|"]
            full = lambda p: 700 if p.split(".")[-1] in ("systemMessage", "text", "message", "toolDescription", "subject", "errorMessage") else 90
            L += [f"| `{p}` | {'`' + _fmt(v, full(p)) + '`' if isinstance(v, str) and (v.startswith('=') or '{{' in v) else _fmt(v, full(p)).replace('<', '&lt;').replace('>', '&gt;')} |" for p, v in rows[:24]]
            if len(rows) > 24:
                L.append(f"| … | {len(rows) - 24} more in workflow.json |")
        else:
            L.append("*No settings. This node works with its defaults.*")
        for key, lang, title in (("jsCode", "javascript", "Code"), ("jsonSchemaExample", "json", "Schema example"), ("inputSchema", "json", "JSON schema")):
            src = n["parameters"].get(key)
            if src:
                if lang == "json":
                    try:
                        src = json.dumps(json.loads(src), indent=2, ensure_ascii=False)
                    except ValueError:
                        pass
                L += ["", f"**{title}:**", "", f"```{lang}", src.rstrip(), "```"]
        L += ["", "</details>", ""]
    L += ["> [!TIP]", "> ⚙️ rows come from each node's **Settings** tab, not its Parameters tab. `{{ … }}` values are **expressions** evaluated at run time. See [workflow anatomy](../../docs/workflow-anatomy.md) for what every property means.", ""]
    return "\n".join(L)


def placeholders(wf):
    hits = []
    for n in wf["nodes"]:
        if "stickyNote" in n["type"]:
            continue
        for path, val in _flatten(n["parameters"]):
            if isinstance(val, str) and any(p in val for p in PLACEHOLDERS):
                hits.append((n["name"], _clean_path(path), val.lstrip("=")))
    creds = sorted({TYPES.get(_short(n["type"]), (_short(n["type"]),))[0] for n in wf["nodes"]
                    if _short(n["type"]) in ("gmail", "gmailTrigger", "googleSheets", "googleDrive", "jira", "lmChatGoogleGemini", "embeddingsGoogleGemini")
                    or (_short(n["type"]) == "httpRequest" and n["parameters"].get("authentication"))})
    L = ["## 📝 Before you run it", ""]
    if hits:
        L += ["Replace these placeholder values with your own:", "", "| Node | Field | Placeholder |", "|---|---|---|"]
        L += [f"| {a} | `{b}` | `{_fmt(c)}` |" for a, b, c in hits]
        L.append("")
    else:
        L += ["No placeholder values. It runs as-is once the credentials are connected.", ""]
    if creds:
        L += ["Nodes that need a credential selected after import: " + ", ".join(f"**{c}**" for c in creds) + ".", ""]
    return "\n".join(L)
