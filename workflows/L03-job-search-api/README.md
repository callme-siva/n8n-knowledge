# L03 · Daily job search digest

**Level:** 🟢 Beginner · **Domain:** Career / HR · **Build time:** 20 min

## The real-world problem
Job hunting means checking portals every day. This workflow searches Google Jobs every morning and emails you one clean table of today's postings.

## What you will learn
- HTTP Request with a **predefined credential** (SerpAPI)
- Reading nested API JSON (`jobs_results[].apply_options[0].link`)
- Code node that turns many items into one HTML email
- Optional chaining `?.` so missing fields don't crash the code
- Escaping HTML so a job title can't break your email

## How it flows
```
Schedule → ⚙️ Config → HTTP (SerpAPI google_jobs) → Code (HTML table) → Gmail
```

## Credentials you need
- SerpAPI key: free at serpapi.com. In n8n: Credentials → *SerpAPI*
- Gmail OAuth2

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Sign up at serpapi.com and copy your API key. In n8n, create a **SerpApi** credential.
2. Build the Schedule → Config chain as in L02.
3. Add an **HTTP Request** node: Authentication = *Predefined credential type → SerpApi*; query `engine=google_jobs`, `q`, `location`, `chips=date_posted:today`.
4. Run it and **study the output JSON**. Find `jobs_results`. This is the most important skill with any API.
5. Add a **Code** node that loops over jobs and builds an HTML table (copy it from workflow.json).
6. Add **Gmail** with subject/body = `{{ $json.subject }}` / `{{ $json.html }}`.

## Test it
- Change `query` to your own role and run it manually.
- Set `location` to a city (for example `Bengaluru, Karnataka, India`).

## Common errors
| Symptom | Fix |
|---|---|
| 401 / Invalid API key | Re-create the SerpApi credential. |
| Email says 0 jobs | `date_posted:today` is strict. Remove the `chips` parameter to test. |
| Monthly quota used up | The free tier gives 100 searches a month. A daily run uses about 30. |

## Level up (try these next)
- Save jobs to Google Sheets and skip ones you've already seen (dedupe by `job_id`).
- Add Gemini to score each job against your resume (see L18).

---
[← Back to the learning path](../../README.md)
