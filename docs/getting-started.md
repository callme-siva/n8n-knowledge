<div align="center">

# 🚀 Getting started

**Install n8n, import workflows and learn the 5 core ideas.**

</div>

---

## 1. Run n8n: pick one

| Option | Best for | Cost | 24/7 schedules? |
|---|---|---|---|
| **[n8n Cloud](https://app.n8n.cloud/register)** — sign up, no card | Fastest start, no install | 14-day trial, then paid | ✅ |
| **npx** on your laptop | Learning L01–L15 | Free | ❌ only while the laptop is on |
| **Docker** on laptop / VPS | Serious use, L19–L21 | Free (plus a VPS from about $5/month) | ✅ on a VPS |

### npx (needs Node.js 20+)
```bash
npx n8n
```
Open http://localhost:5678 and create your owner account.

### Docker
```bash
docker volume create n8n_data
```
```bash
docker run -it --rm --name n8n -p 5678:5678 -e GENERIC_TIMEZONE=Asia/Kolkata -e TZ=Asia/Kolkata -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

> [!IMPORTANT]
> **Webhooks and forms from outside your laptop** (L09, L15 approval links): your n8n must be reachable from the internet. On a VPS, set `WEBHOOK_URL=https://your-domain/`. On a laptop, use a tunnel (for example `cloudflared tunnel --url http://localhost:5678`) and set `WEBHOOK_URL` to the tunnel URL.

**Tested with:** n8n **2.40.x**. The workflows use node versions available since n8n 1.90, so older 1.x installs should mostly work.

## 2. The five ideas you need

1. **Workflow** = trigger + nodes + connections.
2. **Items**: data flows as a *list* of JSON items. Most nodes run once per item.
3. **Expressions**: `{{ $json.field }}` reads the current item; `{{ $('Node Name').item.json.field }}` reads an earlier node.
4. **Credentials** are stored once and reused. Workflows in this repo never contain them.
5. **Active vs manual**: triggers (schedule, webhook, Gmail) only fire automatically when the workflow is **Active**. *Execute workflow* is for testing.

## 3. Import a workflow
- **Paste:** open `workflow.json` → *Raw* → copy all → click an empty n8n canvas → `Ctrl/Cmd + V`.
- **File:** *⋯ (top right) → Import from File*.
- **CLI (all at once):**
  ```bash
  npx n8n import:workflow --separate --input=./workflows-flat/
  ```
  (Copy each `workflow.json` into one folder with a unique name first. `docs/testing.md` has a one-liner.)

After import, open every node with a ⚠️ and pick your credential. Then search the workflow for `PASTE_YOUR` / `REPLACE_` / `you@example.com` and put in your own values.

## 4. A good routine for each lesson
1. Read the lesson README: problem, then concepts.
2. Build it **yourself** from the steps. Run it after *every* node and read the OUTPUT panel.
3. Break it on purpose (wrong field name, bad URL) and read the error.
4. Compare with `workflow.json`.
5. Do one of the *Level up* ideas.

---

<p align="center"><a href="../README.md">← Back to the learning path</a> · <a href="architecture.md">🏗️ Architecture</a></p>
