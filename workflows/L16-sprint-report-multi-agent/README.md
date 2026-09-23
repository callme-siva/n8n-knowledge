# L16 · Sprint progress report with 4 cooperating agents

**Level:** 🔴 Multi-agent & production · **Domain:** Agile / engineering management · **Build time:** 45 min

## The real-world problem
A delivery lead needs one daily email: is the sprint on track, who is overloaded, is the backlog healthy? Each question needs a different lens, so one specialist agent handles each lens and a coordinator writes the final report.

## What you will learn
- GitHub **GraphQL** API via HTTP Request
- Computing metrics in code *before* the LLM sees them (cheaper, and no maths mistakes)
- **Sequential multi-agent** pattern: each agent reads the metrics plus the earlier agents' notes
- A coordinator agent that merges the specialists' output into one report

## How it flows
```
Schedule → Config → Code (GraphQL query) → HTTP POST api.github.com/graphql → Code (metrics)
 → Capacity agent → Backlog agent → Burndown agent → Coordinator agent → Gmail
```

## Credentials you need
- GitHub API token (classic PAT with `read:project`, `repo`)
- Google Gemini API key
- Gmail OAuth2

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Create a GitHub Project (v2) with Status, Estimate and Iteration fields, and add some issues.
2. Create a GitHub credential with a PAT.
3. Config: `org` (your user/org URL), `projectNumber`, recipient email.
4. Import this workflow and run it up to *Compute Sprint Metrics*. Read the metrics JSON before any AI step runs.
5. Run the full chain and read each agent's output in order.

## Test it
- Change a few issue statuses in GitHub, run it again, and compare the burndown text.

## Common errors
| Symptom | Fix |
|---|---|
| GraphQL `Could not resolve to a ProjectV2` | Wrong project number, or it's a user project and the query expects an org. The code handles both, so check `org`. |
| The report contradicts the metrics | Lower the temperature, and tell agents to quote the numbers from the JSON. |

## Level up (try these next)
- Swap GitHub for Jira (Jira node, sprint JQL).
- Run the three specialist agents in **parallel** and merge them, which is faster.

---
[← Back to the learning path](../../README.md)
