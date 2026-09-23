<div align="center">

# L01 · Hello n8n — your first workflow

![level: Beginner](https://img.shields.io/badge/level-Beginner-2EA44F?style=flat-square) ![domain: General](https://img.shields.io/badge/domain-General-334155?style=flat-square) ![build time: 10 min](https://img.shields.io/badge/build_time-10_min-0EA5E9?style=flat-square) ![nodes: 4](https://img.shields.io/badge/nodes-4-7C3AED?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** Everyone starts here. Before automating anything real, you need to understand how data moves between nodes. This workflow takes some values, builds a message and emails it to you.

## 🎯 What you'll learn

- Manual Trigger: run a workflow on demand
- Set node: create data without code
- Code node: transform items with JavaScript
- Expressions: `{{ $json.field }}`
- Reading the INPUT and OUTPUT panels

## 🏗️ Architecture

```mermaid
flowchart LR
  n0(["When clicking 'Execute workflow'"]):::trigger
  n1["Set Your Data"]:::code
  n2["Build Greeting"]:::code
  n3["Send to Yourself"]:::msg
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
Manual Trigger → Set Your Data → Build Greeting (Code) → Send to Yourself (Gmail)
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Gmail OAuth2 — see [docs/credentials.md](../../docs/credentials.md#gmail). *Optional* | delete the Gmail node and the workflow still teaches everything. |

## 📝 Before you run it

Replace these placeholder values with your own:

| Node | Field | Placeholder |
|---|---|---|
| Send to Yourself | `sendTo` | `you@example.com` |

Nodes that need a credential selected after import: **Gmail**.

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Create a new workflow and name it `L01 · Hello n8n`.
2. Add a **Manual Trigger** node.
3. Add an **Edit Fields (Set)** node with three fields: `name` (string), `city` (string), `tasks_done` (number).
4. Add a **Code** node and paste the code from `workflow.json`. Look at how it spreads `...item.json` to keep the old fields.
5. Add a **Gmail → Send message** node. In *To*, put your own email. In *Message*, drag `greeting` from the INPUT panel.
6. Click **Execute workflow**.

## 🔍 Node-by-node reference

Every node in this workflow and every setting inside it, generated from [`workflow.json`](workflow.json). Click a node to expand it.

<details><summary><b>1. When clicking 'Execute workflow'</b> · <code>Manual Trigger</code> v1</summary>

> Starts the workflow when you click *Execute workflow*. For testing only.

*No settings. This node works with its defaults.*

</details>

<details><summary><b>2. Set Your Data</b> · <code>Edit Fields (Set)</code> v3.4</summary>

> Creates, renames or overwrites fields without code.

| Property | Value |
|---|---|
| `name` | Learner |
| `city` | Chennai |
| `tasks_done` | 3 |

</details>

<details><summary><b>3. Build Greeting</b> · <code>Code</code> v2</summary>

> Runs JavaScript. *Run once for all items* sees every item; *for each item* sees one at a time.

| Property | Value |
|---|---|
| `jsCode` | (JavaScript, 8 lines. See workflow.json) |

</details>

<details><summary><b>4. Send to Yourself</b> · <code>Gmail</code> v2.1</summary>

> Sends, reads or labels email. `sendAndWait` pauses the workflow for a human reply.

| Property | Value |
|---|---|
| `sendTo` | you@example.com |
| `subject` | My first n8n workflow 🎉 |
| `emailType` | html |
| `message` | `<p>{{ $json.greeting }}</p><p><small>Sent at {{ $json.generated_at }}</small></p>` |
| `appendAttribution` | off |

</details>

> [!TIP]
> ⚙️ rows come from each node's **Settings** tab, not its Parameters tab. `{{ … }}` values are **expressions** evaluated at run time. See [workflow anatomy](../../docs/workflow-anatomy.md) for what every property means.

## ✅ Test it

- [ ] Click each node and open the **OUTPUT** tab: Table, JSON and Schema views show the same data in different shapes.
- [ ] Change `tasks_done` to 10 and run again.

## 🧯 Troubleshooting

Problems specific to this workflow are below. For general ones (expressions, items, triggers, AI), see [common mistakes](../../docs/common-mistakes.md).

<details><summary><b>Credentials not found on Gmail</b></summary>

Open the node → Credential → *Create new* and sign in with Google.

</details>

<details><summary><b>Code node: Cannot read properties of undefined</b></summary>

Check the field name spelling — JSON keys are case-sensitive.

</details>

## 🚀 Level up

- Add a second item in the Set node (turn on *Include Other Input Fields*) or return two items from Code — watch Gmail send two emails.
- Replace Gmail with Telegram or Slack.

---

<p align="center"> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L02-daily-weather-email/README.md">L02 · Daily weather email →</a></p>
