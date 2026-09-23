# L07 · Lead capture form → Sheets → welcome email

**Level:** 🟡 Integrations · **Domain:** Sales / marketing · **Build time:** 20 min

## The real-world problem
A small business or freelancer needs a *Contact us* form that stores the lead somewhere useful and replies instantly. No Typeform, no CRM subscription.

## What you will learn
- n8n **Form Trigger**: a hosted form with no web developer needed
- Cleaning input (trim, lowercase) in a Set node
- Google Sheets **Append row** with auto-mapped columns
- Sending a personalised email to the submitter

## How it flows
```
Form → Set (clean) → Google Sheets append → Gmail welcome
```

## Credentials you need
- Google Sheets OAuth2
- Gmail OAuth2

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Create a Google Sheet named *Leads* with header row: `timestamp, name, email, company, interest, budget, source`.
2. Add **n8n Form Trigger** with the 5 fields (Email field type = *Email*).
3. Open the **Test URL**, submit once, and look at the output keys: they are the field labels.
4. Add a **Set** node that renames and cleans the fields so they match your sheet headers exactly.
5. Add **Google Sheets → Append row**. Paste the sheet URL, pick the tab, *Map automatically*.
6. Add Gmail to `{{ $('Clean Lead').item.json.email }}`.

## Test it
- Submit the form 3 times with different data. You should see 3 rows and 3 emails.
- Activate it and share the **Production URL**.

## Common errors
| Symptom | Fix |
|---|---|
| Columns are empty in the sheet | The header names don't exactly match the Set field names. Spaces and case matter. |
| The Test URL stops working | Test URLs listen only while you click *Execute*. Use the Production URL once the workflow is active. |

## Level up (try these next)
- Add a duplicate check: *Sheets → Get rows* filtered by email before appending.
- Score the lead with AI and route hot leads to Slack (see **L22**).

---
[← Back to the learning path](../../README.md)
