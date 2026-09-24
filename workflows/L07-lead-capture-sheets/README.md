<div align="center">

# L07 · Lead capture form → Sheets → welcome email

![level: Integrations](https://img.shields.io/badge/level-Integrations-D4A106?style=flat-square) ![domain: Sales / marketing](https://img.shields.io/badge/domain-Sales_/_marketing-334155?style=flat-square) ![build time: 20 min](https://img.shields.io/badge/build_time-20_min-0EA5E9?style=flat-square) ![nodes: 4](https://img.shields.io/badge/nodes-4-7C3AED?style=flat-square) [![e2e test: passed · 2 checks](https://img.shields.io/badge/e2e_test-passed_%C2%B7_2_checks-2EA44F?style=flat-square)](https://github.com/callme-siva/n8n-knowledge/actions/workflows/validate.yml)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** A small business or freelancer needs a *Contact us* form that stores the lead somewhere useful and replies instantly. No Typeform, no CRM subscription.

## 💡 Concept first

**📌 Key idea:** A form + a sheet is the simplest possible **system of record**: capture, clean, store, acknowledge.

**🧠 Mental model:** A reception desk: take the visitor's details, write them neatly in the register, hand them a receipt.

**🚫 When *not* to use it:** Don't use Sheets as a database beyond a few thousand rows or with several writers at once. Move to Airtable, Postgres or a CRM.

## 🎯 What you'll learn

- n8n **Form Trigger**: a hosted form with no web developer needed
- Cleaning input (trim, lowercase) in a Set node
- Google Sheets **Append row** with auto-mapped columns
- Sending a personalised email to the submitter

## 🏗️ Architecture

**System context:** who and what this workflow talks to, and what crosses each boundary. 🔑 = needs a credential · 🧑 = a human decides.

```mermaid
flowchart LR
  s0(["👤 Person filling the form"]):::person
  core{{"⚙️ n8n workflow<br/><small>4 nodes</small>"}}:::n8n
  s1["📊 Google Sheets 🔑"]:::saas
  s2["📧 Gmail 🔑"]:::saas
  s0 -->|"form submission"| core
  core -->|"writes rows"| s1
  core -->|"sends email"| s2
  classDef person fill:#FFF4E5,stroke:#F59E0B,color:#1F2937
  classDef saas fill:#EAF3FF,stroke:#2563EB,color:#1F2937
  classDef n8n fill:#FFF1F4,stroke:#EA4B71,stroke-width:3px,color:#1F2937
```

<details><summary><b>Node-level flow</b> (every node and branch)</summary>

```mermaid
flowchart LR
  n0(["Lead Form"]):::trigger
  n1["Clean Lead"]:::code
  n2["Append to Leads Sheet"]:::data
  n3["Welcome Email"]:::msg
  n0 --> n1
  n1 --> n2
  n2 --> n3
  classDef trigger fill:#E8F7EE,stroke:#2EA44F,stroke-width:2px,color:#1F2937
  classDef code fill:#EEF2F7,stroke:#64748B,stroke-width:2px,color:#1F2937
  classDef data fill:#EAF3FF,stroke:#2563EB,stroke-width:2px,color:#1F2937
  classDef msg fill:#FFEDEF,stroke:#E11D48,stroke-width:2px,color:#1F2937
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Google Sheets OAuth2 | [docs/credentials.md](../../docs/credentials.md) |
| Gmail OAuth2 | [docs/credentials.md](../../docs/credentials.md) |

## 📝 Before you run it

Replace these placeholder values with your own:

| Node | Field | Placeholder |
|---|---|---|
| Append to Leads Sheet | `documentId` | `PASTE_YOUR_GOOGLE_SHEET_URL` |

Nodes that need a credential selected after import: **Gmail**, **Google Sheets**.

### 📥 Starter files

Create each tab from its template, so column names match exactly: **Google Sheets → File → Import → Upload** the CSV → *Insert new sheet(s)*. The tab takes the file's name.

| Tab | Template | Columns |
|---|---|---|
| `Leads` | [Leads.csv](../../templates/L07-lead-capture-sheets/Leads.csv) | `timestamp`, `email`, `name`, `company`, `budget`, `interest`, `source` |

<sub>Columns are generated from what this workflow actually reads and writes in the automated test, so they can't drift from the workflow.</sub>

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Create a Google Sheet named *Leads* with header row: `timestamp, name, email, company, interest, budget, source`.
2. Add **n8n Form Trigger** with the 5 fields (Email field type = *Email*).
3. Open the **Test URL**, submit once, and look at the output keys: they are the field labels.
4. Add a **Set** node that renames and cleans the fields so they match your sheet headers exactly.
5. Add **Google Sheets → Append row**. Paste the sheet URL, pick the tab, *Map automatically*.
6. Add Gmail to `{{ $('Clean Lead').item.json.email }}`.

## 🔍 Node-by-node reference

Every node in this workflow and every setting inside it, generated from [`workflow.json`](workflow.json). Click a node to expand it.

<details><summary><b>1. Lead Form</b> · <code>n8n Form Trigger</code> v2.2</summary>

> Hosts a web form; each submission starts one execution. Field labels become JSON keys.

| Property | Value |
|---|---|
| `formTitle` | Book a free demo |
| `formDescription` | Tell us a little about you. We reply within one business day. |
| `formFields.values` | Name *, Email *, Company, Interested in *, Monthly budget (INR) |
| `respondWithOptions.formSubmittedText` | Thanks! Check your inbox for a confirmation. |

</details>

<details><summary><b>2. Clean Lead</b> · <code>Edit Fields (Set)</code> v3.4</summary>

> Creates, renames or overwrites fields without code.

| Property | Value |
|---|---|
| `timestamp` | `{{ $now.toISO() }}` |
| `name` | `{{ $json.Name.trim() }}` |
| `email` | `{{ $json.Email.trim().toLowerCase() }}` |
| `company` | `{{ $json.Company \|\| '-' }}` |
| `interest` | `{{ $json['Interested in'] }}` |
| `budget` | `{{ $json['Monthly budget (INR)'] \|\| 'not given' }}` |
| `source` | web-form |

</details>

<details><summary><b>3. Append to Leads Sheet</b> · <code>Google Sheets</code> v4.5</summary>

> Reads, appends or updates rows in a spreadsheet.

| Property | Value |
|---|---|
| `operation` | append |
| `documentId` | PASTE_YOUR_GOOGLE_SHEET_URL |
| `sheetName` | Leads |
| `columns.mappingMode` | autoMapInputData |
| `⚙️ Retry on fail` | ✅ on |
| `⚙️ Max tries` | 3 |
| `⚙️ Wait between tries (ms)` | 3000 |

</details>

<details><summary><b>4. Welcome Email</b> · <code>Gmail</code> v2.1</summary>

> Sends, reads or labels email. `sendAndWait` pauses the workflow for a human reply.

| Property | Value |
|---|---|
| `sendTo` | `{{ $('Clean Lead').item.json.email }}` |
| `subject` | `Thanks {{ $('Clean Lead').item.json.name }} — your demo request` |
| `emailType` | html |
| `message` | `<p>Hi {{ $('Clean Lead').item.json.name }},</p><p>Thanks for your interest in <b>{{ $('Clean Lead').item.json.interest }}</b>. We'll reply within one business day with a few slots.</p><p>— Team</p>` |
| `appendAttribution` | off |
| `⚙️ Retry on fail` | ✅ on |
| `⚙️ Max tries` | 3 |
| `⚙️ Wait between tries (ms)` | 3000 |

</details>

> [!TIP]
> ⚙️ rows come from each node's **Settings** tab, not its Parameters tab. `{{ … }}` values are **expressions** evaluated at run time. See [workflow anatomy](../../docs/workflow-anatomy.md) for what every property means.

## ✅ Test it

> [!TIP]
> **Automated end-to-end test: passed.** 4/4 nodes executed in real n8n (3 credentialed or AI nodes replaced by fixtures, so AI output itself isn't tested), 2 behaviour checks. See [tests/](../../tests/README.md).

- [ ] Submit the form 3 times with different data. You should see 3 rows and 3 emails.
- [ ] Activate it and share the **Production URL**.

## 🧯 Troubleshooting

Problems specific to this workflow are below. For general ones (expressions, items, triggers, AI), see [common mistakes](../../docs/common-mistakes.md).

<details><summary><b>Columns are empty in the sheet</b></summary>

The header names don't exactly match the Set field names. Spaces and case matter.

</details>

<details><summary><b>The Test URL stops working</b></summary>

Test URLs listen only while you click *Execute*. Use the Production URL once the workflow is active.

</details>

## 🏋️ Practice

Try each challenge **before** opening the hint. Solutions show the exact expressions and code.

**⭐ Challenge 1:** Reject personal email domains (gmail, yahoo, hotmail) with a polite message.

<details><summary>💡 Hint</summary>

Add an IF after *Clean Lead*.

</details>
<details><summary>✅ Solution</summary>

IF `{{ /@(gmail|yahoo|hotmail|outlook)\./i.test($json.email) }}` *is true*: send a "please use your work email" reply and stop. On false, continue to Sheets.

</details>

**⭐⭐ Challenge 2:** Don't store duplicate leads. Update the existing row instead.

<details><summary>💡 Hint</summary>

Sheets has an *Append or Update* operation with a matching column.

</details>
<details><summary>✅ Solution</summary>

Change the Sheets operation to **Append or Update Row**, matching column `email`. Resubmitting the form now updates the same row (like Q06 and P04).

</details>

## 🚀 Ideas to extend it

- Add a duplicate check: *Sheets → Get rows* filtered by email before appending.
- Score the lead with AI and route hot leads to Slack (see **L22**).

---

<p align="center"><a href="../L06-gmail-pdf-to-drive/README.md">← L06 · Save Gmail PDF attachments to Google Drive</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L08-jira-stale-stories/README.md">L08 · Daily stale Jira stories report →</a></p>
