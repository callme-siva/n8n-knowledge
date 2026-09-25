<div align="center">

# 🧠 Self-check quiz

**30 questions, 5 per track. Answer in your head first, then open the answer.**

</div>

---

**Contents:** [🟢 Basics](#-basics-l01l05) · [🟡 Integrations](#-integrations-l06l10) · [🟠 AI](#-ai-l11l15) · [🔴 Multi-agent & production](#-multi-agent--production-l16l22) · [⚡ Quick wins](#-quick-wins-q01q08) · [🏭 Real-world projects](#-real-world-projects-p01p12)

> [!TIP]
> Scoring 4/5 on a track means you're ready for the next one. Below 3/5, re-read the lesson's **💡 Concept first** block and do its ⭐ challenge.

## 🟢 Basics (L01–L05)

**1.** A Set node outputs 3 items and is connected to a Gmail node. How many emails are sent?
<details><summary>Answer</summary>

**3.** Most nodes run once per item. To send one email, combine first (Aggregate, or Code in *Run once for all items*). → [L01](../workflows/L01-hello-n8n/README.md)
</details>

**2.** Your schedule-triggered workflow works when you click *Execute workflow* but never runs by itself. Most likely cause?
<details><summary>Answer</summary>

The workflow isn't **Active**. Triggers only fire automatically for active workflows. (Second most likely: the machine running n8n was asleep.) → [L02](../workflows/L02-daily-weather-email/README.md)
</details>

**3.** What's the difference between `{{ $json.city }}` and `{{ $('⚙️ Config').item.json.city }}`?
<details><summary>Answer</summary>

`$json` is the **current** item's data (the node's direct input). `$('⚙️ Config').item` reaches back to the item from an **earlier** node that's paired with the current one. → [workflow anatomy](workflow-anatomy.md#5-expressions-cheat-sheet)
</details>

**4.** A Switch compares `{{ $json.rate }}` ≥ 88.5 but every item goes to the fallback, even when the rate is 90. Why?
<details><summary>Answer</summary>

`rate` is a **string** (`"90"`), so the numeric comparison fails. Set the field type to *Number* in the Set node, or use `Number($json.rate)`. → [L04](../workflows/L04-currency-alert-switch/README.md)
</details>

**5.** In a Code node set to *Run once for all items*, what must you return?
<details><summary>Answer</summary>

An **array of items**: `[{ json: {...} }, …]`. In *Run once for each item* mode you return a single `{ json: {...} }`. → [L05](../workflows/L05-rss-news-code-node/README.md)
</details>

## 🟡 Integrations (L06–L10)

**6.** A Gmail-triggered workflow uploads the same PDF to Drive every 5 minutes. What's missing?
<details><summary>Answer</summary>

**Idempotency**: nothing marks the email as processed. Mark it as read or add a label, and filter on it in the trigger. → [L06](../workflows/L06-gmail-pdf-to-drive/README.md)
</details>

**7.** Your form writes to Google Sheets but the columns stay empty. First thing to check?
<details><summary>Answer</summary>

That the **field names match the sheet headers exactly** (case and spaces). Use the lesson's CSV template to create the tab. → [L07](../workflows/L07-lead-capture-sheets/README.md)
</details>

**8.** Your Jira search returns 0 issues and the rest of the workflow silently doesn't run. How do you still send an "all clear" email?
<details><summary>Answer</summary>

Turn on **Always Output Data** on the Jira node, then branch on whether real items exist. → [L08](../workflows/L08-jira-stale-stories/README.md)
</details>

**9.** Why should a public webhook have authentication, even for "harmless" data like expenses?
<details><summary>Answer</summary>

Anyone who finds the URL can write data, trigger costs, or fill your sheet with junk. Use **Header Auth** (and validate input). → [L09](../workflows/L09-webhook-expense-api/README.md)
</details>

**10.** `/webhook-test/expense` works but `/webhook/expense` returns 404. Why?
<details><summary>Answer</summary>

The **test URL** only listens while you click *Listen*. The **production URL** only works when the workflow is **active**. → [L09](../workflows/L09-webhook-expense-api/README.md)
</details>

## 🟠 AI (L11–L15)

**11.** You need the AI's answer to decide which IF branch to take. What node setup do you use?
<details><summary>Answer</summary>

An LLM chain with **Require specific output format** + a **Structured Output Parser**, so you get JSON fields (e.g. `tier`, `score`) your IF/Switch can read. → [L12](../workflows/L12-meeting-transcript-raid-log/README.md)
</details>

**12.** Your RAG bot answers questions confidently even when the policy doesn't cover them. Two fixes?
<details><summary>Answer</summary>

(1) A system prompt that says *answer only from the tool; otherwise say you don't know*. (2) A specific tool description, with low temperature. Also check that the same embedding model is used for insert and search. → [L13](../workflows/L13-rag-policy-chatbot/README.md)
</details>

**13.** When should you use an **AI Agent** instead of a Basic LLM Chain?
<details><summary>Answer</summary>

When the model must **decide which tools to call** (look something up, calculate, fetch). For a fixed prompt → answer, a chain is cheaper, faster and predictable. → [L14](../workflows/L14-ai-agent-with-tools/README.md)
</details>

**14.** Why should arithmetic (GST, totals) be done by a Calculator tool or Code, not the LLM?
<details><summary>Answer</summary>

LLMs predict text; they can produce plausible **wrong numbers**. Code and calculators are exact. → [L14](../workflows/L14-ai-agent-with-tools/README.md), [P01](../workflows/P01-invoice-processing-pipeline/README.md)
</details>

