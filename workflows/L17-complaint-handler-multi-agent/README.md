# L17 · Customer complaint handler (5 agents)

**Level:** 🔴 Multi-agent & production · **Domain:** Customer support · **Build time:** 45 min

## The real-world problem
Support teams spend the first 10 minutes of every complaint just working out what it is. This pipeline classifies it (category, urgency, sentiment), investigates, proposes a resolution and a goodwill gesture, decides whether to escalate, and drafts an empathetic reply.

## What you will learn
- Chained agents, each with its **own schema**
- **Auto-fixing output parser** (a second model repairs malformed JSON)
- Referencing any earlier step: `$('Understand Complaint').item.json.output`
- Designing escalation rules as explicit JSON (`escalate`, `priority`, `route_to`)

## How it flows
```
Form → Understand ⇐(model, schema⇐fix model) → Investigate ⇐… → Resolve ⇐… → Escalate? ⇐… → Draft reply ⇐model → Gmail
```

## Credentials you need
- Google Gemini API key
- Gmail OAuth2

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Import it and connect the Gemini credential. There are 10 model nodes: select them all and set the credential once.
2. Open the form and submit a complaint from [docs/sample-data.md](../../docs/sample-data.md#customer-complaints).
3. Click each agent in the execution and read its `output`. Look at how context builds up.
4. Change the email node to send to **yourself** while testing.

## Test it
- Try an angry high-value complaint (it should escalate) and a mild one (it shouldn't).

## Common errors
| Symptom | Fix |
|---|---|
| `Could not parse LLM output` | The fix model is supposed to catch this. Check that each *Fix Model* is connected to its parser. |
| It emails real customers during testing | Put your own email in *Send Response Email* until you're ready. |

## Level up (try these next)
- Add a real order lookup tool (Google Sheets or your DB) to the Investigate agent.
- Route escalations to a Slack channel and a Jira Service Management ticket.
- Insert an approval step (L15) before *Send Response Email*.

---
[← Back to the learning path](../../README.md)
