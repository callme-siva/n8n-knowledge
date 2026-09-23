<div align="center">

# L05 · Tech news digest with the Code node

![level: Beginner](https://img.shields.io/badge/level-Beginner-2EA44F?style=flat-square) ![domain: Learning / research](https://img.shields.io/badge/domain-Learning_/_research-334155?style=flat-square) ![build time: 25 min](https://img.shields.io/badge/build_time-25_min-0EA5E9?style=flat-square) ![nodes: 8](https://img.shields.io/badge/nodes-8-7C3AED?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** You follow 3 news sites and see the same story three times. This merges the feeds, removes duplicates and sends one clean list.

## 🎯 What you'll learn

- RSS Read node
- **Merge** node with 3 inputs (append mode)
- Code node: filter / map / sort / dedupe / reduce many items into one
- *On Error → Continue*: one broken feed shouldn't kill the run
- An IF guard so you don't get empty emails

## 🏗️ Architecture

```mermaid
flowchart TB
  n0(["Every Morning 8 AM"]):::trigger
  n1["Merge Feeds"]:::logic
  n2["Google News · AI"]:::http
  n3["TechCrunch · AI"]:::http
  n4["The Verge · AI"]:::http
  n5["Filter · Dedupe · Sort"]:::code
  n6{"Anything New?"}:::logic
  n7["Email Digest"]:::msg
  n0 --> n2
  n0 --> n3
  n0 --> n4
  n2 --> n1
  n3 --> n1
  n4 --> n1
  n1 --> n5
  n5 --> n6
  n6 --> n7
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
Schedule ─┬─ RSS Google News ─┐
          ├─ RSS TechCrunch  ─┼─ Merge → Code (filter/dedupe/sort) → IF count>0 → Gmail
          └─ RSS The Verge   ─┘
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Gmail OAuth2 | [docs/credentials.md](../../docs/credentials.md) |

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Add a Schedule Trigger and 3 **RSS Read** nodes, each connected to the trigger.
2. On each RSS node: Settings → *On Error* → **Continue**.
3. Add **Merge** → *Number of inputs* 3, and wire each feed to its own input.
4. Add a **Code** node (*Run once for all items*) and paste the code. Read it line by line; each `.filter` / `.map` is one idea.
5. Add an **IF** node: `count > 0`.
6. Add Gmail on the true branch.

## ✅ Test it

- [ ] Run it and open the Code node output. `listText` is prepared for the AI version in L11.
- [ ] Replace one feed URL with a broken one. The workflow should still finish.

## 🧯 Troubleshooting

<details><summary><b>Merge waits forever or outputs nothing</b></summary>

Every input must be connected. Check the numbered input dots on Merge.

</details>

<details><summary><b>All articles filtered out</b></summary>

Some feeds use `pubDate` and not `isoDate`. The code handles both, so check your feed's field names.

</details>

## 🚀 Level up

- Add your own feeds (company blog, Hacker News `https://hnrss.org/frontpage`).
- Continue to **L11** to have Gemini summarise this.

---

<p align="center"><a href="../L04-currency-alert-switch/README.md">← L04 · Currency rate alert</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L06-gmail-pdf-to-drive/README.md">L06 · Save Gmail PDF attachments to Google Drive →</a></p>
