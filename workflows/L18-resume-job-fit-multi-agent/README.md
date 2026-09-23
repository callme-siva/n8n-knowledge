# L18 · Resume ↔ job fit analyser

**Level:** 🔴 Multi-agent & production · **Domain:** Career / HR / recruiting · **Build time:** 35 min

## The real-world problem
Job seekers want to know *"Am I a fit, and what should I prepare?"*. Recruiters want a quick first screen. The same workflow answers both: it extracts the resume text, scores the fit, lists the gaps, drafts likely interview questions and builds a learning plan.

## What you will learn
- **Extract From File** (PDF → text)
- Specialist agents with narrow, focused prompts
- One consolidated HTML email built from 4 outputs
- Privacy: resumes are personal data, so don't log them to public places

## How it flows
```
Form (PDF + JD) → Extract text → Resume Analyst → Job Fit Analyst → Interview Questions → Learning Plan → Gmail
```

## Credentials you need
- Google Gemini API key
- Gmail OAuth2

## Build it step by step
> Import `workflow.json` to see the finished version, **or** build it yourself using these steps (recommended — you learn more).

1. Import it and connect the credentials.
2. Open the form, upload your resume, and paste a real JD from LinkedIn or Naukri.
3. Compare the fit score with your own judgement. Then tune the Job Fit prompt: add a scoring rubric (skills 40, experience 30, domain 20, extras 10).

## Test it
- Try the same resume against 2 very different JDs. The scores should differ clearly.

## Common errors
| Symptom | Fix |
|---|---|
| Empty resume text | Scanned or image PDFs have no text layer. Add OCR, or ask for a text-based PDF. |
| Scores are always about 75 | Add a rubric and examples of low and high scores to the prompt. |

## Level up (try these next)
- Store results in Sheets to build a candidate pipeline.
- Loop over 20 resumes against one JD and rank them (see L20 sub-workflows).

---
[← Back to the learning path](../../README.md)
