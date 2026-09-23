# L20 · Sub-workflows: reusable building blocks

**Level:** 🔴 Multi-agent & production · **Domain:** HR / team culture · **Build time:** 30 min

## The real-world problem
After 10 workflows you'll have copy-pasted the same email template 10 times. Sub-workflows are functions for n8n: build *Send branded email* once and call it from anywhere. The example use is automatic birthday and work-anniversary wishes, which every HR and team lead wants.

## What you will learn
- **Execute Workflow Trigger** with typed inputs (the callee)
- **Execute Workflow** node (the caller) with mapped inputs
- Returning data from a sub-workflow
- Code that returns 0..N items (no one celebrating today means nothing runs)
- Designing for reuse: small, single-purpose workflows

## How it flows
```
CALLER  Schedule → Sheets read → Code (filter today) → Execute Workflow(L20a)
CALLEE  Execute Workflow Trigger → Code (template) → Gmail → Set (return)
```

## Credentials you need
- Google Sheets OAuth2
- Gmail OAuth2

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Import **L20a** first and save it. Copy its ID from the URL (`/workflow/<ID>`).
2. Create a sheet tab **Team** with `name, email, birthday, joined` (dates as YYYY-MM-DD). Put today's date in one row for testing.
3. Import **L20**. In *Call: Send Branded Email*, select L20a *From list* (or paste the ID).
4. Run it.

## Test it
- Look at the Execute Workflow output: it contains `sent: true` returned by the sub-workflow.
- Change the header colour in L20a and run again. Every caller gets the new look.

## Common errors
| Symptom | Fix |
|---|---|
| `Workflow does not exist` | Wrong ID, or L20a wasn't saved. |
| The sub-workflow receives empty fields | Input names must match exactly on both sides. |

## Level up (try these next)
- Call L20a from L02, L08 and L19 to give every email the same branding.
- Make an L20b *Log to Sheet* sub-workflow for audit logs.

---
[← Back to the learning path](../../README.md)
