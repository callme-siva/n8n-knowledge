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

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Create a new workflow and name it `L01 · Hello n8n`.
2. Add a **Manual Trigger** node.
3. Add an **Edit Fields (Set)** node with three fields: `name` (string), `city` (string), `tasks_done` (number).
4. Add a **Code** node and paste the code from `workflow.json`. Look at how it spreads `...item.json` to keep the old fields.
5. Add a **Gmail → Send message** node. In *To*, put your own email. In *Message*, drag `greeting` from the INPUT panel.
6. Click **Execute workflow**.

## ✅ Test it

- [ ] Click each node and open the **OUTPUT** tab: Table, JSON and Schema views show the same data in different shapes.
- [ ] Change `tasks_done` to 10 and run again.

## 🧯 Troubleshooting

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