**15.** What happens to an execution while a *Send and Wait* approval email is unanswered?
<details><summary>Answer</summary>

It **pauses** (status *Waiting*) until the person clicks a button or the wait limit expires. Set a limit, and handle the timeout path. → [L15](../workflows/L15-retro-ai-approval-jira/README.md), [P06](../workflows/P06-purchase-approval-multilevel/README.md)
</details>

## 🔴 Multi-agent & production (L16–L22)

**16.** What does an auto-fixing output parser do?
<details><summary>Answer</summary>

If the model returns malformed JSON, a second model call **repairs it to match the schema** before the workflow continues. → [L17](../workflows/L17-complaint-handler-multi-agent/README.md)
</details>

**17.** You test your error workflow by clicking *Execute* on a failing workflow, but no alert arrives. Why?
<details><summary>Answer</summary>

Error workflows fire for **production** (automatic) executions, not manual test runs. → [L19](../workflows/L19-global-error-handler/README.md)
</details>

**18.** Name two benefits of sub-workflows.
<details><summary>Answer</summary>

**Reuse** (change the email template once, every caller updates) and **smaller, testable pieces** (each with typed inputs and one job). → [L20](../workflows/L20-subworkflows-caller/README.md)
</details>

**19.** Why does the uptime monitor alert on *change* instead of every failed check?
<details><summary>Answer</summary>

Alerting every 5 minutes during an outage causes **alert fatigue**; people start ignoring alerts. One alert on DOWN, one on recovery. → [L21](../workflows/L21-website-uptime-monitor/README.md)
</details>

**20.** In a lead-scoring workflow, why store the AI's `reason` next to the `score`?
<details><summary>Answer</summary>

So humans can **audit and tune** the scoring. A score without a reason is a black box nobody trusts. → [L22](../workflows/L22-ai-lead-qualifier-router/README.md)
</details>

## ⚡ Quick wins (Q01–Q09)

**21.** Why is `new Date().toISOString().slice(0, 10)` a bad way to get "today" in n8n?
<details><summary>Answer</summary>

It's **UTC**: near midnight it gives yesterday or tomorrow in your timezone. Use `$today.toISODate()`, which follows the workflow timezone. (Our test harness caught this bug in 7 workflows.) → [Q06](../workflows/Q06-invoice-due-reminders/README.md)
</details>

**22.** How does Q06 avoid emailing the same client twice on the same day?
<details><summary>Answer</summary>

It writes **`last_reminded`** back to the sheet (append-or-update by `invoice_no`) and skips rows already reminded today. → [Q06](../workflows/Q06-invoice-due-reminders/README.md)
</details>

**23.** What does *Remove Duplicates → items processed in previous executions* remember?
<details><summary>Answer</summary>

The **dedupe values** (e.g. links) it has seen in earlier runs of that node, up to the history size, so each item is processed once, ever. → [Q08](../workflows/Q08-rss-to-telegram-dedupe/README.md)
</details>

**24.** In a Text Classifier, what matters most for accuracy?
<details><summary>Answer</summary>

The **category descriptions**: they are the prompt. Add typical words and examples, and measure accuracy on real data. → [Q07](../workflows/Q07-gmail-ai-auto-labeler/README.md)
</details>

**25.** Why does a scraped price sometimes come back as `NaN`?
<details><summary>Answer</summary>

The CSS selector matched nothing, often because the site renders prices with **JavaScript**. Use the site's API or JSON endpoint instead. → [Q02](../workflows/Q02-price-drop-tracker/README.md)
</details>

## 🏭 Real-world projects (P01–P12)

**26.** In the invoice pipeline, who does what: AI, code, human?
<details><summary>Answer</summary>

**AI extracts** the fields, **code validates** (totals, GSTIN, duplicates), and a **human approves** above the threshold. Invalid invoices go to an exceptions queue. → [P01](../workflows/P01-invoice-processing-pipeline/README.md)
</details>

**27.** Inside a Loop Over Items, `$('Checkpoint').all().length` returns 3 even though 23 rows were processed. Why, and what's the fix?
<details><summary>Answer</summary>

Inside loops, `$('Node').all()` returns only that node's **last run** (the last batch). Count from the loop's **done** output (`$input.all()`) instead. → [P05](../workflows/P05-bulk-ai-enrichment-checkpointed/README.md)
</details>

**28.** What three things make the Sheets → Jira sync idempotent?
<details><summary>Answer</summary>

A stable **row_id**, the **jira_key written back** after creation, and a **content hash** to detect changes (create / update / skip). → [P08](../workflows/P08-sheets-jira-sync-hashing/README.md)
</details>

**29.** Why does the PII gateway use reversible tokens like `[EMAIL_1]` rather than deleting personal data?
<details><summary>Answer</summary>

The model never sees the raw data, but the **caller still gets a usable answer** with the real values restored, and the audit log stays PII-free. → [P11](../workflows/P11-pii-safe-ai-gateway/README.md)
</details>

**30.** In the executive KPI report, why are the numbers computed in code and not by the LLM?
<details><summary>Answer</summary>

**Numbers from code, narrative from AI.** Code is exact and auditable; the model only explains numbers it's given, so it can't invent KPIs. → [P12](../workflows/P12-weekly-exec-kpi-report/README.md)
</details>

---

<p align="center"><a href="../README.md">← Back to the learning path</a> · <a href="common-mistakes.md">🧯 Common mistakes</a></p>
