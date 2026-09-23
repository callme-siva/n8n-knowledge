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

## 📝 Before you run it

Replace these placeholder values with your own:

| Node | Field | Placeholder |
|---|---|---|
| Email Briefing | `sendTo` | `you@example.com` |

Nodes that need a credential selected after import: **Gmail**, **Google Gemini Chat Model**.

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Start from your finished **L05** (duplicate it).
2. Get a Gemini API key from AI Studio. In n8n, create a *Google Gemini(PaLM) Api* credential (host is the default).
3. Between Code and Gmail, add **Basic LLM Chain**. Prompt = *Define below*, and put `{{ $json.listText }}` in the prompt.
4. Click **+ Chat Model** under the chain and choose **Google Gemini Chat Model** → `gemini-2.5-flash`.
5. Add a *System* message (Chat Messages → System) with the editor rules.
6. Gmail body = `{{ $json.text }}`.

## 🔍 Node-by-node reference

Every node in this workflow and every setting inside it, generated from [`workflow.json`](workflow.json). Click a node to expand it.

<details><summary><b>1. Every Morning 8 AM</b> · <code>Schedule Trigger</code> v1.2</summary>

> Starts the workflow on a timer or cron expression. Only fires when the workflow is **active**.

| Property | Value |
|---|---|
| `rule.interval.triggerAtHour` | 8 |

</details>

<details><summary><b>2. Merge Feeds</b> · <code>Merge</code> v3</summary>

> Waits for several inputs and combines them into one stream.

| Property | Value |
|---|---|
| `numberInputs` | 3 |

</details>

<details><summary><b>3. Google News · AI</b> · <code>RSS Read</code> v1.1</summary>

> Reads an RSS/Atom feed; outputs one item per article.

| Property | Value |
|---|---|
| `url` | https://news.google.com/rss/search?q=artificial+intelligence+when:1d&hl=en-IN&gl=IN&cei… |
| `⚙️ On error` | Continue (regular output) |

</details>

<details><summary><b>4. TechCrunch · AI</b> · <code>RSS Read</code> v1.1</summary>

> Reads an RSS/Atom feed; outputs one item per article.

| Property | Value |
|---|---|
| `url` | https://techcrunch.com/category/artificial-intelligence/feed/ |
| `⚙️ On error` | Continue (regular output) |

</details>

<details><summary><b>5. The Verge · AI</b> · <code>RSS Read</code> v1.1</summary>

> Reads an RSS/Atom feed; outputs one item per article.

| Property | Value |
|---|---|
| `url` | https://www.theverge.com/rss/ai-artificial-intelligence/index.xml |
| `⚙️ On error` | Continue (regular output) |

</details>

<details><summary><b>6. Filter · Dedupe · Sort</b> · <code>Code</code> v2</summary>

> Runs JavaScript. *Run once for all items* sees every item; *for each item* sees one at a time.

| Property | Value |
|---|---|
| `jsCode` | (JavaScript, 13 lines. See workflow.json) |

</details>

<details><summary><b>7. Write Briefing</b> · <code>Basic LLM Chain</code> v1.5</summary>

> Sends one prompt to a model and returns the answer. Simplest AI node.

| Property | Value |
|---|---|
| `promptType` | define |
| `text` | `Here are today's AI news headlines ({{ $json.count }} items):  {{ $json.listText }}` |
| `messages.message` | You are a news editor writing for busy professionals in India. From the headlines, write: 1. **Top 5 stories**: one bullet each, max 2 sentences: what happened + why it matters. Include the link. 2. **One-line trend of the day.** Rules: merge duplicates, skip clickbait, never invent facts beyond the headline. Output clean HTML (&lt;h3&gt;, &lt;ul&gt;, &lt;li&gt;, &lt;a&gt;), no markdown. |

</details>

<details><summary><b>8. Gemini</b> · <code>Google Gemini Chat Model</code> v1</summary>

> The language model plugged into a chain or agent.

| Property | Value |
|---|---|
| `modelName` | models/gemini-2.5-flash |
| `temperature` | 0.3 |

</details>

<details><summary><b>9. Email Briefing</b> · <code>Gmail</code> v2.1</summary>

> Sends, reads or labels email. `sendAndWait` pauses the workflow for a human reply.

| Property | Value |
|---|---|
| `sendTo` | you@example.com |
| `subject` | `☕ AI briefing · {{ $now.toFormat('dd LLL yyyy') }}` |
| `emailType` | html |
| `message` | `{{ $json.text }}<hr><details><summary>All {{ $('Filter · Dedupe · Sort').item.json.count }} headlines</summary>{{ $('Filter · Dedupe · Sort').item.json.html }}</details>` |
| `appendAttribution` | off |

</details>

> [!TIP]
> ⚙️ rows come from each node's **Settings** tab, not its Parameters tab. `{{ … }}` values are **expressions** evaluated at run time. See [workflow anatomy](../../docs/workflow-anatomy.md) for what every property means.

## ✅ Test it

- [ ] Run it and compare the briefing to the raw headlines. Did the model invent anything?
- [ ] Change the system prompt to *Explain like I'm a school student* and run it again.

## 🧯 Troubleshooting

Problems specific to this workflow are below. For general ones (expressions, items, triggers, AI), see [common mistakes](../../docs/common-mistakes.md).

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
