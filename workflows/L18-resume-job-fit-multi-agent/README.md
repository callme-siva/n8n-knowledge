<div align="center">

# L18 · Resume ↔ job fit analyser

![level: Multi-agent & production](https://img.shields.io/badge/level-Multi--agent_%26_production-DC2626?style=flat-square) ![domain: Career / HR / recruiting](https://img.shields.io/badge/domain-Career_/_HR_/_recruiting-334155?style=flat-square) ![build time: 35 min](https://img.shields.io/badge/build_time-35_min-0EA5E9?style=flat-square) ![nodes: 11](https://img.shields.io/badge/nodes-11-7C3AED?style=flat-square) ![e2e test: passed · 0 checks](https://img.shields.io/badge/e2e_test-passed_%C2%B7_0_checks-2EA44F?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** Job seekers want to know *"Am I a fit, and what should I prepare?"*. Recruiters want a quick first screen. The same workflow answers both: it extracts the resume text, scores the fit, lists the gaps, drafts likely interview questions and builds a learning plan.

## 💡 Concept first

**📌 Key idea:** Document AI = **extract text first**, then let specialists analyse; the quality of step 1 limits everything after it.

**🧠 Mental model:** Photocopy the CV, then hand copies to four reviewers with different checklists.

**🚫 When *not* to use it:** Don't feed scanned images to a text extractor. Add OCR, or the AI analyses an empty page.

## 🎯 What you'll learn

- **Extract From File** (PDF → text)
- Specialist agents with narrow, focused prompts
- One consolidated HTML email built from 4 outputs
- Privacy: resumes are personal data, so don't log them to public places

## 🏗️ Architecture

**System context:** who and what this workflow talks to, and what crosses each boundary. 🔑 = needs a credential · 🧑 = a human decides.

```mermaid
flowchart LR
  s0(["👤 Person filling the form"]):::person
  core{{"⚙️ n8n workflow<br/><small>11 nodes</small>"}}:::n8n
  s1["✦ Google Gemini 🔑"]:::ai
  s2["📧 Gmail 🔑"]:::saas
  s0 -->|"form submission"| core
  core <-->|"prompt + data → answer"| s1
  core -->|"sends email"| s2
  classDef person fill:#FFF4E5,stroke:#F59E0B,color:#1F2937
  classDef time fill:#E8F7EE,stroke:#2EA44F,color:#1F2937
  classDef saas fill:#EAF3FF,stroke:#2563EB,color:#1F2937
  classDef ai fill:#F1EBFF,stroke:#7C3AED,color:#1F2937
  classDef ext fill:#E6FAF8,stroke:#0D9488,color:#1F2937
  classDef n8n fill:#FFF1F4,stroke:#EA4B71,stroke-width:3px,color:#1F2937
  classDef store fill:#F8FAFC,stroke:#64748B,color:#1F2937
```

<details><summary><b>Node-level flow</b> (every node and branch)</summary>

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

</details>

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

## 📝 Before you run it

No placeholder values. It runs as-is once the credentials are connected.

Nodes that need a credential selected after import: **Gmail**, **Google Gemini Chat Model**.

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Import it and connect the credentials.
2. Open the form, upload your resume, and paste a real JD from LinkedIn or Naukri.
3. Compare the fit score with your own judgement. Then tune the Job Fit prompt: add a scoring rubric (skills 40, experience 30, domain 20, extras 10).

## 🔍 Node-by-node reference

Every node in this workflow and every setting inside it, generated from [`workflow.json`](workflow.json). Click a node to expand it.

<details><summary><b>1. Candidate Submission</b> · <code>n8n Form Trigger</code> v2.6</summary>

> Hosts a web form; each submission starts one execution. Field labels become JSON keys.

| Property | Value |
|---|---|
| `formTitle` | Resume & Job Fit Analysis |
| `formDescription` | Upload your resume and paste one or more job descriptions to receive a personalized ana… |
| `formFields.values` | Candidate Name *, Email *, Resume *, Job Descriptions * |

</details>

<details><summary><b>2. Extract Resume Text</b> · <code>Extract From File</code> v1.1</summary>

> Pulls text or data out of a binary file (PDF, CSV, XLSX…).

| Property | Value |
|---|---|
| `operation` | pdf |
| `binaryPropertyName` | Resume |
| `joinPages` | ✅ on |

</details>

<details><summary><b>3. Resume Analyst</b> · <code>AI Agent</code> v3.1</summary>

> An LLM that can call tools, use memory and loop until it has an answer.

| Property | Value |
|---|---|
| `promptType` | define |
| `text` | `Analyze the following resume. Summarize the candidate's key skills, experience, notable achievements, strengths, and any gaps or weaknesses.  RESUME: {{ $json.text }}` |
| `systemMessage` | You are an expert technical recruiter and resume reviewer. Produce a clear, well-structured analysis using short headings and bullet points. |

</details>

<details><summary><b>4. Model - Analyzer</b> · <code>Google Gemini Chat Model</code> v1</summary>

> The language model plugged into a chain or agent.

| Property | Value |
|---|---|
| `modelName` | models/gemini-2.5-flash |
| `temperature` | 0.2 |

</details>

<details><summary><b>5. Job Fit Analyst</b> · <code>AI Agent</code> v3.1</summary>

> An LLM that can call tools, use memory and loop until it has an answer.

| Property | Value |
|---|---|
| `promptType` | define |
| `text` | `Compare the candidate's resume against the job description(s). For each role, give a fit score out of 100, list matched requirements, missing/weak requirements, and an overall recommendation.  RESUME: {{ $node["Extract Resume Text"].json.text }}  JOB DESCRIPTION(S): {{ $node["Candidate Submission"].json["Job Descriptions"] }}` |
| `systemMessage` | You are an expert hiring manager. Assess how well the candidate matches each job's requirements. Use clear headings per role and bullet points. |

</details>

<details><summary><b>6. Model - Matcher</b> · <code>Google Gemini Chat Model</code> v1</summary>

> The language model plugged into a chain or agent.

| Property | Value |
|---|---|
| `modelName` | models/gemini-2.5-flash |
| `temperature` | 0.2 |

</details>

<details><summary><b>7. Interview Question Generator</b> · <code>AI Agent</code> v3.1</summary>

> An LLM that can call tools, use memory and loop until it has an answer.

| Property | Value |
|---|---|
| `promptType` | define |
| `text` | `Based on the resume and the job description(s), prepare a tailored set of interview questions: technical, behavioral, and role-specific. Group them by category and note what a strong answer should cover.  RESUME: {{ $node["Extract Resume Text"].json.text }}  JOB DESCRIPTION(S): {{ $node["Candidate Submission"].json["Job Descriptions"] }}` |
| `systemMessage` | You are an experienced interviewer. Produce practical, tailored interview questions grouped by category. |

</details>

<details><summary><b>8. Model - Interview</b> · <code>Google Gemini Chat Model</code> v1</summary>

> The language model plugged into a chain or agent.

| Property | Value |
|---|---|
| `modelName` | models/gemini-2.5-flash |
| `temperature` | 0.2 |

</details>

<details><summary><b>9. Learning Plan Builder</b> · <code>AI Agent</code> v3.1</summary>

> An LLM that can call tools, use memory and loop until it has an answer.

| Property | Value |
|---|---|
| `promptType` | define |
| `text` | `Create a personalized learning plan to close the gaps between the candidate's resume and the job description(s). Include prioritized skills to learn, recommended resource types, and a suggested weekly timeline.  RESUME: {{ $node["Extract Resume Text"].json.text }}  JOB DESCRIPTION(S): {{ $node["Candidate Submission"].json["Job Descriptions"] }}` |
| `systemMessage` | You are a career coach. Build an actionable, prioritized learning plan with a realistic timeline. |

</details>

<details><summary><b>10. Model - Learning</b> · <code>Google Gemini Chat Model</code> v1</summary>

> The language model plugged into a chain or agent.

| Property | Value |
|---|---|
| `modelName` | models/gemini-2.5-flash |
| `temperature` | 0.2 |

</details>

<details><summary><b>11. Send Analysis Email</b> · <code>Gmail</code> v2.2</summary>

> Sends, reads or labels email. `sendAndWait` pauses the workflow for a human reply.

| Property | Value |
|---|---|
| `sendTo` | `{{ $node["Candidate Submission"].json.Email }}` |
| `subject` | `Your Resume & Job Fit Analysis, {{ $node["Candidate Submission"].json["Candidate Name"] }}` |
| `message` | `<h2>Hi {{ $node["Candidate Submission"].json["Candidate Name"] }},</h2><p>Here is your personalized resume and job fit analysis.</p><h3>1. Resume Analysis</h3><div style="white-space:pre-wrap">{{ $node["Resume Analyst"].json.output }}</div><h3>2. Job Fit &amp; Comparison</h3><div style="white-space:pre-wrap">{{ $node["Job Fit Analyst"].json.output }}</div><h3>3. Interview Questions</h3><div style="white-space:pre-wrap">{{ $node["Interview Question Generator"].json.output }}</div><h3>4. Personalized Learning Plan</h3><div style="white-space:pre-wrap">{{ $node["Learning Plan Builder"].json.output }}</div><p>Best of luck!</p>` |

</details>

> [!TIP]
> ⚙️ rows come from each node's **Settings** tab, not its Parameters tab. `{{ … }}` values are **expressions** evaluated at run time. See [workflow anatomy](../../docs/workflow-anatomy.md) for what every property means.

## ✅ Test it

> [!TIP]
> **Automated end-to-end test: passed.** 7/7 nodes executed in real n8n (7 credentialed nodes replaced by realistic mocks), 0 behaviour checks. See [tests/](../../tests/README.md).

- [ ] Try the same resume against 2 very different JDs. The scores should differ clearly.

## 🧯 Troubleshooting

Problems specific to this workflow are below. For general ones (expressions, items, triggers, AI), see [common mistakes](../../docs/common-mistakes.md).

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
