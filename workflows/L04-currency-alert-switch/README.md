<div align="center">

# L04 · Currency rate alert

![level: Beginner](https://img.shields.io/badge/level-Beginner-2EA44F?style=flat-square) ![domain: Finance / personal](https://img.shields.io/badge/domain-Finance_/_personal-334155?style=flat-square) ![build time: 20 min](https://img.shields.io/badge/build_time-20_min-0EA5E9?style=flat-square) ![nodes: 10](https://img.shields.io/badge/nodes-10-7C3AED?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** If you send money abroad, pay overseas freelancers or invoice in USD, the exchange rate matters. You don't want to check it by hand, and you don't want an email every hour either. You want one only when the rate crosses a threshold.

## 🎯 What you'll learn

- **IF** node: validate an API response before trusting it
- **Switch** node with named outputs plus a fallback
- Comparing numbers against Config values
- **Stop and Error**: fail loudly so your error workflow (L19) catches it
- Dynamic URLs: `https://…/latest/{{ $json.base }}`

## 🏗️ Architecture

```mermaid
flowchart TB
  n0(["Every Hour"]):::trigger
  n1["⚙️ Config"]:::code
  n2["Get Exchange Rate"]:::http
  n3{"API OK?"}:::logic
  n4["Extract Rate"]:::code
  n5{"Which Zone?"}:::logic
  n6["Alert: Rate High"]:::msg
  n7["Alert: Rate Low"]:::msg
  n8["Normal — do nothing"]:::logic
  n9["API Failed — log it"]:::logic
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 -->|true| n4
  n3 -->|false| n9
  n4 --> n5
  n5 -->|High| n6
  n5 -->|Low| n7
  n5 -->|Normal| n8
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
Schedule (hourly) → Config → HTTP → IF ok?
   ├─ true → Extract Rate → Switch ─ High → Gmail
   │                               ├ Low  → Gmail
   │                               └ Normal → (nothing)
   └─ false → Stop and Error
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Gmail OAuth2 (open.er-api.com needs no key) | [docs/credentials.md](../../docs/credentials.md) |

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Schedule Trigger → *Hours*, every 1.
2. Config: base, target, high, low, email_to.
3. HTTP GET `https://open.er-api.com/v6/latest/{{ $json.base }}`.
4. **IF**: `{{ $json.result }}` *is equal to* `success`.
5. On true, add a **Set** node that extracts `rate = {{ $json.rates[$('⚙️ Config').item.json.target] }}` as a *Number*.
6. Add a **Switch** in *Rules* mode. Rule 1: rate ≥ high, rename the output to `High`. Rule 2: rate ≤ low, `Low`. Options → *Fallback output* → Extra output, named `Normal`.
7. Connect a Gmail node to High and to Low, and a **No Operation** to Normal.
8. On IF false, add **Stop and Error**.

## ✅ Test it

- [ ] Set `high` to 1 and run it. You should get the HIGH email.
- [ ] Set `base` to `XYZ` and run it. You should hit the Stop and Error branch.

## 🧯 Troubleshooting

<details><summary><b>Switch always goes to Normal</b></summary>

The rate was saved as a string. Set its type to *Number* in the Set node.

</details>

<details><summary><b>Too many emails</b></summary>

Add a cooldown: store the last alert time with `$getWorkflowStaticData` (see L21).

</details>

## 🚀 Level up

- Track 3 currencies at once (Config returns 3 items).
- Log every reading to Google Sheets and chart it.

---

<p align="center"><a href="../L03-job-search-api/README.md">← L03 · Daily job search digest</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L05-rss-news-code-node/README.md">L05 · Tech news digest →</a></p>
