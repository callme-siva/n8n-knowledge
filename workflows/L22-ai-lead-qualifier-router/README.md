# L22 · AI lead qualifier & router (capstone)

**Level:** 🔴 Multi-agent & production · **Domain:** Sales · **Build time:** 40 min

## The real-world problem
Sales teams waste hours on tyre-kickers while hot leads go cold. This capstone scores every enquiry with AI (BANT), logs it to a CRM sheet, alerts sales straight away for hot leads, sends a personalised reply, and sends cold leads a nurture email.

## What you will learn
- Combines **everything**: form, structured AI output, Set, Sheets, Switch routing, multiple Gmail branches
- AI as a *decision-maker* with explicit, auditable reasons
- Temperature 0 for consistent scoring
- Designing the fallback path (cold leads still get a reply)

## How it flows
```
Form → LLM Chain ⇐ Gemini, ⇐ Schema → Set CRM row → Sheets → Switch
   ├ Hot  → Alert sales → Personal reply
   ├ Warm → Personal reply
   └ Cold → Nurture email
```

## Credentials you need
- Google Gemini API key
- Google Sheets OAuth2 (tab `Leads`: time, name, email, company, score, tier, reason, use_case, reply)
- Gmail OAuth2

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Build it yourself using L07 + L12 + L04 as references. That is the capstone test.
2. If you get stuck, import `workflow.json` and compare node by node.
3. Set the workflow's *Error workflow* to L19.

## Test it
- Submit the 3 sample leads in [docs/sample-data.md](../../docs/sample-data.md#sales-leads): one each should come out hot, warm and cold.

## Common errors
| Symptom | Fix |
|---|---|
| Every lead is 'warm' | Make the rubric stricter and give examples in the system prompt. |
| A replied lead gets 2 emails | Hot goes through alert → reply once. Check you didn't also wire Hot directly to *Personal Reply*. |

## Level up (try these next)
- Replace the Sheet with HubSpot / Zoho CRM nodes.
- Add an approval step (L15) before the AI reply goes out.
- Enrich with company data via an API before scoring.

---
[← Back to the learning path](../../README.md)
