# L19 · Global error handler

**Level:** 🔴 Multi-agent & production · **Domain:** Operations / reliability · **Build time:** 20 min

## The real-world problem
Automation that fails silently is worse than none, because you think the reports are going out when they aren't. One error workflow can watch *all* your workflows, email you with a plain-English hint, and keep a log you can review every week.

## What you will learn
- **Error Trigger** and the *Error workflow* setting
- Error payload: `execution.error.message`, `lastNodeExecuted`, `execution.url`
- Pattern-matching errors into actionable hints
- Node-level *On Error: continue* so the alerting itself never crashes
- The full reliability toolkit: Retry on Fail · Continue on Error · Stop and Error · Error workflow

## How it flows
```
Error Trigger → Code (shape + hint) ─┬→ Gmail alert
                                    └→ Sheets log
```

## Credentials you need
- Gmail OAuth2
- Google Sheets OAuth2 (tab `Errors`: time, workflow, workflow_id, node, message, hint, url, mode)

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Add **Error Trigger** (this workflow never needs to be *active*).
2. Add the Code node to shape the error and generate a hint.
3. Add Gmail and Sheets in parallel, each with *On Error → Continue*.
4. Open **every** other workflow → *Settings* → **Error workflow** → choose this one.

## Test it
- Activate **L04** with `base = XYZ` (or disconnect a credential) and let it run. The alert should arrive within seconds.
- Note: error workflows fire for **production** executions, not manual test runs.

## Common errors
| Symptom | Fix |
|---|---|
| No alert when testing manually | That's expected. Only automatic (trigger or production) executions call the error workflow. |
| Alert loop | Never set L19 as its own error workflow. |

## Level up (try these next)
- Add Slack / Telegram alerts.
- Weekly summary: read the Errors sheet → group by workflow → email the top offenders.

---
[← Back to the learning path](../../README.md)
