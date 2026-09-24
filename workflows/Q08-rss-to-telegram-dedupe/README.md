<div align="center">

# Q08 · RSS → Telegram channel with dedupe across runs

![level: Quick win](https://img.shields.io/badge/level-Quick_win-0EA5E9?style=flat-square) ![domain: Marketing / community](https://img.shields.io/badge/domain-Marketing_/_community-334155?style=flat-square) ![build time: 15 min](https://img.shields.io/badge/build_time-15_min-0EA5E9?style=flat-square) ![nodes: 7](https://img.shields.io/badge/nodes-7-7C3AED?style=flat-square) [![e2e test: passed · 3 checks](https://img.shields.io/badge/e2e_test-passed_%C2%B7_3_checks-2EA44F?style=flat-square)](https://github.com/callme-siva/n8n-knowledge/actions/workflows/validate.yml)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** Communities and company channels need a steady flow of relevant links, and nobody wants to post them by hand. The hard part is never posting the same link twice, even across restarts. n8n's *Remove Duplicates* node now remembers what it has seen between executions.

## 💡 Concept first

**📌 Key idea:** **Deduplicate across executions** so each item is processed once, ever, even after restarts.

**🧠 Mental model:** A bouncer with a guest list who remembers everyone already let in.

**🚫 When *not* to use it:** Don't dedupe on a field that changes (titles get edited). Use a stable ID or URL.

## 🎯 What you'll learn

- **Remove Duplicates → Remove items seen in previous executions**
- History size and what happens when it fills
- Why **filter before dedupe, never limit after it**: anything dropped after dedupe is marked seen and lost
- Sorting so the channel reads in publish order
- Telegram HTML formatting

## 🏗️ Architecture

**System context:** who and what this workflow talks to, and what crosses each boundary. 🔑 = needs a credential · 🧑 = a human decides.

```mermaid
flowchart LR
  s0(["⏰ Schedule"]):::time
  core{{"⚙️ n8n workflow<br/><small>7 nodes</small>"}}:::n8n
  state[("🗄️ memory<br/>between runs")]:::store
  core -.- state
  s1["🌐 URLs from data"]:::ext
  s2["✈️ Telegram 🔑"]:::saas
  s0 -->|"fires"| core
  core <-->|"reads feed"| s1
  core -->|"sends messages"| s2
  classDef time fill:#E8F7EE,stroke:#2EA44F,color:#1F2937
  classDef saas fill:#EAF3FF,stroke:#2563EB,color:#1F2937
  classDef ext fill:#E6FAF8,stroke:#0D9488,color:#1F2937
  classDef n8n fill:#FFF1F4,stroke:#EA4B71,stroke-width:3px,color:#1F2937
  classDef store fill:#F8FAFC,stroke:#64748B,color:#1F2937
```

<details><summary><b>Node-level flow</b> (every node and branch)</summary>

```mermaid
flowchart TB
  n0(["Every 30 Minutes"]):::trigger
  n1["⚙️ Config"]:::code
  n2["Read Feed"]:::http
  n3{"Recent Only"}:::logic
  n4["Oldest First"]:::logic
  n5["Only New Links"]:::logic
  n6["Post to Channel"]:::msg
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  n4 --> n5
  n5 --> n6
  classDef trigger fill:#E8F7EE,stroke:#2EA44F,stroke-width:2px,color:#1F2937
  classDef logic fill:#FFF4E5,stroke:#F59E0B,stroke-width:2px,color:#1F2937
  classDef code fill:#EEF2F7,stroke:#64748B,stroke-width:2px,color:#1F2937
  classDef http fill:#E6FAF8,stroke:#0D9488,stroke-width:2px,color:#1F2937
  classDef msg fill:#FFEDEF,stroke:#E11D48,stroke-width:2px,color:#1F2937
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Telegram bot token (add the bot as an **admin** of your channel) | [docs/credentials.md](../../docs/credentials.md) |

## 📝 Before you run it

No placeholder values. It runs as-is.

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Create a channel and add your bot as admin with *Post messages*.
2. Set the feed URL, channel and `max_age_days` in **⚙️ Config**.
3. **Filter** `isoDate` is after `{{ $now.minus({ days: 3 }) }}`, then **Sort** by `isoDate` (ascending). This stops the first run flooding the channel with the whole feed.
4. **Remove Duplicates** → operation *Remove items processed in previous executions*, value `{{ $json.link }}`.
5. Telegram *Send message* to `{{ $('⚙️ Config').first().json.channel }}`, parse mode HTML.

## 🔍 Node-by-node reference

Every node in this workflow and every setting inside it, generated from [`workflow.json`](workflow.json). Click a node to expand it.

<details><summary><b>1. Every 30 Minutes</b> · <code>Schedule Trigger</code> v1.2</summary>

> Starts the workflow on a timer or cron expression. Only fires when the workflow is **active**.

| Property | Value |
|---|---|
| `rule.interval.field` | minutes |
| `rule.interval.minutesInterval` | 30 |

</details>

<details><summary><b>2. ⚙️ Config</b> · <code>Edit Fields (Set)</code> v3.4</summary>

> Creates, renames or overwrites fields without code.

| Property | Value |
|---|---|
| `feed_url` | https://blog.n8n.io/rss/ |
| `channel` | @your_channel_name |
| `max_age_days` | 3 |

</details>

<details><summary><b>3. Read Feed</b> · <code>RSS Read</code> v1.1</summary>

> Reads an RSS/Atom feed; outputs one item per article.

| Property | Value |
|---|---|
| `url` | `{{ $json.feed_url }}` |
| `⚙️ On error` | Continue (regular output) |

</details>

<details><summary><b>4. Recent Only</b> · <code>Filter</code> v2.2</summary>

> Keeps only items that match; drops the rest.

| Property | Value |
|---|---|
| `condition` | `{{ $json.isoDate }} after {{ $now.minus({ days: $('⚙️ Config').first().json.max_age_day…` |

</details>

<details><summary><b>5. Oldest First</b> · <code>sort</code> v1</summary>



| Property | Value |
|---|---|
| `sortFieldsUi.sortField.fieldName` | isoDate |

</details>

<details><summary><b>6. Only New Links</b> · <code>removeDuplicates</code> v2</summary>



| Property | Value |
|---|---|
| `operation` | removeItemsSeenInPreviousExecutions |
| `dedupeValue` | `{{ $json.link }}` |
| `historySize` | 5000 |

</details>

<details><summary><b>7. Post to Channel</b> · <code>telegram</code> v1.2</summary>



| Property | Value |
|---|---|
| `chatId` | `{{ $('⚙️ Config').first().json.channel }}` |
| `text` | `📰 <b>{{ $json.title }}</b> {{ ($json.contentSnippet \|\| '').slice(0, 200) }}… {{ $json.link }}` |
| `additionalFields.parse_mode` | HTML |
| `additionalFields.appendAttribution` | off |
| `⚙️ Retry on fail` | ✅ on |
| `⚙️ Max tries` | 3 |
| `⚙️ Wait between tries (ms)` | 3000 |

</details>

> [!TIP]
> ⚙️ rows come from each node's **Settings** tab, not its Parameters tab. `{{ … }}` values are **expressions** evaluated at run time. See [workflow anatomy](../../docs/workflow-anatomy.md) for what every property means.

## ✅ Test it

> [!TIP]
> **Automated end-to-end test: passed.** 7/7 nodes executed in real n8n (2 credentialed or AI nodes replaced by fixtures, so AI output itself isn't tested), 3 behaviour checks. See [tests/](../../tests/README.md).

- [ ] Run twice. The second run should post nothing.
- [ ] The first run posts only articles from the last 3 days, oldest first.
- [ ] **Activate** it. Like static data, dedupe history only builds up in real (active) runs you keep.

## 🧯 Troubleshooting

Problems specific to this workflow are below. For general ones (expressions, items, triggers, AI), see [common mistakes](../../docs/common-mistakes.md).

<details><summary><b>chat not found</b></summary>

Use `@channelusername` for public channels, or the numeric `-100…` ID for private ones. The bot must be an admin.

</details>

<details><summary><b>Posts everything again after editing</b></summary>

Dedupe history is per node. Deleting or recreating the node resets it.

</details>

<details><summary><b>A post failed and never came back</b></summary>

The link was already marked seen. *Post to Channel* retries 3 times; if Telegram is down longer, repost by hand.

</details>

## 🏋️ Practice

Try each challenge **before** opening the hint. Solutions show the exact expressions and code.

**⭐ Challenge 1:** Post only articles matching **keywords** (e.g. "AI", "automation").

<details><summary>💡 Hint</summary>

Filter before dedupe, so skipped items aren't remembered.

</details>
<details><summary>✅ Solution</summary>

Add a **Filter**: `{{ /\b(ai|automation|n8n)\b/i.test($json.title) }}` is true, placed before *Only New Links*.

</details>

**⭐⭐ Challenge 2:** Add an AI-written one-line hook per article.

<details><summary>💡 Hint</summary>

LLM chain per item, after the Limit (so you pay for max 5).

</details>
<details><summary>✅ Solution</summary>

After *Max 5 per Run*, add a Basic LLM Chain + Gemini: *"Write one catchy line (max 15 words) about: {{ $json.title }}"*. Use `{{ $json.text }}` in the Telegram message.

</details>

## 🚀 Ideas to extend it

- Add AI to write a one-line hook per article.
- Merge several feeds (see L05).

---

<p align="center"><a href="../Q07-gmail-ai-auto-labeler/README.md">← Q07 · Gmail AI auto-labeler</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; 🏁 End of Quick wins</p>
