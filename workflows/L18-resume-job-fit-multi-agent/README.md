<div align="center">

# L18 · Resume ↔ job fit analyser

![level: Multi-agent & production](https://img.shields.io/badge/level-Multi--agent_%26_production-DC2626?style=flat-square) ![domain: Career / HR / recruiting](https://img.shields.io/badge/domain-Career_/_HR_/_recruiting-334155?style=flat-square) ![build time: 35 min](https://img.shields.io/badge/build_time-35_min-0EA5E9?style=flat-square) ![nodes: 11](https://img.shields.io/badge/nodes-11-7C3AED?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** Job seekers want to know *"Am I a fit, and what should I prepare?"*. Recruiters want a quick first screen. The same workflow answers both: it extracts the resume text, scores the fit, lists the gaps, drafts likely interview questions and builds a learning plan.

## 🎯 What you'll learn

- **Extract From File** (PDF → text)
- Specialist agents with narrow, focused prompts
- One consolidated HTML email built from 4 outputs
- Privacy: resumes are personal data, so don't log them to public places

## 🏗️ Architecture

```mermaid
flowchart TB
  n0(["Candidate Submission"]):::trigger
  n1["Extract Resume Text"]:::data
  n2[["Resume Analyst"]]:::ai
  n3("Model - Analyzer"):::sub
  n4[["Job Fit Analyst"]]:::ai
  n5("Model - Matcher"):::sub
  n6[["Interview Question Generator"]]:::ai
  n7("Model - Interview"):::sub
  n8[["Learning Plan Builder"]]:::ai
  n9("Model - Learning"):::sub
  n10["Send Analysis Email"]:::msg
  n0 --> n1
  n1 --> n2
  n2 --> n4
  n3 -.->|languageModel| n2
  n4 --> n6
  n5 -.->|languageModel| n4
  n6 --> n8
  n7 -.->|languageModel| n6
  n8 --> n10
  n9 -.->|languageModel| n8
  classDef trigger fill:#E8F7EE,stroke:#2EA44F,stroke-width:2px,color:#1F2937
  classDef ai fill:#F1EBFF,stroke:#7C3AED,stroke-width:2px,color:#1F2937
  classDef sub fill:#F7F3FF,stroke:#A78BFA,stroke-width:2px,color:#1F2937
  classDef logic fill:#FFF4E5,stroke:#F59E0B,stroke-width:2px,color:#1F2937
  classDef code fill:#EEF2F7,stroke:#64748B,stroke-width:2px,color:#1F2937
  classDef data fill:#EAF3FF,stroke:#2563EB,stroke-width:2px,color:#1F2937
  classDef http fill:#E6FAF8,stroke:#0D9488,stroke-width:2px,color:#1F2937
  classDef msg fill:#FFEDEF,stroke:#E11D48,stroke-width:2px,color:#1F2937
```

<details><summary>Plain-text flow</summary>

```
Form (PDF + JD) → Extract text → Resume Analyst → Job Fit Analyst → Interview Questions → Learning Plan → Gmail
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Google Gemini API key | [docs/credentials.md](../../docs/credentials.md) |
| Gmail OAuth2 | [docs/credentials.md](../../docs/credentials.md) |

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Import it and connect the credentials.
2. Open the form, upload your resume, and paste a real JD from LinkedIn or Naukri.
3. Compare the fit score with your own judgement. Then tune the Job Fit prompt: add a scoring rubric (skills 40, experience 30, domain 20, extras 10).

## ✅ Test it

- [ ] Try the same resume against 2 very different JDs. The scores should differ clearly.

## 🧯 Troubleshooting

<details><summary><b>Empty resume text</b></summary>

Scanned or image PDFs have no text layer. Add OCR, or ask for a text-based PDF.

</details>

<details><summary><b>Scores are always about 75</b></summary>

Add a rubric and examples of low and high scores to the prompt.

</details>

## 🚀 Level up

- Store results in Sheets to build a candidate pipeline.
- Loop over 20 resumes against one JD and rank them (see L20 sub-workflows).

---

<p align="center"><a href="../L17-complaint-handler-multi-agent/README.md">← L17 · Customer complaint handler</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L19-global-error-handler/README.md">L19 · Global error handler →</a></p>
