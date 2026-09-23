<div align="center">

# L13 · HR policy chatbot with RAG

![level: AI](https://img.shields.io/badge/level-AI-F97316?style=flat-square) ![domain: HR / internal support](https://img.shields.io/badge/domain-HR_/_internal_support-334155?style=flat-square) ![build time: 35 min](https://img.shields.io/badge/build_time-35_min-0EA5E9?style=flat-square) ![nodes: 11](https://img.shields.io/badge/nodes-11-7C3AED?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** Employees keep asking HR the same questions ("How many casual leaves do I get?", "Is my broadband reimbursed?") when the answer is already in a 40-page PDF. RAG lets a chatbot answer from *your* documents, not from what the model remembers from the internet.

## 🎯 What you'll learn

- The RAG idea: **chunk → embed → store → retrieve → answer**
- Embeddings with Gemini (`gemini-embedding-001`)
- Vector store *insert* mode vs *retrieve-as-tool* mode
- AI Agent + tool + memory
- Grounding prompts that stop the model from guessing

## 🏗️ Architecture

```mermaid
flowchart LR
  n0(["Upload Policy PDFs"]):::trigger
  n1[["Store in Vector DB"]]:::ai
  n2("Gemini Embeddings (insert)"):::sub
  n3("PDF Loader"):::sub
  n4("Chunker"):::sub
  n5(["Chat with Employees"]):::trigger
  n6[["Policy Assistant"]]:::ai
  n7("Gemini Chat"):::sub
  n8("Chat Memory"):::sub
  n9("policy_documents"):::sub
  n10("Gemini Embeddings (search)"):::sub
  n0 --> n1
  n2 -.->|embedding| n1
  n3 -.->|document| n1
  n4 -.->|textSplitter| n3
  n5 --> n6
  n7 -.->|languageModel| n6
  n8 -.->|memory| n6
  n9 -.->|tool| n6
  n10 -.->|embedding| n9
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
PART A  Form (PDF upload) → Vector Store insert ⇐ Embeddings, ⇐ Loader ⇐ Chunker
PART B  Chat Trigger → AI Agent ⇐ Gemini, ⇐ Memory, ⇐ Tool: Vector Store (retrieve) ⇐ Embeddings
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Google Gemini API key (used for chat and embeddings) | [docs/credentials.md](../../docs/credentials.md) |

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. **Part A**: Form Trigger with a *File* field (accept `.pdf`).
2. Add **In-Memory Vector Store**, mode *Insert Documents*, memory key `hr_policies`.
3. Attach **Embeddings Google Gemini** + **Default Data Loader** (type *Binary*) + **Recursive Character Text Splitter** (1000 / 150).
4. Open the form, upload a policy PDF, and check how many chunks were inserted.
5. **Part B**: add a **Chat Trigger** → **AI Agent**. Attach Gemini, **Window Buffer Memory**, and a second **In-Memory Vector Store** in *Retrieve documents (as tool)* mode with the **same memory key** and its own embeddings node.
6. Write the strict system prompt (see workflow.json).
7. Click **Open chat** and ask a question.

## ✅ Test it

- [ ] Use the sample policy in [docs/sample-data.md](../../docs/sample-data.md#hr-policy) (save it as a PDF).
- [ ] Ask something that *isn't* in the policy ("What's the CEO's salary?"). It must refuse.
- [ ] Open the agent's execution log to see which chunks were retrieved.

## 🧯 Troubleshooting

<details><summary><b>The agent answers without searching</b></summary>

Make the tool description specific and say "ALWAYS search" in the system prompt.

</details>

<details><summary><b>Nothing found after restarting n8n</b></summary>

In-memory storage is wiped on restart. Re-upload, or move to a persistent vector DB.

</details>

<details><summary><b>Embedding dimension mismatch</b></summary>

Use the *same* embedding model for insert and search.

</details>

## 🚀 Level up

- Swap in Supabase / Qdrant / Pinecone for persistent storage.
- Serve it inside Slack or Teams instead of n8n chat.
- Add a Google Drive trigger so new policies index themselves.

---

<p align="center"><a href="../L12-meeting-transcript-raid-log/README.md">← L12 · Meeting transcript → RAID log</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L14-ai-agent-with-tools/README.md">L14 · Personal assistant agent →</a></p>
