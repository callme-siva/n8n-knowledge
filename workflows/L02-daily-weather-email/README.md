<div align="center">

# L02 · Daily weather email

![level: Beginner](https://img.shields.io/badge/level-Beginner-2EA44F?style=flat-square) ![domain: Personal productivity](https://img.shields.io/badge/domain-Personal_productivity-334155?style=flat-square) ![build time: 15 min](https://img.shields.io/badge/build_time-15_min-0EA5E9?style=flat-square) ![nodes: 4](https://img.shields.io/badge/nodes-4-7C3AED?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** You want a short weather summary in your inbox every morning, before you leave home. This is the "hello world" of scheduled automation, and it calls a real public API.

## 🎯 What you'll learn

- Schedule Trigger and activating workflows
- A **Config node** pattern: keep every setting in one place
- HTTP Request with query parameters
- Referencing an earlier node: `$('⚙️ Config').item.json.city`
- Retry on fail (node Settings tab)
- Inline JavaScript in expressions (`? :` ternary)

## 🏗️ Architecture

```mermaid
flowchart LR
  n0(["Every Morning 7 AM"]):::trigger
  n1["⚙️ Config"]:::code
  n2["Fetch Weather"]:::http
  n3["Email Summary"]:::msg
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
Schedule (7 AM) → ⚙️ Config → HTTP GET open-meteo.com → Gmail
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Gmail OAuth2 | [docs/credentials.md](../../docs/credentials.md) |

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Add a **Schedule Trigger** → *Days*, hour 7.
2. Add a **Set** node named `⚙️ Config` with city, latitude, longitude, timezone and email_to. Get the coordinates from Google Maps (right-click → copy coordinates).
3. Add an **HTTP Request** node: GET `https://api.open-meteo.com/v1/forecast`, turn on *Send Query Parameters* and map them from Config.
4. In the HTTP node **Settings** tab, turn on *Retry On Fail* (3 tries, 5000 ms). Public APIs fail sometimes.
5. Add **Gmail**. Build the HTML body by dragging fields from the INPUT panel.
6. Run it once manually, then **Activate** it.

## ✅ Test it

- [ ] Click *Execute workflow*. A schedule workflow can always be run manually for testing.
- [ ] Check **Executions** (left sidebar) the next morning to see the automatic run.

## 🧯 Troubleshooting

<details><summary><b>Workflow never runs automatically</b></summary>

It isn't **Active**, or your n8n instance was asleep (for example a laptop that was closed). Use n8n Cloud or a VPS for 24/7.

</details>

<details><summary><b>Wrong hour</b></summary>

Set the timezone in *Workflow settings → Timezone*.

</details>

## 🚀 Level up

- Add an **IF** node: send only if the rain chance is above 50% (this previews L04).
- Loop over 3 cities by making Config return 3 items.

---

<p align="center"><a href="../L01-hello-n8n/README.md">← L01 · Hello n8n — your first workflow</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L03-job-search-api/README.md">L03 · Daily job search digest →</a></p>
