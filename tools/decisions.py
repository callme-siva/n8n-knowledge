"""Design decisions & trade-offs for the real-world projects: (decision, why, trade-off / alternative)."""

DECISIONS = {
    "P01": [
        ("AI extracts fields, **code** re-checks subtotal + tax = total and GSTIN format", "LLMs misread digits and do arithmetic badly; a 10-line check catches it deterministically", "Adds a validation step to maintain. Alternative: OCR-specialised invoice APIs (costlier, less flexible)"),
        ("Dedupe key = normalised vendor + invoice number, remembered across runs", "Suppliers resend invoices; paying twice is the most expensive AP mistake", "Same number reused by two vendors is fine; a vendor reusing numbers would be blocked (rare, shows in logs)"),
        ("Approval only **above a threshold**", "Humans approve what matters; small invoices flow straight through", "The threshold must be tuned. Too low creates a bottleneck; too high adds risk"),
        ("Bad invoices go to an **Exceptions** sheet + email, never silently dropped", "Silent drops are how automations lose trust", "Someone must own the exceptions queue daily"),
        ("Gmail label `invoices` as the entry point", "Lets humans control what enters the pipeline with a normal Gmail filter", "Relies on the filter being right; a dedicated AP mailbox is cleaner at scale"),
    ],
    "P02": [
        ("Classify first, answer only \"Question\" emails", "Cheap triage avoids spending an LLM answer on spam or angry escalations", "Two model calls per question email. Could merge into one prompt, at the cost of clarity"),
        ("Ground answers in a **Google Sheet FAQ**", "Support leads can edit answers without touching the workflow", "Doesn't scale past ~100 entries in one prompt; then move to RAG (L13)"),
        ("Create a **draft**, never send", "Wrong answers never reach customers; agents stay in control", "Saves less time than auto-send. That's the price of safety until accuracy is proven"),
        ("Gate on confidence ≥ 0.75 **and** `needs_human = false`", "Models are overconfident; two signals are safer than one", "Threshold chosen by judgement. Tune it with real data"),
    ],
    "P03": [
        ("Dedupe by alert **fingerprint** kept in workflow static data", "Monitoring re-fires every minute; one problem should be one incident", "Static data is per-workflow and not shared across instances; use a DB table in HA setups"),
        ("Severity matrix in one Switch: page / notify / resolve / suppress", "The policy is visible in one place and easy to change", "Doesn't cover time-based escalation (add a Wait + acknowledgement check)"),
        ("Store the Jira key against the fingerprint", "The resolve event must find the incident it belongs to", "If static data is lost, resolves can't link back (they're ignored safely)"),
        ("AI writes a postmortem **draft** with \"never invent facts\"", "Removes the blank-page problem; humans add root cause", "Draft quality depends on alert annotations. Richer alerts give better drafts"),
        ("Header auth on the webhook", "Anyone who can post alerts can page your on-call engineer", "Monitoring tools must be configured with the token"),
    ],
    "P04": [
        ("One long-running execution per lead, using **Wait** nodes", "The whole sequence is readable in one place; state lives in the execution", "Needs Postgres + an always-on instance; thousands of waiting executions use DB space"),
        ("Reply detection by Gmail search (`from:lead after:start`)", "No extra tools or tracking pixels needed", "Only sees replies to the sending mailbox; misses replies from colleagues' addresses"),
        ("Separate short branch per stage (`replied_after_email_N`)", "No crossing flows, plus you learn which email converts", "Slight duplication of the CRM + Slack pair per stage"),
        ("CRM updates map values inline (append-or-update by email)", "Fewer nodes; the row key is explicit", "Column names must match the sheet exactly"),
    ],
    "P05": [
        ("Read only `status = pending` rows", "Makes every run **resumable** and idempotent", "The status column is critical; protect it from manual edits"),
        ("Batches of 10 + a 2 s wait", "Stays under API rate limits and keeps memory flat", "Slower than full speed. Tune the batch size to your API tier"),
        ("Per-row error output → `status = error` with reason", "One bad row never stops the other 999", "Errors need a periodic review and re-queue"),
        ("Limit 500 per run", "Caps cost and runtime of a single execution", "Big lists take several runs (schedule it nightly)"),
        ("Summary counts from the loop's **done** output", "`$('node').all()` inside a loop returns only the last batch (a real bug we caught in testing)", "None; this is simply the correct way"),
    ],
    "P06": [
        ("Chained Send-and-Wait approvals with **3-day limits**", "Approvals can't hang forever; timeouts escalate", "Email-based approvals depend on a reachable n8n (`WEBHOOK_URL`)"),
        ("Switch on approved / rejected / **missing** decision", "A timeout is a distinct outcome and must not be read as \"rejected\"", "One more branch to design and test"),
        ("Threshold rule in the Config node", "Finance can change the policy without editing logic", "More complex rule sets (per cost centre) outgrow a Set node; use a lookup sheet"),
        ("Upsert the same audit row as status changes", "One row per request = an easy audit trail and reporting", "No history of intermediate states; add an append-only log if auditors need it"),
    ],
    "P07": [
        ("Checklist generated from data (common + per-role tasks)", "HR edits a list, not a workflow; new roles are one line", "Lives in code for now; a sheet makes it fully no-code"),
        ("Two parallel branches joined by Merge (combine by position)", "Jira and Calendar don't depend on each other, so run them in parallel", "Each branch must output exactly one item (hence Aggregate)"),
        ("Welcome email **after** tasks and events exist", "The summary can include real links, and nothing is announced that failed", "If Jira is down, the welcome waits. Add Retry on Fail and the error workflow"),
        ("Session times built in the workflow timezone", "10:00 must mean 10:00 for the team, not UTC", "Distributed teams need per-person timezones"),
    ],
    "P08": [
        ("One-way sync (Sheet → Jira)", "One source of truth avoids conflict resolution entirely", "Edits made in Jira are overwritten on the next change in the sheet"),
        ("SHA-256 hash of business fields as change detector", "Cheap, deterministic, no timestamps or history needed", "Hash only business fields; including volatile ones causes endless updates"),
        ("Write `jira_key` + `sync_hash` back to the sheet", "Makes the sync idempotent and restartable", "Users can break it by deleting the key. Protect those columns"),
        ("Stable `row_id` as the upsert key", "Row numbers shift when people sort; IDs don't", "Someone must create IDs (a formula or a form)"),
    ],
    "P09": [
        ("Plan → search → read → cross-check → cite, spelled out in the system prompt", "Agents perform much better with an explicit procedure", "Longer prompt, more tokens per run"),
        ("A `read_page` tool (not just search snippets)", "Snippets are too thin to cite; pages carry the facts", "Page reads are the main cost; capped by `maxLength` and `maxIterations`"),
        ("\"Not found\" is an acceptable answer", "Hallucinated sources destroy trust in the whole report", "Reports can look incomplete. That's honest, and the right trade"),
        ("Email a draft labelled \"verify key facts\"", "Sets expectations: the agent saves time, humans stay accountable", "Needs a human reviewer for anything decision-critical"),
    ],
    "P10": [
        ("Expose tools through the **MCP Server Trigger**", "One governed endpoint works with Claude, ChatGPT, Cursor and IDE agents", "Clients must support HTTP MCP; the workflow must be active"),
        ("Tools as sub-workflows with `$fromAI()` parameters", "Each tool is testable on its own and reusable in normal workflows", "More workflows to manage (naming and IDs matter)"),
        ("Bearer auth + read-only tools first", "Least privilege: assistants can look things up but not change data", "Write actions need an approval pattern before exposure"),
    ],
    "P11": [
        ("Redact with **reversible tokens** (`[EMAIL_1]`)", "The model never sees raw PII, yet the caller gets a usable answer", "The token map lives only in the execution; don't log it"),
        ("Luhn-check card numbers before redacting", "Cuts false positives on long IDs and phone-like numbers", "Other identifiers (names, addresses) need NER models"),
        ("Keyword injection screen → 403", "Blocks the laziest attacks cheaply", "Easy to bypass; it's a first layer, not a boundary"),
        ("Audit only redacted text + PII counts", "Compliance evidence without creating a new PII store", "Harder to debug a specific user's issue (by design)"),
    ],
    "P12": [
        ("Fetch three sources **in parallel**, join with Merge", "Faster, and each source can fail and retry independently", "Every branch must return exactly one item"),
        ("KPIs and deltas computed in code; AI only narrates", "Numbers stay exact; the AI adds the so-what", "The narrative is only as good as the metrics you choose"),
        ("Last week's KPIs kept in static data", "Week-over-week change with no extra database", "Lost on re-import; store weekly KPIs in a sheet for long trends"),
        ("Chart + narrative merged before the email", "One email with everything, in a predictable order", "A failed chart blocks the email. Add On Error → continue for non-critical parts"),
    ],
}
