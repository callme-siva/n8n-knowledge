# L01 · Hello n8n — your first workflow

**Level:** 🟢 Beginner · **Domain:** General · **Build time:** 10 min

## The real-world problem
Everyone starts here. Before automating anything real, you need to understand how data moves between nodes. This workflow takes some values, builds a message and emails it to you.

## What you will learn
- Manual Trigger: run a workflow on demand
- Set node: create data without code
- Code node: transform items with JavaScript
- Expressions: `{{ $json.field }}`
- Reading the INPUT and OUTPUT panels

## How it flows
```
Manual Trigger → Set Your Data → Build Greeting (Code) → Send to Yourself (Gmail)
```

## Credentials you need
- Gmail OAuth2 — see [docs/credentials.md](../../docs/credentials.md#gmail). *Optional*: delete the Gmail node and the workflow still teaches everything.

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Create a new workflow and name it `L01 · Hello n8n`.
2. Add a **Manual Trigger** node.
3. Add an **Edit Fields (Set)** node with three fields: `name` (string), `city` (string), `tasks_done` (number).
4. Add a **Code** node and paste the code from `workflow.json`. Look at how it spreads `...item.json` to keep the old fields.
5. Add a **Gmail → Send message** node. In *To*, put your own email. In *Message*, drag `greeting` from the INPUT panel.
6. Click **Execute workflow**.

## Test it
- Click each node and open the **OUTPUT** tab: Table, JSON and Schema views show the same data in different shapes.
- Change `tasks_done` to 10 and run again.

## Common errors
| Symptom | Fix |
|---|---|
| `Credentials not found` on Gmail | Open the node → Credential → *Create new* and sign in with Google. |
| Code node: `Cannot read properties of undefined` | Check the field name spelling — JSON keys are case-sensitive. |

## Level up (try these next)
- Add a second item in the Set node (turn on *Include Other Input Fields*) or return two items from Code — watch Gmail send two emails.
- Replace Gmail with Telegram or Slack.

---
[← Back to the learning path](../../README.md)
