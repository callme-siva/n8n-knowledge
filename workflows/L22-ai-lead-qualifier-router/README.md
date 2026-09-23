<div align="center">

# L22 · AI lead qualifier & router (capstone)

![level: Multi-agent & production](https://img.shields.io/badge/level-Multi--agent_%26_production-DC2626?style=flat-square) ![domain: Sales](https://img.shields.io/badge/domain-Sales-334155?style=flat-square) ![build time: 40 min](https://img.shields.io/badge/build_time-40_min-0EA5E9?style=flat-square) ![nodes: 10](https://img.shields.io/badge/nodes-10-7C3AED?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** Sales teams waste hours on tyre-kickers while hot leads go cold. This capstone scores every enquiry with AI (BANT), logs it to a CRM sheet, alerts sales straight away for hot leads, sends a personalised reply, and sends cold leads a nurture email.

## 🎯 What you'll learn

- Combines **everything**: form, structured AI output, Set, Sheets, Switch routing, multiple Gmail branches
- AI as a *decision-maker* with explicit, auditable reasons
- Temperature 0 for consistent scoring
- Designing the fallback path (cold leads still get a reply)

## 🏗️ Architecture

```mermaid
flowchart TB
  n0(["Enquiry Form"]):::trigger
  n1[["Qualify Lead"]]:::ai
  n2("Gemini"):::sub
  n3("Lead Schema"):::sub
  n4["Build CRM Row"]:::code
  n5["Save to CRM Sheet"]:::data
  n6{"Route by Tier"}:::logic
  n7["🔥 Alert Sales Now"]:::msg
  n8["Personal Reply (Hot/Warm)"]:::msg
  n9["Nurture Email (Cold)"]:::msg
  n0 --> n1
  n1 --> n4
  n4 --> n5
  n5 --> n6
  n6 -->|Hot| n7
  n6 -->|Warm| n8
  n6 -->|Cold| n9
  n7 --> n8
  n2 -.->|languageModel| n1
  n3 -.->|outputParser| n1
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
Form → LLM Chain ⇐ Gemini, ⇐ Schema → Set CRM row → Sheets → Switch
   ├ Hot  → Alert sales → Personal reply
   ├ Warm → Personal reply
   └ Cold → Nurture email
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Google Gemini API key | [docs/credentials.md](../../docs/credentials.md) |
| Google Sheets OAuth2 (tab `Leads` | time, name, email, company, score, tier, reason, use_case, reply) |
| Gmail OAuth2 | [docs/credentials.md](../../docs/credentials.md) |

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Build it yourself using L07 + L12 + L04 as references. That is the capstone test.
2. If you get stuck, import `workflow.json` and compare node by node.
3. Set the workflow's *Error workflow* to L19.

## ✅ Test it

- [ ] Submit the 3 sample leads in [docs/sample-data.md](../../docs/sample-data.md#sales-leads): one each should come out hot, warm and cold.

## 🧯 Troubleshooting

<details><summary><b>Every lead is 'warm'</b></summary>

Make the rubric stricter and give examples in the system prompt.

</details>

<details><summary><b>A replied lead gets 2 emails</b></summary>

Hot goes through alert → reply once. Check you didn't also wire Hot directly to *Personal Reply*.

</details>

## 🚀 Level up

- Replace the Sheet with HubSpot / Zoho CRM nodes.
- Add an approval step (L15) before the AI reply goes out.
- Enrich with company data via an API before scoring.

---

<p align="center"><a href="../L21-website-uptime-monitor/README.md">← L21 · Website & API uptime monitor</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; 🏁 You finished the path!</p>
