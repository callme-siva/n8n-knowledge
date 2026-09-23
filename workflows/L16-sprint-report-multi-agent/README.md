<div align="center">

# L16 · Sprint progress report with 4 cooperating agents

![level: Multi-agent & production](https://img.shields.io/badge/level-Multi--agent_%26_production-DC2626?style=flat-square) ![domain: Agile / engineering management](https://img.shields.io/badge/domain-Agile_/_engineering_management-334155?style=flat-square) ![build time: 45 min](https://img.shields.io/badge/build_time-45_min-0EA5E9?style=flat-square) ![nodes: 14](https://img.shields.io/badge/nodes-14-7C3AED?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** A delivery lead needs one daily email: is the sprint on track, who is overloaded, is the backlog healthy? Each question needs a different lens, so one specialist agent handles each lens and a coordinator writes the final report.

## 🎯 What you'll learn

- GitHub **GraphQL** API via HTTP Request
- Computing metrics in code *before* the LLM sees them (cheaper, and no maths mistakes)
- **Sequential multi-agent** pattern: each agent reads the metrics plus the earlier agents' notes
- A coordinator agent that merges the specialists' output into one report

## 🏗️ Architecture

```mermaid
flowchart TB
  n0["Config"]:::code
  n1["Build GraphQL Request"]:::code
  n2["Fetch GitHub Project"]:::http
  n3["Compute Sprint Metrics"]:::code
  n4[["Capacity Planning Agent"]]:::ai
  n5("Capacity Model"):::sub
  n6[["Backlog Health Agent"]]:::ai
  n7("Backlog Model"):::sub
  n8[["Burndown Tracking Agent"]]:::ai
  n9("Burndown Model"):::sub
  n10[["Coordinator Agent"]]:::ai
  n11("Coordinator Model"):::sub
  n12["Email Daily Report"]:::msg
  n13(["Weekdays 9 AM"]):::trigger
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  n4 --> n6
  n5 -.->|languageModel| n4
  n6 --> n8
  n7 -.->|languageModel| n6
  n8 --> n10
  n9 -.->|languageModel| n8
  n10 --> n12
  n11 -.->|languageModel| n10
  n13 --> n0
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
Schedule → Config → Code (GraphQL query) → HTTP POST api.github.com/graphql → Code (metrics)
 → Capacity agent → Backlog agent → Burndown agent → Coordinator agent → Gmail
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| GitHub API token (classic PAT with `read:project`, `repo`) | [docs/credentials.md](../../docs/credentials.md) |
| Google Gemini API key | [docs/credentials.md](../../docs/credentials.md) |
| Gmail OAuth2 | [docs/credentials.md](../../docs/credentials.md) |

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Create a GitHub Project (v2) with Status, Estimate and Iteration fields, and add some issues.
2. Create a GitHub credential with a PAT.
3. Config: `org` (your user/org URL), `projectNumber`, recipient email.
4. Import this workflow and run it up to *Compute Sprint Metrics*. Read the metrics JSON before any AI step runs.
5. Run the full chain and read each agent's output in order.

## ✅ Test it

- [ ] Change a few issue statuses in GitHub, run it again, and compare the burndown text.

## 🧯 Troubleshooting

<details><summary><b>GraphQL Could not resolve to a ProjectV2</b></summary>

Wrong project number, or it's a user project and the query expects an org. The code handles both, so check `org`.

</details>

<details><summary><b>The report contradicts the metrics</b></summary>

Lower the temperature, and tell agents to quote the numbers from the JSON.

</details>

## 🚀 Level up

- Swap GitHub for Jira (Jira node, sprint JQL).
- Run the three specialist agents in **parallel** and merge them, which is faster.

---

<p align="center"><a href="../L15-retro-ai-approval-jira/README.md">← L15 · Retrospective → AI action items → human approval → Jira</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L17-complaint-handler-multi-agent/README.md">L17 · Customer complaint handler →</a></p>
