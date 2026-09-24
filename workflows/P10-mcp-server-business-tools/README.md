<div align="center">

# P10 · MCP server for company tools

![level: Real-world project](https://img.shields.io/badge/level-Real--world_project-7C3AED?style=flat-square) ![domain: AI platform / internal tools](https://img.shields.io/badge/domain-AI_platform_/_internal_tools-334155?style=flat-square) ![build time: 30 min](https://img.shields.io/badge/build_time-30_min-0EA5E9?style=flat-square) ![nodes: 4](https://img.shields.io/badge/nodes-4-7C3AED?style=flat-square) [![e2e test: structure only](https://img.shields.io/badge/e2e_test-structure_only-64748B?style=flat-square)](https://github.com/callme-siva/n8n-knowledge/actions/workflows/validate.yml)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** The **Model Context Protocol (MCP)** is how AI assistants (Claude, ChatGPT, Cursor, IDE agents) call external tools. Every company now wants its assistants to answer "what plan is this customer on?" or "raise a ticket" safely. With n8n's **MCP Server Trigger**, any workflow becomes a governed tool: authenticated, logged in Executions, and built by the ops team without a backend developer.

## 💡 Concept first

**📌 Key idea:** **MCP** lets AI assistants call your workflows as tools: authenticated, logged, and governed by you.

**🧠 Mental model:** A staff-only door with a keycard reader: assistants can come in, but only to the rooms you allow.

**🚫 When *not* to use it:** Don't expose write actions (refunds, deletes) as MCP tools without an approval step.

## 🎯 What you'll learn

- **MCP Server Trigger** with bearer authentication
- Sub-workflows as tools (**Call n8n Workflow tool**) with `$fromAI()` parameters
- Writing tool descriptions that AI clients choose correctly
- Governance: auth, least-privilege tools, and read-only by default

## 🏗️ Architecture

**System context:** who and what this workflow talks to, and what crosses each boundary. 🔑 = needs a credential · 🧑 = a human decides.

```mermaid
flowchart LR
  s0(["🤖 AI assistant (MCP client)"]):::ai
  core{{"⚙️ n8n workflow<br/><small>4 nodes</small>"}}:::n8n
  s1["↗ Sub-workflow"]:::time
  s2["🌐 open.er-api.com"]:::ext
  s0 -->|"tool calls"| core
  core -->|"calls with inputs"| s1
  core <-->|"agent tool call"| s2
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
flowchart LR
  n0(["MCP Server Trigger"]):::trigger
  n1("lookup_customer"):::sub
  n2("get_exchange_rate"):::sub
  n3("calculator"):::sub
  n1 -.->|tool| n0
  n2 -.->|tool| n0
  n3 -.->|tool| n0
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
MCP client (Claude / Cursor / ChatGPT) ⇄ MCP Server Trigger /mcp/business-tools
    ⇐ lookup_customer → sub-workflow P10a → Sheets
    ⇐ get_exchange_rate → HTTP
    ⇐ calculator
```

</details>

## ⚖️ Design decisions & trade-offs

Why it's built this way, and what it costs.

| Decision | Why | Trade-off / alternative |
|---|---|---|
| Expose tools through the **MCP Server Trigger** | One governed endpoint works with Claude, ChatGPT, Cursor and IDE agents | Clients must support HTTP MCP; the workflow must be active |
| Tools as sub-workflows with `$fromAI()` parameters | Each tool is testable on its own and reusable in normal workflows | More workflows to manage (naming and IDs matter) |
| Bearer auth + read-only tools first | Least privilege: assistants can look things up but not change data | Write actions need an approval pattern before exposure |

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Bearer auth credential (make a long random token) | [docs/credentials.md](../../docs/credentials.md) |
| Google Sheets OAuth2 (for P10a) | [docs/credentials.md](../../docs/credentials.md) |

## 📝 Before you run it

Replace these placeholder values with your own:

| Node | Field | Placeholder |
|---|---|---|
| lookup_customer | `workflowId` | `REPLACE_WITH_P10a_WORKFLOW_ID` |

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Import **P10a** first, save it, and copy its ID into *lookup_customer*.
2. Create the `Customers` tab with a few rows (use the sample leads).
3. In the MCP Server Trigger, create a **Bearer Auth** credential with a long random token.
4. **Activate** P10 and copy the *Production URL*.
5. Add it to your MCP client. Claude Code: `claude mcp add --transport http business-tools <URL> --header "Authorization: Bearer <token>"`.

## 🔍 Node-by-node reference

Every node in this workflow and every setting inside it, generated from [`workflow.json`](workflow.json). Click a node to expand it.

<details><summary><b>1. MCP Server Trigger</b> · <code>mcpTrigger</code> v2.1</summary>



| Property | Value |
|---|---|
| `authentication` | bearerAuth |
| `path` | business-tools |
| `instructions` | Company tools. Use lookup_customer for any question about a customer's plan, billing st… |

</details>

<details><summary><b>2. lookup_customer</b> · <code>toolWorkflow</code> v2.2</summary>



| Property | Value |
|---|---|
| `description` | Look up a customer by email. Returns plan, MRR, status and last ticket, or found=false. |
| `source` | database |
| `workflowId` | REPLACE_WITH_P10a_WORKFLOW_ID |
| `workflowInputs.mappingMode` | defineBelow |
| `workflowInputs.email` | `{{ $fromAI('email', 'Customer email address', 'string') }}` |
| `workflowInputs.schema.displayName` | email |
| `workflowInputs.schema.type` | string |
| `workflowInputs.schema.required` | off |
| `workflowInputs.schema.display` | ✅ on |
| `workflowInputs.schema.canBeUsedToMatch` | ✅ on |
| `workflowInputs.schema.defaultMatch` | off |
| `workflowInputs.schema.removed` | off |

</details>

<details><summary><b>3. get_exchange_rate</b> · <code>HTTP Request Tool</code> v1.1</summary>

> Lets an agent call an API. `{placeholders}` in the URL are filled in by the model.

| Property | Value |
|---|---|
| `toolDescription` | Latest exchange rates for a base currency (e.g. USD). Returns a map of currency → rate. |
| `url` | https://open.er-api.com/v6/latest/{base} |
| `placeholderDefinitions.name` | base |
| `placeholderDefinitions.description` | 3-letter ISO currency code |
| `placeholderDefinitions.type` | string |
| `optimizeResponse` | ✅ on |
| `dataField` | rates |
| `fieldsToInclude` | all |

</details>

<details><summary><b>4. calculator</b> · <code>Calculator Tool</code> v1</summary>

> Lets an agent do exact arithmetic.

*No settings. This node works with its defaults.*

</details>

> [!TIP]
> ⚙️ rows come from each node's **Settings** tab, not its Parameters tab. `{{ … }}` values are **expressions** evaluated at run time. See [workflow anatomy](../../docs/workflow-anatomy.md) for what every property means.

## ✅ Test it

- [ ] In your AI client: *"What plan is asha@finlytics.example.com on, and what's their MRR in USD?"* It should call lookup_customer, then get_exchange_rate and calculator.
- [ ] Check n8n **Executions**: each tool call is logged.

## 🧯 Troubleshooting

Problems specific to this workflow are below. For general ones (expressions, items, triggers, AI), see [common mistakes](../../docs/common-mistakes.md).

<details><summary><b>Client can't connect</b></summary>

The workflow must be active, and your client needs the **production** URL over HTTPS.

</details>

<details><summary><b>401 Unauthorized</b></summary>

The bearer token in the client must match the credential exactly.

</details>

## 🏋️ Practice

Try each challenge **before** opening the hint. Solutions show the exact expressions and code.

**⭐ Challenge 1:** Add a **`list_open_tickets`** read-only tool.

<details><summary>💡 Hint</summary>

Any sub-workflow can become a tool.

</details>
<details><summary>✅ Solution</summary>

Create a sub-workflow: Execute Workflow Trigger (`email`) → Jira *Get many* (`reporter = email AND statusCategory != Done`) → Set a compact list. Add a **Call n8n Workflow** tool to P10 with a clear description.

</details>

**⭐⭐ Challenge 2:** Add a **write** tool (`create_ticket`) that requires human approval.

<details><summary>💡 Hint</summary>

Tools can pause for approval, like any workflow.

</details>
<details><summary>✅ Solution</summary>

Sub-workflow: inputs (summary, customer_email) → Slack **Send and Wait** to the support lead → IF approved → Jira create → return `{created: key}`; else return `{created: false, reason: 'declined'}`. The AI client gets an honest answer either way.

</details>

## 🚀 Ideas to extend it

- Add a `create_ticket` tool that needs human approval (L15 pattern).
- Separate read-only and write MCP servers with different tokens.
- Log every tool call to a sheet for audit.

---

<p align="center"><a href="../P09-deep-research-agent/README.md">← P09 · Deep research agent</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../P11-pii-safe-ai-gateway/README.md">P11 · PII-safe AI gateway →</a></p>
