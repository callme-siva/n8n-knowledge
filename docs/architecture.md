<div align="center">

# 🏗️ Architecture guide

**How n8n works under the hood, and the design patterns used across all 43 workflows.**

</div>

> [!NOTE]
> Every diagram here uses Mermaid, so GitHub draws it for you. Each lesson README also has its own architecture diagram, generated from its `workflow.json`.

**Contents:** [1. n8n platform](#1-the-n8n-platform) · [2. Anatomy of a workflow](#2-anatomy-of-a-workflow) · [3. AI building blocks](#3-ai-building-blocks) · [4. RAG](#4-rag-retrieval-augmented-generation) · [5. Multi-agent patterns](#5-multi-agent-patterns) · [6. Human in the loop](#6-human-in-the-loop) · [7. Reliability](#7-reliability-and-error-handling) · [8. Production deployment](#8-production-deployment) · [9. Pattern index](#9-pattern--lesson-index)

---

## 1. The n8n platform

```mermaid
flowchart LR
  subgraph Triggers["⚡ Triggers"]
    T1([Schedule / Cron])
    T2([Webhook / Form])
    T3([App events<br/>Gmail, Jira…])
    T4([Chat])
    T5([Error Trigger])
  end
  subgraph Engine["⚙️ n8n engine"]
    E1[Workflow executor]
    E2[(Credentials<br/>encrypted)]
    E3[(Executions log<br/>SQLite / Postgres)]
    E4[Task runner<br/>Code node sandbox]
  end
  subgraph Out["🌐 The outside world"]
    O1[SaaS apps<br/>Gmail · Sheets · Jira]
    O2[Any REST / GraphQL API]
    O3[LLMs<br/>Gemini · OpenAI · Ollama]
    O4[Vector DBs]
  end
  Triggers --> E1
  E1 <--> E2
  E1 --> E3
  E1 <--> E4
  E1 <--> Out
  classDef t fill:#E8F7EE,stroke:#2EA44F,color:#1F2937
  classDef e fill:#F1EBFF,stroke:#7C3AED,color:#1F2937
  classDef o fill:#EAF3FF,stroke:#2563EB,color:#1F2937
  class T1,T2,T3,T4,T5 t
  class E1,E2,E3,E4 e
  class O1,O2,O3,O4 o
```

| Part | What it does | Where you meet it |
|---|---|---|
| **Trigger** | Starts an execution: time, HTTP call, form, app event, chat, another workflow's error | Every lesson |
| **Executor** | Runs nodes in order and passes **items** (JSON + optional binary) between them | L01 |
| **Credentials store** | Encrypted secrets. Workflows only reference them by name, so exported JSON is safe to share | L02+ |
| **Executions log** | Every run with the input and output of every node, which is how you debug | L19 |
| **Task runner** | Isolated sandbox for Code nodes | L05 |

---

## 2. Anatomy of a workflow

```mermaid
flowchart LR
  A([Trigger]) --> B["⚙️ Config<br/>(Set node)"] --> C[Fetch data<br/>HTTP / app node] --> D{Guard<br/>IF: valid & non-empty?}
  D -->|true| E[Transform<br/>Code / Set] --> F[Act<br/>email · sheet · ticket]
  D -->|false| G[Stop and Error<br/>or No-op]
  classDef t fill:#E8F7EE,stroke:#2EA44F,color:#1F2937
  classDef c fill:#EEF2F7,stroke:#64748B,color:#1F2937
  classDef l fill:#FFF4E5,stroke:#F59E0B,color:#1F2937
  classDef a fill:#FFEDEF,stroke:#E11D48,color:#1F2937
  class A t
  class B,C,E c
  class D,G l
  class F a
```

This **Trigger → Config → Fetch → Guard → Transform → Act** shape appears in almost every lesson.

- **Config node first.** Every setting (email, thresholds, IDs) lives in one Set node. Change it once, and nobody has to hunt through ten nodes.
- **Guard before acting.** Check that the API succeeded and that there's something to send (L04, L05).
- **Items are lists.** Most nodes run once per item. The Code node can turn *many → one* (a digest) or *one → many* (one item per PDF, L06).

---

## 3. AI building blocks

n8n's AI nodes are a **root node** with **sub-nodes** plugged in underneath. The dashed lines on the canvas are these connections.

```mermaid
flowchart TB
  IN([Input: chat / form / text]) --> ROOT
  subgraph ROOT_BOX[" "]
    ROOT[["Root node<br/>Basic LLM Chain or AI Agent"]]
  end
  M("🧠 Chat model<br/>Gemini") -.->|ai_languageModel| ROOT
  P("{ } Output parser<br/>JSON schema") -.->|ai_outputParser| ROOT
  MEM("💾 Memory<br/>last N messages") -.->|ai_memory| ROOT
  T1("🛠 Tool: HTTP") -.->|ai_tool| ROOT
  T2("🛠 Tool: Calculator") -.->|ai_tool| ROOT
  T3("🛠 Tool: Vector store") -.->|ai_tool| ROOT
  ROOT --> OUT[Next node]
  classDef r fill:#F1EBFF,stroke:#7C3AED,color:#1F2937
  classDef s fill:#F7F3FF,stroke:#A78BFA,color:#1F2937
  class ROOT r
  class M,P,MEM,T1,T2,T3 s
```

| Choose | When | Lessons |
|---|---|---|
| **Basic LLM Chain** | One prompt in, one answer out. Predictable and cheap | L11, L12, L15, L22 |
| **LLM Chain + Output Parser** | You need **rows, fields or decisions**, not prose | L12, L15, L22 |
| **AI Agent + tools** | The model must *decide* what to look up or calculate | L13, L14, L17 |
| **Agent + memory** | Multi-turn chat | L13, L14 |

> [!TIP]
> Start with a chain. Move to an agent only when the model needs to choose actions. Agents are slower, cost more and are harder to test.

---

## 4. RAG (Retrieval-Augmented Generation)

Used in **L13**. Two flows share one vector store.

```mermaid
flowchart LR
  subgraph Ingest["📥 Ingest (once per document)"]
    direction LR
    D([PDF upload]) --> L[Loader] --> S[Chunker<br/>1000 chars / 150 overlap] --> EM1[Embeddings] --> VS[(Vector store)]
  end
  subgraph Query["💬 Query (every question)"]
    direction LR
    Q([Question]) --> AG[[AI Agent]]
    AG -->|search tool| EM2[Embeddings] --> VS
    VS -->|top-4 chunks| AG
    AG --> A([Grounded answer<br/>+ policy name])
  end
  classDef t fill:#E8F7EE,stroke:#2EA44F,color:#1F2937
  classDef s fill:#F7F3FF,stroke:#A78BFA,color:#1F2937
  classDef d fill:#EAF3FF,stroke:#2563EB,color:#1F2937
  class D,Q,A t
  class L,S,EM1,EM2,AG s
  class VS d
```

**Rules that make RAG trustworthy:**
1. Use the **same embedding model** for ingest and query.
2. The system prompt says *"answer only from the tool; otherwise say you don't know."*
3. Chunk overlap stops answers being cut in half at chunk boundaries.
4. In-memory storage is for learning. For production, switch to Postgres/pgvector, Qdrant, Pinecone or Supabase.

---

## 5. Multi-agent patterns

### Sequential specialists (L16, L17, L18)
```mermaid
flowchart LR
  I([Input]) --> A1[[Agent 1<br/>Understand]] --> A2[[Agent 2<br/>Investigate]] --> A3[[Agent 3<br/>Decide]] --> A4[[Coordinator<br/>Write final]] --> O([Output])
  A1 -. context .-> A3
  A1 -. context .-> A4
  A2 -. context .-> A4
  classDef r fill:#F1EBFF,stroke:#7C3AED,color:#1F2937
  class A1,A2,A3,A4 r
```
Each agent has a **narrow prompt** and a **strict JSON schema**. Later agents read all earlier outputs with `$('Agent name').item.json.output`.

### Self-healing output (L17)
```mermaid
flowchart LR
  AG[[Agent]] --> P{Schema valid?}
  P -->|yes| N[Next step]
  P -->|no| F("Fix model<br/>repairs the JSON") --> P
  classDef r fill:#F1EBFF,stroke:#7C3AED,color:#1F2937
  classDef l fill:#FFF4E5,stroke:#F59E0B,color:#1F2937
  class AG,F r
  class P l
```

> [!TIP]
> **Do the maths in code, the judgement in the LLM.** L16 computes sprint metrics in a Code node *before* any agent sees them. That's cheaper and avoids arithmetic mistakes.

---

## 6. Human in the loop

Used in **L15**. The AI proposes, a human decides, and the execution **pauses** until they respond.

```mermaid
sequenceDiagram
  autonumber
  participant F as Form
  participant N as n8n
  participant G as Gemini
  participant SM as Scrum Master
  participant J as Jira
  F->>N: Retro feedback submitted
  N->>G: Analyse + propose action items (JSON)
  G-->>N: 3 action items
  N->>SM: Email with Approve / Decline buttons
  Note over N: Execution waits (max 2 days)
  SM-->>N: Approve
  N->>J: Create 3 tasks
```

Use this whenever AI output **leaves your organisation** (customer emails, L17) or **creates work for people** (tickets, L15).

---

## 7. Reliability and error handling

```mermaid
flowchart TB
  subgraph Node["Per node"]
    R[Retry on Fail<br/>3 tries · 5 s]
    C[On Error → Continue<br/>non-critical steps]
  end
  subgraph Flow["Per workflow"]
    S[Stop and Error<br/>fail loudly on bad data]
    I[Idempotency<br/>mark as read · dedupe keys]
  end
  subgraph Global["Whole instance"]
    E([Error Trigger workflow · L19]) --> A[Email / Slack alert<br/>+ hint] & LG[(Error log sheet)]
  end
  Node --> Flow --> Global
```

| Layer | Tool | Lesson |
|---|---|---|
| Flaky API | Retry on Fail | L02, L03, L06 |
| One bad input among many | On Error → Continue | L05 (RSS feeds) |
| Data you must not trust | IF guard + Stop and Error | L04 |
| Never process twice | Mark as read / static-data state | L06, L21 |
| Know when *anything* fails | Global error workflow | L19 |
| Don't spam alerts | Alert only when state changes | L21 |

---

## 8. Production deployment

```mermaid
flowchart LR
  U([Users / webhooks]) -->|HTTPS| RP[Reverse proxy<br/>Caddy / Nginx / Cloudflare]
  RP --> M[n8n main<br/>editor + webhooks]
  M --> Q[(Redis queue)]
  Q --> W1[Worker 1] & W2[Worker 2]
  M & W1 & W2 --> PG[(PostgreSQL)]
  M -.-> B[(Nightly backup<br/>DB + encryption key)]
  classDef d fill:#EAF3FF,stroke:#2563EB,color:#1F2937
  class PG,Q,B d
```

| Stage | Setup |
|---|---|
| Learning | `npx n8n` on a laptop, SQLite |
| Team (under 5k runs/day) | Docker on a small VPS + Postgres + HTTPS proxy |
| Scale | **Queue mode**: main + Redis + N workers |

**Checklist:** set `WEBHOOK_URL` · `GENERIC_TIMEZONE` · back up `N8N_ENCRYPTION_KEY` (without it your credentials can't be decrypted) · use Postgres, not SQLite · set an error workflow on everything · prune old executions (`EXECUTIONS_DATA_MAX_AGE`).

---

## 9. Pattern → lesson index

| Pattern | Lessons |
|---|---|
| Config node | L02, L03, L04, L08 |
| Many → one digest | L03, L05, L08, L11 |
| One → many split | L06, L12, L15 |
| Branching (IF / Switch) | L04, L05, L09, L15, L22 |
| Your own API (Webhook + Respond) | L09 |
| Structured AI output | L12, L15, L17, L22 |
| RAG | L13 |
| Tools agent | L14 |
| Human approval | L15 |
| Multi-agent | L16, L17, L18 |
| Error workflow | L19 |
| Sub-workflows | L20 |
| Stateful monitoring | L21 |
| Long waits between steps (Wait node) | P04 |
| Batches + checkpoints + resume | P05 |
| Multi-level approval with timeouts | P06, P01 |
| Fan-out / fan-in (Merge) | P07, P12 |
| Change detection with hashes | P08 |
| Dedupe across executions | Q08, P01, P03 |
| Research agent (search + read + cite) | P09 |
| MCP server (tools for AI assistants) | P10 |
| PII redaction + AI gateway | P11 |
| Text Classifier / Information Extractor | Q07, P01, P02, P05 |

<p align="center"><a href="../README.md">← Back to the learning path</a></p>
