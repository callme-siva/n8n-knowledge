<div align="center">

# L06 · Gmail PDF attachments → Google Drive

![level: Integrations](https://img.shields.io/badge/level-Integrations-D4A106?style=flat-square) ![domain: Admin / finance](https://img.shields.io/badge/domain-Admin_/_finance-334155?style=flat-square) ![build time: 20 min](https://img.shields.io/badge/build_time-20_min-0EA5E9?style=flat-square) ![nodes: 4](https://img.shields.io/badge/nodes-4-7C3AED?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** Invoices, bills, payslips and statements arrive as PDFs in email and get lost. This workflow files every PDF into one Drive folder with a date prefix, so you can find them at tax time.

## 🎯 What you'll learn

- Gmail Trigger (polling) with Gmail search filters
- Working with **binary data** (files) in n8n
- Splitting one email into many file items
- **Idempotency**: mark as read so the same email is never processed twice
- Google Drive upload into a folder

## 🏗️ Architecture

```mermaid
flowchart LR
  n0(["New Email with Attachment"]):::trigger
  n1["Split PDF Attachments"]:::code
  n2["Upload to Drive"]:::data
  n3["Mark Email as Read"]:::msg
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
Gmail Trigger (every 5 min, unread + PDF) → Code (1 item per PDF) → Drive upload → Gmail mark as read
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Gmail OAuth2 | [docs/credentials.md](../../docs/credentials.md) |
| Google Drive OAuth2 (the same Google Cloud project works, see docs/credentials.md) | [docs/credentials.md](../../docs/credentials.md) |

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Add **Gmail Trigger**: poll every 5 minutes. Turn *Simplify* off. Filters: search `has:attachment filename:pdf`, read status *Unread*. Options: *Download attachments* on.
2. Send yourself a test email with a PDF, then click *Fetch test event*. Look at the **Binary** tab of the output.
3. Add the **Code** node: it loops over `item.binary` and emits one item per PDF.
4. Add **Google Drive → Upload file**. Folder: paste your folder URL. File name: `{{ $json.fileName }}`.
5. Add **Gmail → Mark as read** with `messageId` from the Code node.
6. Activate it.

## ✅ Test it

- [ ] Email yourself 2 PDFs and 1 image. Exactly 2 files should appear in Drive.
- [ ] Check that the email is now read and that the next poll doesn't re-upload it.

## 🧯 Troubleshooting

<details><summary><b>Same file uploaded again and again</b></summary>

This was the bug in the original version: nothing marked the email as read. Keep the last node.

</details>

<details><summary><b>No binary data</b></summary>

*Download attachments* is off, or *Simplify* is on.

</details>

<details><summary><b>Drive 404 folder</b></summary>

Use the folder URL, and make sure your Google account owns the folder.

</details>

## 🚀 Level up

- Route by sender: bank → /Bank, employer → /Payslips (use Switch).
- Use Gemini to read the PDF and rename it `2026-09 Airtel bill ₹799.pdf` (see L12).

---

<p align="center"><a href="../L05-rss-news-code-node/README.md">← L05 · Tech news digest</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L07-lead-capture-sheets/README.md">L07 · Lead capture form → Google Sheets + welcome email →</a></p>
