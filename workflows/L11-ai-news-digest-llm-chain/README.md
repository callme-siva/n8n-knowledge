<div align="center">

# L11 · AI news briefing with a Basic LLM Chain

![level: AI](https://img.shields.io/badge/level-AI-F97316?style=flat-square) ![domain: Learning / research](https://img.shields.io/badge/domain-Learning_/_research-334155?style=flat-square) ![build time: 20 min](https://img.shields.io/badge/build_time-20_min-0EA5E9?style=flat-square) ![nodes: 9](https://img.shields.io/badge/nodes-9-7C3AED?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** 25 headlines is still too many to read. An LLM can turn them into 5 bullets that say *why each story matters*, which is what a good executive briefing does.

## 🎯 What you'll learn

- Basic LLM Chain node: prompt in, text out
- Connecting a **Chat Model sub-node** (Gemini)
- Writing a system prompt with rules and an output format
- Temperature: 0.3 for factual summaries
- Keeping the raw data in the email as a fallback, so the AI never hides the source

## 🏗️ Architecture

```mermaid
flowchart TB
  n0(["Every Morning 8 AM"]):::trigger
  n1["Merge Feeds"]:::logic
  n2["Google News · AI"]:::http
  n3["TechCrunch · AI"]:::http
  n4["The Verge · AI"]:::http
  n5["Filter · Dedupe · Sort"]:::code
  n6[["Write Briefing"]]:::ai
  n7("Gemini"):::sub
  n8["Email Briefing"]:::msg
  n0 --> n2
  n0 --> n3
  n0 --> n4
  n2 --> n1
  n3 --> n1
  n4 --> n1
  n1 --> n5
  n5 --> n6
  n6 --> n8
  n7 -.->|languageModel| n6
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
Schedule → 3× RSS → Merge → Code (from L05) → LLM Chain ⇐ Gemini → Gmail
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Google Gemini (PaLM) API key | free at https://aistudio.google.com/app/apikey |
| Gmail OAuth2 | [docs/credentials.md](../../docs/credentials.md) |

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Start from your finished **L05** (duplicate it).
2. Get a Gemini API key from AI Studio. In n8n, create a *Google Gemini(PaLM) Api* credential (host is the default).
3. Between Code and Gmail, add **Basic LLM Chain**. Prompt = *Define below*, and put `{{ $json.listText }}` in the prompt.
4. Click **+ Chat Model** under the chain and choose **Google Gemini Chat Model** → `gemini-2.5-flash`.
5. Add a *System* message (Chat Messages → System) with the editor rules.
6. Gmail body = `{{ $json.text }}`.

## ✅ Test it

- [ ] Run it and compare the briefing to the raw headlines. Did the model invent anything?
- [ ] Change the system prompt to *Explain like I'm a school student* and run it again.

## 🧯 Troubleshooting

<details><summary><b>429 / quota exceeded</b></summary>

The free tier has per-minute limits. Wait a minute, or use `gemini-2.5-flash-lite`.

</details>

<details><summary><b>Output shows html fences</b></summary>

Add "no code fences" to the prompt, or strip them with `.replace(/```html|```/g,'')`.

</details>

## 🚀 Level up

- Ask for JSON and render your own template (this previews L12).
- Send it to Telegram as a morning message.

---

<p align="center"><a href="../L10-form-bug-report-jira/README.md">← L10 · Bug report form → Jira issue + reporter confirmation</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L12-meeting-transcript-raid-log/README.md">L12 · Meeting transcript → RAID log →</a></p>
