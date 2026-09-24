<div align="center">

# P10a · Tool sub-workflow: look up customer

![level: Real-world project](https://img.shields.io/badge/level-Real--world_project-7C3AED?style=flat-square) ![domain: Tool for P10](https://img.shields.io/badge/domain-Tool_for_P10-334155?style=flat-square) ![build time: 10 min](https://img.shields.io/badge/build_time-10_min-0EA5E9?style=flat-square) ![nodes: 3](https://img.shields.io/badge/nodes-3-7C3AED?style=flat-square) [![e2e test: passed · 1 checks](https://img.shields.io/badge/e2e_test-passed_%C2%B7_1_checks-2EA44F?style=flat-square)](https://github.com/callme-siva/n8n-knowledge/actions/workflows/validate.yml)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** Helper used by [P10 · MCP server](../P10-mcp-server-business-tools/README.md). Any sub-workflow can become a tool for an AI agent or an MCP client.

## 🎯 What you'll learn

- Execute Workflow Trigger inputs as tool parameters
- `alwaysOutputData` for "not found" answers

## 🏗️ Architecture

**System context:** who and what this workflow talks to, and what crosses each boundary. 🔑 = needs a credential · 🧑 = a human decides.

```mermaid
flowchart LR
  s0(["↗ Calling workflow"]):::time
  core{{"⚙️ n8n workflow<br/><small>3 nodes</small>"}}:::n8n
  s1["📊 Google Sheets 🔑"]:::saas
  s0 -->|"inputs"| core
  core <-->|"reads rows"| s1
  classDef person fill:#FFF4E5,stroke:#F59E0B,color:#1F2937
  classDef time fill:#E8F7EE,stroke:#2EA44F,color:#1F2937
  classDef saas fill:#EAF3FF,stroke:#2563EB,color:#1F2937
  classDef ai fill:#F1EBFF,stroke:#7C3AED,color:#1F2937
  classDef ext fill:#E6FAF8,stroke:#0D9488,color:#1F2937
  classDef n8n fill:#FFF1F4,stroke:#EA4B71,stroke-width:3px,color:#1F2937
  classDef store fill:#F8FAFC,stroke:#64748B,color:#1F2937
```

<details><summary><b>Node-level flow</b> (every node and branch)</summary>

```mermaid
flowchart LR
  n0(["When Called as Tool"]):::trigger
  n1["Find Customer"]:::data
  n2["Shape Answer"]:::code
  n0 --> n1
  n1 --> n2
  classDef trigger fill:#E8F7EE,stroke:#2EA44F,stroke-width:2px,color:#1F2937
  classDef ai fill:#F1EBFF,stroke:#7C3AED,stroke-width:2px,color:#1F2937
  classDef sub fill:#F7F3FF,stroke:#A78BFA,stroke-width:2px,color:#1F2937
  classDef logic fill:#FFF4E5,stroke:#F59E0B,stroke-width:2px,color:#1F2937
  classDef code fill:#EEF2F7,stroke:#64748B,stroke-width:2px,color:#1F2937
  classDef data fill:#EAF3FF,stroke:#2563EB,stroke-width:2px,color:#1F2937
  classDef http fill:#E6FAF8,stroke:#0D9488,stroke-width:2px,color:#1F2937
  classDef msg fill:#FFEDEF,stroke:#E11D48,stroke-width:2px,color:#1F2937
```

</details>

<details><summary>Plain-text flow</summary>

```
Execute Workflow Trigger (email) → Sheets lookup → Code (found / not found)
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Google Sheets OAuth2 (tab `Customers` | email, name, plan, mrr, status, last_ticket) |

## 📝 Before you run it

Replace these placeholder values with your own:

| Node | Field | Placeholder |
|---|---|---|
| Find Customer | `documentId` | `PASTE_YOUR_GOOGLE_SHEET_URL` |

Nodes that need a credential selected after import: **Google Sheets**.

### 📥 Starter files

Create each tab from its template, so column names match exactly: **Google Sheets → File → Import → Upload** the CSV → *Insert new sheet(s)*. The tab takes the file's name.

| Tab | Template | Columns |
|---|---|---|
| `Customers` | [Customers.csv](../../templates/P10a-tool-lookup-customer/Customers.csv) | `email`, `mrr`, `plan`, `status` |

<sub>Columns are generated from what this workflow actually reads and writes in the automated test, so they can't drift from the workflow.</sub>

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Import and **save** this first. Copy its ID from the URL.
2. Paste the ID into P10's *lookup_customer* tool.

## 🔍 Node-by-node reference

Every node in this workflow and every setting inside it, generated from [`workflow.json`](workflow.json). Click a node to expand it.

<details><summary><b>1. When Called as Tool</b> · <code>Execute Workflow Trigger</code> v1.1</summary>

> Makes this workflow callable from other workflows, like a function.

| Property | Value |
|---|---|
| `workflowInputs.name` | email |

</details>

<details><summary><b>2. Find Customer</b> · <code>Google Sheets</code> v4.5</summary>

> Reads, appends or updates rows in a spreadsheet.

| Property | Value |
|---|---|
| `documentId` | PASTE_YOUR_GOOGLE_SHEET_URL |
| `sheetName` | Customers |
| `filtersUI.lookupColumn` | email |
| `filtersUI.lookupValue` | `{{ $json.email.toLowerCase() }}` |
| `⚙️ Retry on fail` | ✅ on |
| `⚙️ Max tries` | 3 |
| `⚙️ Wait between tries (ms)` | 3000 |
| `⚙️ Always output data` | ✅ on |

</details>

<details><summary><b>3. Shape Answer</b> · <code>Code</code> v2</summary>

> Runs JavaScript. *Run once for all items* sees every item; *for each item* sees one at a time.

| Property | Value |
|---|---|
| `jsCode` | (JavaScript, 2 lines, shown below) |

**Code:**

```javascript
const r = $input.first()?.json || {};
return [{ json: r.email ? { found: true, ...r } : { found: false, message: 'No customer with that email' } }];
```

</details>

> [!TIP]
> ⚙️ rows come from each node's **Settings** tab, not its Parameters tab. `{{ … }}` values are **expressions** evaluated at run time. See [workflow anatomy](../../docs/workflow-anatomy.md) for what every property means.

## ✅ Test it

> [!TIP]
> **Automated end-to-end test: passed.** 3/3 nodes executed in real n8n (2 credentialed or AI nodes replaced by fixtures, so AI output itself isn't tested), 1 behaviour checks. See [tests/](../../tests/README.md).

- [ ] Run P10 and ask an MCP client "what plan is asha@finlytics.example.com on?"

## 🧯 Troubleshooting

Problems specific to this workflow are below. For general ones (expressions, items, triggers, AI), see [common mistakes](../../docs/common-mistakes.md).

<details><summary><b>Always not found</b></summary>

The sheet email column must be lowercase, or lowercase it in a helper column.

</details>

## 🚀 Ideas to extend it

- Add `create_ticket` and `get_invoices` tools the same way.

---

<p align="center"><a href="../P10-mcp-server-business-tools/README.md">← Used by P10 · MCP server</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a></p>
