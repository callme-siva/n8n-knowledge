<div align="center">

# L07 · Lead capture form → Sheets → welcome email

![level: Integrations](https://img.shields.io/badge/level-Integrations-D4A106?style=flat-square) ![domain: Sales / marketing](https://img.shields.io/badge/domain-Sales_/_marketing-334155?style=flat-square) ![build time: 20 min](https://img.shields.io/badge/build_time-20_min-0EA5E9?style=flat-square) ![nodes: 4](https://img.shields.io/badge/nodes-4-7C3AED?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** A small business or freelancer needs a *Contact us* form that stores the lead somewhere useful and replies instantly. No Typeform, no CRM subscription.

## 🎯 What you'll learn

- n8n **Form Trigger**: a hosted form with no web developer needed
- Cleaning input (trim, lowercase) in a Set node
- Google Sheets **Append row** with auto-mapped columns
- Sending a personalised email to the submitter

## 🏗️ Architecture

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
  classDef ai fill:#F1EBFF,stroke:#7C3AED,stroke-width:2px,color:#1F2937
  classDef sub fill:#F7F3FF,stroke:#A78BFA,stroke-width:2px,color:#1F2937
  classDef logic fill:#FFF4E5,stroke:#F59E0B,stroke-width:2px,color:#1F2937
  classDef code fill:#EEF2F7,stroke:#64748B,stroke-width:2px,color:#1F2937
  classDef data fill:#EAF3FF,stroke:#2563EB,stroke-width:2px,color:#1F2937
  classDef http fill:#E6FAF8,stroke:#0D9488,stroke-width:2px,color:#1F2937
  classDef msg fill:#FFEDEF,stroke:#E11D48,stroke-width:2px,color:#1F2937
```

<details><summary>Plain-text flow</summary>

```
Form → Set (clean) → Google Sheets append → Gmail welcome
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

</details>

> [!TIP]
> ⚙️ rows come from each node's **Settings** tab, not its Parameters tab. `{{ … }}` values are **expressions** evaluated at run time. See [workflow anatomy](../../docs/workflow-anatomy.md) for what every property means.

## ✅ Test it

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

## 🚀 Level up

- Add a duplicate check: *Sheets → Get rows* filtered by email before appending.
- Score the lead with AI and route hot leads to Slack (see **L22**).

---

<p align="center"><a href="../L06-gmail-pdf-to-drive/README.md">← L06 · Save Gmail PDF attachments to Google Drive</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L08-jira-stale-stories/README.md">L08 · Daily stale Jira stories report →</a></p>
