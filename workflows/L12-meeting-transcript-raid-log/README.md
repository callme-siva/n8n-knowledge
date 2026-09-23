# L12 · Meeting transcript → RAID log

**Level:** 🟠 AI · **Domain:** Project management · **Build time:** 30 min

## The real-world problem
After a steering committee or status meeting, someone should update the RAID log. Usually nobody does. Paste the transcript (from Teams, Zoom or Meet) and every risk, assumption, issue and dependency lands in a sheet with owner, impact and due date.

## What you will learn
- **Structured Output Parser**: force the LLM to follow a JSON schema
- `hasOutputParser` on the LLM Chain
- **Split Out**: one AI answer → many items
- Mapping AI fields to spreadsheet columns

## How it flows
```
Form (transcript) → LLM Chain ⇐ Gemini, ⇐ Structured Parser → Split Out items → Set row → Sheets append
```

## Credentials you need
- Google Gemini API key
- Google Sheets OAuth2

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Create a Sheet tab **RAID** whose headers match the fields in *Build RAID Row*.
2. Form Trigger: meeting title, date, transcript (textarea).
3. **Basic LLM Chain** → turn on *Require Specific Output Format* → attach a **Structured Output Parser** and paste an example JSON (`items: [{category, description, owner, impact, ...}]`).
4. Attach the Gemini model.
5. **Split Out** on `output.items`.
6. **Set** the row columns, then **Sheets → Append**.

## Test it
- Paste a sample transcript from [docs/sample-data.md](../../docs/sample-data.md#meeting-transcript).
- Check that every row has a category from Risk/Assumption/Issue/Dependency and nothing else.

## Common errors
| Symptom | Fix |
|---|---|
| `Model output doesn't fit required format` | Lower the temperature to 0, simplify the schema example, or turn on auto-fix (L17 shows this). |
| Only one row appears | Split Out must point to the array path, `output.items`. |

## Level up (try these next)
- Email the owner of each high-impact risk.
- Run it over every transcript file dropped in a Drive folder.

---
[← Back to the learning path](../../README.md)
