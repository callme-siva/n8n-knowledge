# L21 · Website & API uptime monitor

**Level:** 🔴 Multi-agent & production · **Domain:** DevOps / IT · **Build time:** 30 min

## The real-world problem
Paid uptime tools cost money, and simple ones spam you every 5 minutes while a site is down. This monitor checks your sites and APIs, logs response times, and alerts only when the state *changes*: once when a site goes down and once when it recovers.

## What you will learn
- HTTP Request with **Full Response + Never Error** (read status codes instead of crashing)
- **Workflow static data**: memory that survives between executions
- Alert on *change* instead of on *state*, which avoids alert fatigue
- Filter node
- Fan-out: log everything, alert on some

## How it flows
```
Schedule (5 min) → Code (site list) → HTTP (full response, never error) → Code (compare state)
   ├→ Sheets log (every check)
   └→ Filter changed → Gmail alert
```

## Credentials you need
- Gmail OAuth2
- Google Sheets OAuth2 (tab `Uptime`: time, name, url, status, code, ms, changed, since, error)

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Edit the site list in *Sites to Watch*.
2. HTTP Request: URL `{{ $json.url }}`, Options → *Response → Include full response* + *Never error*, timeout 10 s.
3. Code: read and update `$getWorkflowStaticData('global')`.
4. Filter `changed = true` → Gmail.
5. **Activate** it (static data isn't saved in manual runs).

## Test it
- The `httpstat.us/503` demo site should alert DOWN on the second automatic run.
- Replace it with `https://httpstat.us/200` and you should get an 🟢 recovery alert.

## Common errors
| Symptom | Fix |
|---|---|
| Alerts never fire | Static data only persists in *active* executions. Manual runs start fresh every time. |
| Every site shows DOWN | Check that *Never error* and *Full response* are both on, so `statusCode` exists. |

## Level up (try these next)
- Add a slowness alert (ms > 3000 for 3 checks in a row).
- Weekly uptime % report from the Uptime sheet.
- Check SSL certificate expiry via an API.

---
[← Back to the learning path](../../README.md)
