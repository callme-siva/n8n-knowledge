<div align="center">

# L12 · Meeting transcript → RAID log

![level: AI](https://img.shields.io/badge/level-AI-F97316?style=flat-square) ![domain: Project management](https://img.shields.io/badge/domain-Project_management-334155?style=flat-square) ![build time: 30 min](https://img.shields.io/badge/build_time-30_min-0EA5E9?style=flat-square) ![nodes: 7](https://img.shields.io/badge/nodes-7-7C3AED?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** After a steering committee or status meeting, someone should update the RAID log. Usually nobody does. Paste the transcript (from Teams, Zoom or Meet) and every risk, assumption, issue and dependency lands in a sheet with owner, impact and due date.

## 🎯 What you'll learn

- **Structured Output Parser**: force the LLM to follow a JSON schema
- `hasOutputParser` on the LLM Chain
- **Split Out**: one AI answer → many items
- Mapping AI fields to spreadsheet columns

## 🏗️ Architecture

```mermaid
flowchart LR
  n0(["Submit Meeting Transcript"]):::trigger
  n1[["Extract RAID"]]:::ai
  n2("RAID Analysis Model"):::sub
  n3("RAID Parser"):::sub
  n4["Split RAID Items"]:::logic
  n5["Build RAID Row"]:::code
  n6["Append RAID to Sheet"]:::data
  n0 --> n1
  n1 --> n4
  n2 -.->|languageModel| n1
  n3 -.->|outputParser| n1
  n4 --> n5
  n5 --> n6
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
Form (transcript) → LLM Chain ⇐ Gemini, ⇐ Structured Parser → Split Out items → Set row → Sheets append
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Google Gemini API key | [docs/credentials.md](../../docs/credentials.md) |
| Google Sheets OAuth2 | [docs/credentials.md](../../docs/credentials.md) |

## 📝 Before you run it

Replace these placeholder values with your own:

| Node | Field | Placeholder |
|---|---|---|
| Append RAID to Sheet | `documentId` | `PASTE_YOUR_GOOGLE_SHEET_URL` |

Nodes that need a credential selected after import: **Google Gemini Chat Model**, **Google Sheets**.

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Create a Sheet tab **RAID** whose headers match the fields in *Build RAID Row*.
2. Form Trigger: meeting title, date, transcript (textarea).
3. **Basic LLM Chain** → turn on *Require Specific Output Format* → attach a **Structured Output Parser** and paste an example JSON (`items: [{category, description, owner, impact, ...}]`).
4. Attach the Gemini model.
5. **Split Out** on `output.items`.
6. **Set** the row columns, then **Sheets → Append**.

## 🔍 Node-by-node reference

Every node in this workflow and every setting inside it, generated from [`workflow.json`](workflow.json). Click a node to expand it.

<details><summary><b>1. Submit Meeting Transcript</b> · <code>n8n Form Trigger</code> v2.6</summary>

> Hosts a web form; each submission starts one execution. Field labels become JSON keys.

| Property | Value |
|---|---|
| `formTitle` | Project Meeting Transcript — RAID Analysis |
| `formDescription` | Paste a raw transcript from a project status, steering committee, sprint review, or gov… |
| `formFields.values` | Meeting Title *, Meeting Date *, Meeting Type *, Transcript * |

</details>

<details><summary><b>2. Extract RAID</b> · <code>Basic LLM Chain</code> v1.9</summary>

> Sends one prompt to a model and returns the answer. Simplest AI node.

| Property | Value |
|---|---|
| `promptType` | define |
| `text` | `Analyse the following project meeting transcript and identify every Risk, Assumption, Issue and Dependency (RAID).  Meeting Title: {{ $json["Meeting Title"] }} Meeting Type: {{ $json["Meeting Type"] }} Meeting Date: {{ $json["Meeting Date"] }}  Transcript: {{ $json["Transcript"] }}` |
| `hasOutputParser` | ✅ on |
| `messages.message` | You are an experienced project-management analyst. Read the meeting transcript and extract a flat list of RAID items. For each item set "category" to exactly one of: "Risk", "Assumption", "Issue", "Dependency". Provide a concise "description", the responsible "owner" (use "Unassigned" if none is stated), the "impact", and a "mitigation" or next step ("N/A" if none). Only include items genuinely supported by the transcript. If a category has no items, simply omit them. Return the result using the required structured format. |

</details>

<details><summary><b>3. RAID Analysis Model</b> · <code>Google Gemini Chat Model</code> v1</summary>

> The language model plugged into a chain or agent.

| Property | Value |
|---|---|
| `modelName` | models/gemini-2.5-flash |
| `temperature` | 0.2 |

</details>

<details><summary><b>4. RAID Parser</b> · <code>Structured Output Parser</code> v1.3</summary>

> Forces the model's answer into JSON matching your schema.

| Property | Value |
|---|---|
| `jsonSchemaExample` | (JSON schema, 18 lines, shown below) |

**Schema example:**

```json
{
  "items": [
    {
      "category": "Risk",
      "description": "Third-party vendor may miss the integration deadline.",
      "owner": "Jane Doe",
      "impact": "Could delay go-live by two weeks.",
      "mitigation": "Escalate to vendor account manager and prepare fallback."
    },
    {
      "category": "Dependency",
      "description": "Release depends on the security team completing the pen test.",
      "owner": "Security Team",
      "impact": "Blocks production deployment until resolved.",
      "mitigation": "Book pen-test slot for next sprint."
    }
  ]
}
```

</details>

<details><summary><b>5. Split RAID Items</b> · <code>Split Out</code> v1</summary>

> Turns one item holding an array into one item per array element.

| Property | Value |
|---|---|
| `fieldToSplitOut` | output.items |

</details>

<details><summary><b>6. Build RAID Row</b> · <code>Edit Fields (Set)</code> v3.5</summary>

> Creates, renames or overwrites fields without code.

| Property | Value |
|---|---|
| `meeting_title` | `{{ $("Submit Meeting Transcript").item.json["Meeting Title"] }}` |
| `meeting_date` | `{{ $("Submit Meeting Transcript").item.json["Meeting Date"] }}` |
| `meeting_type` | `{{ $("Submit Meeting Transcript").item.json["Meeting Type"] }}` |
| `category` | `{{ $json.category }}` |
| `description` | `{{ $json.description }}` |
| `owner` | `{{ $json.owner }}` |
| `impact` | `{{ $json.impact }}` |
| `mitigation` | `{{ $json.mitigation }}` |
| `logged_at` | `{{ $now.toISO() }}` |

</details>

<details><summary><b>7. Append RAID to Sheet</b> · <code>Google Sheets</code> v4.7</summary>

> Reads, appends or updates rows in a spreadsheet.

| Property | Value |
|---|---|
| `operation` | append |
| `documentId` | PASTE_YOUR_GOOGLE_SHEET_URL |
| `sheetName` | RAID |
| `columns.mappingMode` | autoMapInputData |
| `columns.schema.1.displayName` | meeting_title |
| `columns.schema.1.required` | off |
| `columns.schema.1.defaultMatch` | off |
| `columns.schema.1.display` | ✅ on |
| `columns.schema.1.type` | string |
| `columns.schema.1.canBeUsedToMatch` | ✅ on |
| `columns.schema.2.displayName` | meeting_date |
| `columns.schema.2.required` | off |
| `columns.schema.2.defaultMatch` | off |
| `columns.schema.2.display` | ✅ on |
| `columns.schema.2.type` | string |
| `columns.schema.2.canBeUsedToMatch` | off |
| `columns.schema.3.displayName` | meeting_type |
| `columns.schema.3.required` | off |
| `columns.schema.3.defaultMatch` | off |
| `columns.schema.3.display` | ✅ on |
| `columns.schema.3.type` | string |
| `columns.schema.3.canBeUsedToMatch` | off |
| `columns.schema.4.displayName` | category |
| `columns.schema.4.required` | off |
| … | 34 more in workflow.json |

</details>

> [!TIP]
> ⚙️ rows come from each node's **Settings** tab, not its Parameters tab. `{{ … }}` values are **expressions** evaluated at run time. See [workflow anatomy](../../docs/workflow-anatomy.md) for what every property means.

## ✅ Test it

- [ ] Paste a sample transcript from [docs/sample-data.md](../../docs/sample-data.md#meeting-transcript).
- [ ] Check that every row has a category from Risk/Assumption/Issue/Dependency and nothing else.

## 🧯 Troubleshooting

Problems specific to this workflow are below. For general ones (expressions, items, triggers, AI), see [common mistakes](../../docs/common-mistakes.md).

<details><summary><b>Model output doesn't fit required format</b></summary>

Lower the temperature to 0, simplify the schema example, or turn on auto-fix (L17 shows this).

</details>

<details><summary><b>Only one row appears</b></summary>

Split Out must point to the array path, `output.items`.

</details>

## 🚀 Level up

- Email the owner of each high-impact risk.
- Run it over every transcript file dropped in a Drive folder.

---

<p align="center"><a href="../L11-ai-news-digest-llm-chain/README.md">← L11 · AI news briefing</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L13-rag-policy-chatbot/README.md">L13 · HR policy chatbot →</a></p>
