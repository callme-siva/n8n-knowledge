<div align="center">

# 🧪 End-to-end tests

**Every workflow is executed in a real n8n on every push, with 61 behaviour checks.**

</div>

---

## What runs for real, and what is mocked

| Runs for real | Replaced by realistic mocks |
|---|---|
| Code nodes, IF / Switch / Filter, Merge, loops (Loop Over Items), Wait (shortened to 1 s), Set, Aggregate, Remove Duplicates, Crypto, HTML extraction, expressions | Anything that needs **your** credentials: Gmail, Google Sheets / Drive / Calendar, Jira, Slack, Telegram, Gemini (chains, agents, extractors, classifiers), authenticated HTTP (SerpAPI, GitHub) |
| **Live** public APIs: Open-Meteo, open.er-api.com, RSS feeds, books.toscrape.com, quickchart.io | Event triggers (form, webhook, Gmail, chat, error, sub-workflow) become a manual start + a sample event |

Sheets writes with inline column mappings are evaluated for real (their expressions are part of the test).

## Behaviour checks

Passing means more than "didn't crash". Examples from [`fixtures.py`](fixtures.py):

| Workflow | Check |
|---|---|
| P01 invoices | 3 invoices in → 2 to the ledger, 1 to approval, 1 exception mentioning `≠ total` and `GSTIN format invalid` |
| P03 incidents | 3 alerts in → 1 page, 1 notify, 1 suppressed; exactly **one** Jira incident |
| P05 bulk AI | 23 rows → 23 checkpoints, summary says `processed: 23, errors: 0` |
| P08 sync | exactly 1 create, 1 update, 1 skip |
| P11 PII gateway | the audit log must **not** contain the raw email or card number; the caller's answer must |
| Q06 reminders | 1 friendly nudge + 1 firm reminder, both written back |

## Bugs this harness caught (and we fixed)

1. **Timezone off-by-one** in 7 workflows: `new Date().toISOString()` is UTC, so near midnight "today" was yesterday. Invoice reminders were skipped and birthday wishes came a day late. Fixed with `$today` / Luxon in the workflow timezone.
2. **P05 summary under-counted**: inside a loop, `$('Node').all()` returns only the **last batch**. Fixed by counting the loop's *done* output.
3. **L06 PDF splitting** was never exercised with a real attachment. The harness now injects binary files.

## Run it yourself

```bash
mkdir -p /tmp/n8n && cd /tmp/n8n && npm init -y && npm i n8n@2.40.5
```
```bash
N8N_DIR=/tmp/n8n python3 tests/harness.py
```
Run a subset by prefix: `python3 tests/harness.py P01 Q06`. Results are written to [`results.json`](results.json) and shown as the **e2e test** badge on each lesson.

## Adding a workflow

1. Add a sample event to `TRIGGERS` if it starts from a form, webhook, chat, etc.
2. Add fixtures for any node the harness can't mock by default (it tells you which).
3. Add at least one `EXPECT` behaviour check that would fail if the logic were wrong.

<p align="center"><a href="../README.md">← Back to the learning path</a> · <a href="../docs/testing.md">🧪 Testing guide</a></p>
