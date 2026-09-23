# L10 · Bug report form → Jira issue

**Level:** 🟡 Integrations · **Domain:** Agile / product support · **Build time:** 20 min

## The real-world problem
Users, testers and business teams report bugs in chat and email, and half the details are missing. A structured form creates a proper Jira Bug with priority set, and the reporter gets the ticket number straight away.

## What you will learn
- Form fields with dropdowns and validation
- Mapping business language to system values (Severity → Priority)
- Jira **Create issue** with labels
- Using the output of a *create* call (`$json.key`) in the next step

## How it flows
```
Form → Code (map severity, build summary) → Jira create Bug → Gmail confirmation with ticket key
```

## Credentials you need
- Jira Software Cloud API token
- Gmail OAuth2

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Find your project ID and Bug issue type ID. In the Jira node, switch the fields to *From list* and pick them, which fills the IDs.
2. Build the form with 5 fields.
3. Add a Code node (*for each item*) that builds `summary`, `description` and `priority`.
4. Add **Jira → Issue → Create**. Add labels `from-form`. (Priority needs your Jira priority IDs; add it under *Additional fields* once you know them.)
5. Add Gmail using `{{ $json.key }}` from the Jira output.

## Test it
- Submit a Blocker bug. Check that the Jira issue exists and that the email shows the key.

## Common errors
| Symptom | Fix |
|---|---|
| `issuetype: Specify a valid issue type` | Team-managed and company-managed projects use different issue-type IDs. Pick them from the list. |
| Description formatting looks odd | Jira Cloud v3 uses ADF, and n8n converts plain text. Keep it simple, or use the Jira REST API via HTTP for rich text. |

## Level up (try these next)
- Accept a screenshot upload (form *File* field) and attach it to the issue.
- Let AI detect duplicates before creating the issue (L14 agent + Jira search tool).

---
[← Back to the learning path](../../README.md)
