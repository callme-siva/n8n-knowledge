<div align="center">

# L17 · Customer complaint handler (5 agents)

![level: Multi-agent & production](https://img.shields.io/badge/level-Multi--agent_%26_production-DC2626?style=flat-square) ![domain: Customer support](https://img.shields.io/badge/domain-Customer_support-334155?style=flat-square) ![build time: 45 min](https://img.shields.io/badge/build_time-45_min-0EA5E9?style=flat-square) ![nodes: 20](https://img.shields.io/badge/nodes-20-7C3AED?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** Support teams spend the first 10 minutes of every complaint just working out what it is. This pipeline classifies it (category, urgency, sentiment), investigates, proposes a resolution and a goodwill gesture, decides whether to escalate, and drafts an empathetic reply.

## 🎯 What you'll learn

- Chained agents, each with its **own schema**
- **Auto-fixing output parser** (a second model repairs malformed JSON)
- Referencing any earlier step: `$('Understand Complaint').item.json.output`
- Designing escalation rules as explicit JSON (`escalate`, `priority`, `route_to`)

## 🏗️ Architecture

```mermaid
flowchart TB
  n0(["Complaint Form"]):::trigger
  n1[["Understand Complaint"]]:::ai
  n2("Understand Model"):::sub
  n3("Understanding Schema"):::sub
  n4("Understanding Fix Model"):::sub
  n5[["Investigate Customer/Order"]]:::ai
  n6("Investigate Model"):::sub
  n7("Investigation Schema"):::sub
  n8("Investigation Fix Model"):::sub
  n9[["Determine Resolution"]]:::ai
  n10("Resolution Model"):::sub
  n11("Resolution Schema"):::sub
  n12("Resolution Fix Model"):::sub
  n13[["Check Escalation"]]:::ai
  n14("Escalation Model"):::sub
  n15("Escalation Schema"):::sub
  n16("Escalation Fix Model"):::sub
  n17[["Draft Response"]]:::ai
  n18("Draft Model"):::sub
  n19["Send Response Email"]:::msg
  n0 --> n1
  n1 --> n5
  n2 -.->|languageModel| n1
  n3 -.->|outputParser| n1
  n4 -.->|languageModel| n3
  n5 --> n9
  n6 -.->|languageModel| n5
  n7 -.->|outputParser| n5
  n8 -.->|languageModel| n7
  n9 --> n13
  n10 -.->|languageModel| n9
  n11 -.->|outputParser| n9
  n12 -.->|languageModel| n11
  n13 --> n17
  n14 -.->|languageModel| n13
  n15 -.->|outputParser| n13
  n16 -.->|languageModel| n15
  n17 --> n19
  n18 -.->|languageModel| n17
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
Form → Understand ⇐(model, schema⇐fix model) → Investigate ⇐… → Resolve ⇐… → Escalate? ⇐… → Draft reply ⇐model → Gmail
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Google Gemini API key | [docs/credentials.md](../../docs/credentials.md) |
| Gmail OAuth2 | [docs/credentials.md](../../docs/credentials.md) |

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Import it and connect the Gemini credential. There are 10 model nodes: select them all and set the credential once.
2. Open the form and submit a complaint from [docs/sample-data.md](../../docs/sample-data.md#customer-complaints).
3. Click each agent in the execution and read its `output`. Look at how context builds up.
4. Change the email node to send to **yourself** while testing.

## ✅ Test it

- [ ] Try an angry high-value complaint (it should escalate) and a mild one (it shouldn't).

## 🧯 Troubleshooting

<details><summary><b>Could not parse LLM output</b></summary>

The fix model is supposed to catch this. Check that each *Fix Model* is connected to its parser.

</details>

<details><summary><b>It emails real customers during testing</b></summary>

Put your own email in *Send Response Email* until you're ready.

</details>

## 🚀 Level up

- Add a real order lookup tool (Google Sheets or your DB) to the Investigate agent.
- Route escalations to a Slack channel and a Jira Service Management ticket.
- Insert an approval step (L15) before *Send Response Email*.

---

<p align="center"><a href="../L16-sprint-report-multi-agent/README.md">← L16 · Sprint progress report</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L18-resume-job-fit-multi-agent/README.md">L18 · Resume ↔ job fit analyser →</a></p>
