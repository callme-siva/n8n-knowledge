# L02 · Daily weather email

**Level:** 🟢 Beginner · **Domain:** Personal productivity · **Build time:** 15 min

## The real-world problem
You want a short weather summary in your inbox every morning, before you leave home. This is the "hello world" of scheduled automation, and it calls a real public API.

## What you will learn
- Schedule Trigger and activating workflows
- A **Config node** pattern: keep every setting in one place
- HTTP Request with query parameters
- Referencing an earlier node: `$('⚙️ Config').item.json.city`
- Retry on fail (node Settings tab)
- Inline JavaScript in expressions (`? :` ternary)

## How it flows
```
Schedule (7 AM) → ⚙️ Config → HTTP GET open-meteo.com → Gmail
```

## Credentials you need
- Gmail OAuth2

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Add a **Schedule Trigger** → *Days*, hour 7.
2. Add a **Set** node named `⚙️ Config` with city, latitude, longitude, timezone and email_to. Get the coordinates from Google Maps (right-click → copy coordinates).
3. Add an **HTTP Request** node: GET `https://api.open-meteo.com/v1/forecast`, turn on *Send Query Parameters* and map them from Config.
4. In the HTTP node **Settings** tab, turn on *Retry On Fail* (3 tries, 5000 ms). Public APIs fail sometimes.
5. Add **Gmail**. Build the HTML body by dragging fields from the INPUT panel.
6. Run it once manually, then **Activate** it.

## Test it
- Click *Execute workflow*. A schedule workflow can always be run manually for testing.
- Check **Executions** (left sidebar) the next morning to see the automatic run.

## Common errors
| Symptom | Fix |
|---|---|
| Workflow never runs automatically | It isn't **Active**, or your n8n instance was asleep (for example a laptop that was closed). Use n8n Cloud or a VPS for 24/7. |
| Wrong hour | Set the timezone in *Workflow settings → Timezone*. |

## Level up (try these next)
- Add an **IF** node: send only if the rain chance is above 50% (this previews L04).
- Loop over 3 cities by making Config return 3 items.

---
[← Back to the learning path](../../README.md)
