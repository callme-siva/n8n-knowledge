# L09 · Expense logger API with Webhook

**Level:** 🟡 Integrations · **Domain:** Finance / developer · **Build time:** 25 min

## The real-world problem
You want to log expenses from anywhere: an iPhone Shortcut, a Telegram bot, a Google Form or another app. A webhook turns n8n into your own small API with validation and proper HTTP status codes.

## What you will learn
- **Webhook** node (POST, JSON body in `$json.body`)
- *Respond to Webhook* for custom status codes (201 / 400)
- Input validation in Code (*Run once for each item*)
- Set node in raw JSON mode
- Test URL and Production URL

## How it flows
```
Webhook POST /expense → Code validate → IF valid
  ├─ true  → Set row → Sheets append → Respond 201
  └─ false → Respond 400 {errors}
```

## Credentials you need
- Google Sheets OAuth2

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Create a sheet tab *Expenses* with headers `date, amount, category, note, submitted_by`.
2. Add **Webhook**: method POST, path `expense`, Respond = *Using 'Respond to Webhook' node*.
3. Click *Listen for test event*, then run the curl command from the sticky note using the **Test URL**.
4. Add the **Validate** Code node (mode: *Run once for each item*).
5. Add **IF** `valid is true`, then on the true branch Set (raw JSON) → Sheets append → **Respond to Webhook** (201).
6. On the false branch, **Respond to Webhook** with 400.

## Test it
- `curl ... -d '{"amount":450,"category":"food"}'` should return 201.
- `curl ... -d '{"amount":-5,"category":"pizza"}'` should return 400 with 2 errors.
- iPhone: Shortcuts app → *Get contents of URL* → POST JSON. That gives you a one-tap expense logger.

## Common errors
| Symptom | Fix |
|---|---|
| `Webhook node not correctly configured` | Respond mode must be *Using Respond to Webhook node* when you use that node. |
| 404 on the production URL | The workflow isn't active. Test URLs use `/webhook-test/`, production uses `/webhook/`. |
| Anyone can post to my webhook | Add *Header Auth* in the Webhook authentication option. |

## Level up (try these next)
- Add Header Auth with a secret token.
- Add a daily 9 PM summary: *Sheets get rows* → sum by category → email.

---
[← Back to the learning path](../../README.md)
