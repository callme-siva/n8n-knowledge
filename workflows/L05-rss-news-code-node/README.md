# L05 · Tech news digest with the Code node

**Level:** 🟢 Beginner · **Domain:** Learning / research · **Build time:** 25 min

## The real-world problem
You follow 3 news sites and see the same story three times. This merges the feeds, removes duplicates and sends one clean list.

## What you will learn
- RSS Read node
- **Merge** node with 3 inputs (append mode)
- Code node: filter / map / sort / dedupe / reduce many items into one
- *On Error → Continue*: one broken feed shouldn't kill the run
- An IF guard so you don't get empty emails

## How it flows
```
Schedule ─┬─ RSS Google News ─┐
          ├─ RSS TechCrunch  ─┼─ Merge → Code (filter/dedupe/sort) → IF count>0 → Gmail
          └─ RSS The Verge   ─┘
```

## Credentials you need
- Gmail OAuth2

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Add a Schedule Trigger and 3 **RSS Read** nodes, each connected to the trigger.
2. On each RSS node: Settings → *On Error* → **Continue**.
3. Add **Merge** → *Number of inputs* 3, and wire each feed to its own input.
4. Add a **Code** node (*Run once for all items*) and paste the code. Read it line by line; each `.filter` / `.map` is one idea.
5. Add an **IF** node: `count > 0`.
6. Add Gmail on the true branch.

## Test it
- Run it and open the Code node output. `listText` is prepared for the AI version in L11.
- Replace one feed URL with a broken one. The workflow should still finish.

## Common errors
| Symptom | Fix |
|---|---|
| Merge waits forever or outputs nothing | Every input must be connected. Check the numbered input dots on Merge. |
| All articles filtered out | Some feeds use `pubDate` and not `isoDate`. The code handles both, so check your feed's field names. |

## Level up (try these next)
- Add your own feeds (company blog, Hacker News `https://hnrss.org/frontpage`).
- Continue to **L11** to have Gemini summarise this.

---
[← Back to the learning path](../../README.md)
