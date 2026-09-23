# L15 · Retrospective → AI action items → human approval → Jira

**Level:** 🟠 AI · **Domain:** Agile / Scrum · **Build time:** 35 min

## The real-world problem
AI is good at turning messy retro notes into clear action items. But you don't want it filling Jira with junk tickets on its own. The Scrum Master gets an email with the proposal and clicks **Approve** or **Decline**, and only approved items become tasks.

## What you will learn
- **Send and Wait for Response**: pause a workflow for a human decision
- Wait time limits (auto-timeout after 2 days)
- Structured output for a list of action items
- Keeping data across a pause: `$('Node').first()`
- Responsible-AI design: the AI proposes and a human decides

## How it flows
```
Form → LLM Chain ⇐ Gemini, ⇐ Schema → Code (HTML) → Gmail send-and-wait ⏸ → IF approved
   ├─ yes → one item per action → Jira create task
   └─ no  → stop
```

## Credentials you need
- Google Gemini API key
- Gmail OAuth2
- Jira Software Cloud API token

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Build the form (sprint, 3 textareas, morale dropdown).
2. **Basic LLM Chain** + Gemini + **Structured Output Parser** with the example JSON.
3. Code: build an HTML summary for the approver.
4. **Gmail → Send and Wait for Response**, response type *Approval*, *Approve and Disapprove* buttons. Limit the wait to 2 days.
5. **IF** `{{ $json.data.approved }}` is true.
6. Code: turn `action_items` back into items, then **Jira → Create issue** for each one.

## Test it
- Submit a retro from [docs/sample-data.md](../../docs/sample-data.md#retro-feedback). You should get an approval email and see the execution *Waiting*.
- Click **Approve**: 1–3 Jira tasks should appear. Try again and click **Decline**: no tasks.

## Common errors
| Symptom | Fix |
|---|---|
| Approval link opens an error page | Your n8n must be reachable from where you click. Set `WEBHOOK_URL` if you self-host behind a tunnel or domain. |
| `approved` is undefined | Check the output of the Gmail node. The decision lives in `data.approved`. |

## Level up (try these next)
- Collect retros from the whole team for a week, then analyse all of them together (Aggregate node).
- Post the approval to Slack instead (the Slack node also has *Send and Wait*).

---
[← Back to the learning path](../../README.md)
