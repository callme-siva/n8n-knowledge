# L14 · Personal assistant agent with tools

**Level:** 🟠 AI · **Domain:** Personal productivity · **Build time:** 30 min

## The real-world problem
A plain LLM can't know today's weather and often gets arithmetic wrong. An **agent** can call tools. It reads the question, picks the right tool, calls it, and writes the answer from the result.

## What you will learn
- AI Agent node (tools agent)
- Built-in tools: Calculator, Wikipedia
- **HTTP Request Tool** with `{placeholders}` the model fills in
- Window Buffer Memory for multi-turn chat
- Tool descriptions are prompts: write them carefully
- Max iterations as a safety limit

## How it flows
```
Chat → AI Agent ⇐ Gemini, ⇐ Memory, ⇐ Calculator, ⇐ Wikipedia, ⇐ get_weather (HTTP), ⇐ get_exchange_rate (HTTP)
```

## Credentials you need
- Google Gemini API key (all tools used here are free and keyless)

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Chat Trigger → **AI Agent**.
2. Attach Gemini + Window Buffer Memory.
3. Attach **Calculator** and **Wikipedia** tools.
4. Attach **HTTP Request Tool**: name `get_weather`, URL with `{lat}` and `{lon}` placeholders, and define both placeholders.
5. Attach a second HTTP tool, `get_exchange_rate`, with a `{base}` placeholder.
6. Write a system prompt that tells the agent *when* to use tools.

## Test it
- "What's 17.5% of 84,999?" should use Calculator.
- "Weather in Bengaluru?" should use get_weather with about 12.97, 77.59.
- "Who founded Infosys?" should use Wikipedia.
- Follow-up: "and in USD?" tests memory and the currency tool.

## Common errors
| Symptom | Fix |
|---|---|
| The agent answers from memory and skips tools | Make the system prompt stricter ("ALWAYS use…") and set a lower temperature. |
| `Too many iterations` | The tool keeps failing. Open the Logs panel to see the tool error. |
| Huge tool responses / token errors | Turn on *Optimize Response* on HTTP tools and pick only the fields you need. |

## Level up (try these next)
- Add a Google Calendar tool ("what's on my calendar tomorrow?").
- Add a Gmail tool, but put an approval step in front of it (L15).

---
[← Back to the learning path](../../README.md)
