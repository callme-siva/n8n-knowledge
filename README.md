# n8n Knowledge: learn automation by building 22 real workflows

A **step-by-step learning path** for [n8n](https://n8n.io), from your first two-node workflow to multi-agent AI systems you can run in production.
Every workflow solves a real problem, imports in one click, and comes with a guide that teaches you to **build it yourself**.

- 🆓 **Free to run.** Uses Google Gemini (free tier) and free public APIs wherever possible.
- 🪜 **Each level builds on the last.** Every workflow adds one or two new concepts, nothing more.
- 🧪 **Tested.** Every workflow is checked against a real n8n install (node types, versions and parameters) in CI.
- 📝 **Instructions on the canvas.** Each workflow has sticky notes that explain it where you're working.
- 🔒 **Safe to share.** No credentials, no personal data, no pinned test data (enforced by CI).

---

## Start here

1. **Get n8n running.** See [docs/getting-started.md](docs/getting-started.md) (n8n Cloud trial, `npx n8n`, or Docker).
2. **Set up credentials once.** See [docs/credentials.md](docs/credentials.md) (Gemini key, Google, Jira).
3. Go through the levels in order. For each workflow: read the README, **build it yourself**, then compare with `workflow.json`.

> **How to import:** open a workflow's `workflow.json` on GitHub → *Raw* → copy → in n8n press `Ctrl/Cmd + V` on an empty canvas. Or use *⋯ → Import from File*.

---

## The learning path

### 🟢 Level 1: Basics
| # | Workflow | Real-world use | You learn |
|---|---|---|---|
| L01 | [Hello n8n](workflows/L01-hello-n8n) | Your first automated email | Items, Set, Code, expressions |
| L02 | [Daily weather email](workflows/L02-daily-weather-email) | Morning briefing | Schedule, HTTP API, Config pattern, retries |
| L03 | [Job search digest](workflows/L03-job-search-api) | Job hunting | API credentials, parsing nested JSON |
| L04 | [Currency rate alert](workflows/L04-currency-alert-switch) | Money transfers, invoicing | IF, Switch, Stop and Error |
| L05 | [Tech news digest](workflows/L05-rss-news-code-node) | Staying informed | RSS, Merge, Code node (filter / dedupe / sort) |

### 🟡 Level 2: Integrations
| # | Workflow | Real-world use | You learn |
|---|---|---|---|
| L06 | [Gmail PDFs → Drive](workflows/L06-gmail-pdf-to-drive) | Filing bills and invoices | Gmail trigger, binary files, idempotency |
| L07 | [Lead capture form](workflows/L07-lead-capture-sheets) | Sales and marketing | n8n Forms, Google Sheets |
| L08 | [Stale Jira stories](workflows/L08-jira-stale-stories) | Scrum Master stand-up | Jira + JQL, cron |
| L09 | [Expense logger API](workflows/L09-webhook-expense-api) | Build your own API | Webhook, validation, HTTP status codes |
| L10 | [Bug report → Jira](workflows/L10-form-bug-report-jira) | Product support | Mapping forms to Jira |

### 🟠 Level 3: AI
| # | Workflow | Real-world use | You learn |
|---|---|---|---|
| L11 | [AI news briefing](workflows/L11-ai-news-digest-llm-chain) | Executive summary | LLM Chain, Gemini, prompting |
| L12 | [Transcript → RAID log](workflows/L12-meeting-transcript-raid-log) | Project management | **Structured output**, Split Out |
| L13 | [HR policy chatbot](workflows/L13-rag-policy-chatbot) | Internal help desk | **RAG**, embeddings, vector store |
| L14 | [Assistant with tools](workflows/L14-ai-agent-with-tools) | Personal assistant | **AI Agent**, tools, memory |
| L15 | [Retro → approval → Jira](workflows/L15-retro-ai-approval-jira) | Agile retrospectives | **Human-in-the-loop** approval |

### 🔴 Level 4: Multi-agent and production
| # | Workflow | Real-world use | You learn |
|---|---|---|---|
| L16 | [Sprint report (4 agents)](workflows/L16-sprint-report-multi-agent) | Delivery management | GitHub GraphQL, sequential agents |
| L17 | [Complaint handler (5 agents)](workflows/L17-complaint-handler-multi-agent) | Customer support | Auto-fixing parsers, escalation |
| L18 | [Resume ↔ job fit](workflows/L18-resume-job-fit-multi-agent) | Recruiting / career | PDF extraction, specialist agents |
| L19 | [Global error handler](workflows/L19-global-error-handler) | Reliability | Error Trigger, alerting |
| L20 | [Sub-workflows](workflows/L20-subworkflows-caller) (+ [L20a](workflows/L20a-subworkflow-send-branded-email)) | Birthday and anniversary wishes | Reusable workflows |
| L21 | [Uptime monitor](workflows/L21-website-uptime-monitor) | DevOps / IT | Static data, alert-on-change |
| L22 | [AI lead qualifier](workflows/L22-ai-lead-qualifier-router) 🏁 | Sales **capstone** | Everything together |

**Domains covered:** Agile/Scrum (L08, L10, L15, L16) · PM (L12) · Sales (L07, L22) · Support (L17) · HR (L13, L18, L20) · Finance (L04, L06, L09) · DevOps (L19, L21) · Personal (L01–L03, L05, L11, L14)

---

## How this repo differs from other n8n collections

| | Big template dumps (2,000+ JSONs) | Video courses | **This repo** |
|---|---|---|---|
| Order to learn in | ❌ search and hope | ✅ | ✅ 4 levels, one new concept at a time |
| Explains *why*, not only *what* | ❌ | ✅ (in video) | ✅ written, searchable, on the canvas |
| Step-by-step "build it yourself" | ❌ | ✅ | ✅ |
| Test data included | ❌ | sometimes | ✅ [sample-data.md](docs/sample-data.md) |
| Common errors and fixes | ❌ | ❌ | ✅ in every README |
| Production practices (errors, retries, idempotency, human approval) | rarely | rarely | ✅ built in |
| Verified against a real n8n version | ❌ | n/a | ✅ CI + `tools/check-nodes.js` |
| Free to run | varies (often OpenAI) | varies | ✅ Gemini free tier |

If you just want *any* template for a niche app, the big collections are great. This repo is for **learning to design workflows yourself**.

---

## Repo layout
```
workflows/Lxx-name/
  workflow.json   ← import into n8n
  README.md       ← problem, concepts, build steps, tests, errors, next steps
docs/             ← getting started, credentials, testing, sample data
tools/            ← build.py (generates workflows), validate.py (CI), check-nodes.js (deep check)
```

## Contributing
New workflows are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md). Every workflow must pass `python3 tools/validate.py`.

License: [MIT](LICENSE)
