# L08 · Daily stale Jira stories report

**Level:** 🟡 Integrations · **Domain:** Agile / Scrum · **Build time:** 20 min

## The real-world problem
Stories sit "In Progress" for days without anyone saying so at stand-up. A Scrum Master wants a list every weekday morning of what's stuck and who owns it, so the stand-up can start with it.

## What you will learn
- Jira Software node + **JQL** queries
- Cron expression for weekdays only (`0 9 * * 1-5`)
- `alwaysOutputData`: still send the ✅ email when Jira returns nothing
- Grouping and counting with `reduce`
- Conditional styling in HTML (red if more than 7 days)

## How it flows
```
Schedule (Mon–Fri 9 AM) → Config → Jira search (JQL) → Code (table + per-person count) → Gmail
```

## Credentials you need
- Jira Software Cloud: email + API token from id.atlassian.com → Security → API tokens
- Gmail OAuth2

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Create an API token at https://id.atlassian.com/manage-profile/security/api-tokens and add a **Jira SW Cloud API** credential (domain + email + token).
2. Schedule Trigger → *Custom (cron)* → `0 9 * * 1-5`.
3. Config: project_key, stale_days, email_to, jira_base_url.
4. **Jira → Issue → Get many**, Return all, Options → JQL. Test your JQL in Jira's own search first!
5. Node Settings → **Always Output Data** on (so an empty result still continues).
6. Code node builds the report, then Gmail.

## Test it
- Set `stale_days` to 0 so you see every in-progress story.
- Use a project key that doesn't exist. You should get a clear Jira error.

## Common errors
| Symptom | Fix |
|---|---|
| `JQL: field 'statusCategory' does not exist` | On older Jira Server, use `status = "In Progress"`. |
| No email when there are no stale stories | Turn on *Always Output Data* on the Jira node. |

## Level up (try these next)
- Post it to the team Slack/Teams channel instead of email.
- Also comment on each stale issue: "Any blockers? 🙂".

---
[← Back to the learning path](../../README.md)
