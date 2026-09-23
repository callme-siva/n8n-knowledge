# L11 · AI news briefing with a Basic LLM Chain

**Level:** 🟠 AI · **Domain:** Learning / research · **Build time:** 20 min

## The real-world problem
25 headlines is still too many to read. An LLM can turn them into 5 bullets that say *why each story matters*, which is what a good executive briefing does.

## What you will learn
- Basic LLM Chain node: prompt in, text out
- Connecting a **Chat Model sub-node** (Gemini)
- Writing a system prompt with rules and an output format
- Temperature: 0.3 for factual summaries
- Keeping the raw data in the email as a fallback, so the AI never hides the source

## How it flows
```
Schedule → 3× RSS → Merge → Code (from L05) → LLM Chain ⇐ Gemini → Gmail
```

## Credentials you need
- Google Gemini (PaLM) API key: free at https://aistudio.google.com/app/apikey
- Gmail OAuth2

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Start from your finished **L05** (duplicate it).
2. Get a Gemini API key from AI Studio. In n8n, create a *Google Gemini(PaLM) Api* credential (host is the default).
3. Between Code and Gmail, add **Basic LLM Chain**. Prompt = *Define below*, and put `{{ $json.listText }}` in the prompt.
4. Click **+ Chat Model** under the chain and choose **Google Gemini Chat Model** → `gemini-2.5-flash`.
5. Add a *System* message (Chat Messages → System) with the editor rules.
6. Gmail body = `{{ $json.text }}`.

## Test it
- Run it and compare the briefing to the raw headlines. Did the model invent anything?
- Change the system prompt to *Explain like I'm a school student* and run it again.

## Common errors
| Symptom | Fix |
|---|---|
| 429 / quota exceeded | The free tier has per-minute limits. Wait a minute, or use `gemini-2.5-flash-lite`. |
| Output shows ```html fences | Add "no code fences" to the prompt, or strip them with `.replace(/```html|```/g,'')`. |

## Level up (try these next)
- Ask for JSON and render your own template (this previews L12).
- Send it to Telegram as a morning message.

---
[← Back to the learning path](../../README.md)
