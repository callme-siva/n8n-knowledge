<div align="center">

# L19 · Global error handler

![level: Multi-agent & production](https://img.shields.io/badge/level-Multi--agent_%26_production-DC2626?style=flat-square) ![domain: Operations / reliability](https://img.shields.io/badge/domain-Operations_/_reliability-334155?style=flat-square) ![build time: 20 min](https://img.shields.io/badge/build_time-20_min-0EA5E9?style=flat-square) ![nodes: 4](https://img.shields.io/badge/nodes-4-7C3AED?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** Automation that fails silently is worse than none, because you think the reports are going out when they aren't. One error workflow can watch *all* your workflows, email you with a plain-English hint, and keep a log you can review every week.

## 🎯 What you'll learn

- **Error Trigger** and the *Error workflow* setting
- Error payload: `execution.error.message`, `lastNodeExecuted`, `execution.url`
- Pattern-matching errors into actionable hints
- Node-level *On Error: continue* so the alerting itself never crashes
- The full reliability toolkit: Retry on Fail · Continue on Error · Stop and Error · Error workflow

## 🏗️ Architecture

```mermaid
flowchart LR
  n0(["On Any Workflow Error"]):::trigger
  n1["Shape Error"]:::code
  n2["Email Alert"]:::msg
  n3["Log to Error Sheet"]:::data
  n0 --> n1
  n1 --> n2
  n1 --> n3
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
Error Trigger → Code (shape + hint) ─┬→ Gmail alert
                                    └→ Sheets log
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Gmail OAuth2 | [docs/credentials.md](../../docs/credentials.md) |
| Google Sheets OAuth2 (tab `Errors` | time, workflow, workflow_id, node, message, hint, url, mode) |

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Add **Error Trigger** (this workflow never needs to be *active*).
2. Add the Code node to shape the error and generate a hint.
3. Add Gmail and Sheets in parallel, each with *On Error → Continue*.
4. Open **every** other workflow → *Settings* → **Error workflow** → choose this one.

## ✅ Test it

- [ ] Activate **L04** with `base = XYZ` (or disconnect a credential) and let it run. The alert should arrive within seconds.
- [ ] Note: error workflows fire for **production** executions, not manual test runs.

## 🧯 Troubleshooting

<details><summary><b>No alert when testing manually</b></summary>

That's expected. Only automatic (trigger or production) executions call the error workflow.

</details>

<details><summary><b>Alert loop</b></summary>

Never set L19 as its own error workflow.

</details>

## 🚀 Level up

- Add Slack / Telegram alerts.
- Weekly summary: read the Errors sheet → group by workflow → email the top offenders.

---

<p align="center"><a href="../L18-resume-job-fit-multi-agent/README.md">← L18 · Resume ↔ job fit analyser</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L20-subworkflows-caller/README.md">L20 · Sub-workflows — weekly birthday & anniversary wishes →</a></p>
