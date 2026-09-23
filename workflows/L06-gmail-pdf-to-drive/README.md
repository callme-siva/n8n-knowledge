# L06 · Gmail PDF attachments → Google Drive

**Level:** 🟡 Integrations · **Domain:** Admin / finance · **Build time:** 20 min

## The real-world problem
Invoices, bills, payslips and statements arrive as PDFs in email and get lost. This workflow files every PDF into one Drive folder with a date prefix, so you can find them at tax time.

## What you will learn
- Gmail Trigger (polling) with Gmail search filters
- Working with **binary data** (files) in n8n
- Splitting one email into many file items
- **Idempotency**: mark as read so the same email is never processed twice
- Google Drive upload into a folder

## How it flows
```
Gmail Trigger (every 5 min, unread + PDF) → Code (1 item per PDF) → Drive upload → Gmail mark as read
```

## Credentials you need
- Gmail OAuth2
- Google Drive OAuth2 (the same Google Cloud project works, see docs/credentials.md)

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Add **Gmail Trigger**: poll every 5 minutes. Turn *Simplify* off. Filters: search `has:attachment filename:pdf`, read status *Unread*. Options: *Download attachments* on.
2. Send yourself a test email with a PDF, then click *Fetch test event*. Look at the **Binary** tab of the output.
3. Add the **Code** node: it loops over `item.binary` and emits one item per PDF.
4. Add **Google Drive → Upload file**. Folder: paste your folder URL. File name: `{{ $json.fileName }}`.
5. Add **Gmail → Mark as read** with `messageId` from the Code node.
6. Activate it.

## Test it
- Email yourself 2 PDFs and 1 image. Exactly 2 files should appear in Drive.
- Check that the email is now read and that the next poll doesn't re-upload it.

## Common errors
| Symptom | Fix |
|---|---|
| Same file uploaded again and again | This was the bug in the original version: nothing marked the email as read. Keep the last node. |
| No binary data | *Download attachments* is off, or *Simplify* is on. |
| Drive 404 folder | Use the folder URL, and make sure your Google account owns the folder. |

## Level up (try these next)
- Route by sender: bank → /Bank, employer → /Payslips (use Switch).
- Use Gemini to read the PDF and rename it `2026-09 Airtel bill ₹799.pdf` (see L12).

---
[← Back to the learning path](../../README.md)
