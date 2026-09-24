<div align="center">

# L08 · Daily stale Jira stories report

![level: Integrations](https://img.shields.io/badge/level-Integrations-D4A106?style=flat-square) ![domain: Agile / Scrum](https://img.shields.io/badge/domain-Agile_/_Scrum-334155?style=flat-square) ![build time: 20 min](https://img.shields.io/badge/build_time-20_min-0EA5E9?style=flat-square) ![nodes: 5](https://img.shields.io/badge/nodes-5-7C3AED?style=flat-square) [![e2e test: passed · 2 checks](https://img.shields.io/badge/e2e_test-passed_%C2%B7_2_checks-2EA44F?style=flat-square)](https://github.com/callme-siva/n8n-knowledge/actions/workflows/validate.yml)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** Stories sit "In Progress" for days without anyone saying so at stand-up. A Scrum Master wants a list every weekday morning of what's stuck and who owns it, so the stand-up can start with it.

## 💡 Concept first

**📌 Key idea:** Query the tool of record (**JQL**) instead of copying data; send a digest only when it's useful.

**🧠 Mental model:** A morning newspaper printed only with today's stuck stories, delivered before stand-up.

**🚫 When *not* to use it:** Don't email the whole team a list they will ignore. Target the owner, or post where the team already talks.

## 🎯 What you'll learn

- Jira Software node + **JQL** queries
- Cron expression for weekdays only (`0 9 * * 1-5`)
- `alwaysOutputData`: still send the ✅ email when Jira returns nothing
- Grouping and counting with `reduce`
- Conditional styling in HTML (red if more than 7 days)

## 🏗️ Architecture

**System context:** who and what this workflow talks to, and what crosses each boundary. 🔑 = needs a credential · 🧑 = a human decides.

```mermaid
flowchart LR
  s0(["⏰ Schedule"]):::time
  core{{"⚙️ n8n workflow<br/><small>5 nodes</small>"}}:::n8n
  s1["🧭 Jira 🔑"]:::saas
  s2["📧 Gmail 🔑"]:::saas
  s0 -->|"fires"| core
  core <-->|"JQL search"| s1
  core -->|"sends email"| s2
  classDef time fill:#E8F7EE,stroke:#2EA44F,color:#1F2937
  classDef saas fill:#EAF3FF,stroke:#2563EB,color:#1F2937
  classDef n8n fill:#FFF1F4,stroke:#EA4B71,stroke-width:3px,color:#1F2937
```

<details><summary><b>Node-level flow</b> (every node and branch)</summary>

```mermaid
flowchart LR
  n0(["Weekdays 9 AM"]):::trigger
  n1["⚙️ Config"]:::code
  n2["Search Stale Stories"]:::data
  n3["Build Report"]:::code
  n4["Email Scrum Master"]:::msg
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  classDef trigger fill:#E8F7EE,stroke:#2EA44F,stroke-width:2px,color:#1F2937
  classDef code fill:#EEF2F7,stroke:#64748B,stroke-width:2px,color:#1F2937
  classDef data fill:#EAF3FF,stroke:#2563EB,stroke-width:2px,color:#1F2937
  classDef msg fill:#FFEDEF,stroke:#E11D48,stroke-width:2px,color:#1F2937
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| Jira Software Cloud | email + API token from id.atlassian.com → Security → API tokens |
| Gmail OAuth2 | [docs/credentials.md](../../docs/credentials.md) |

## 📝 Before you run it

Replace these placeholder values with your own:

| Node | Field | Placeholder |
|---|---|---|
| ⚙️ Config | `email_to` | `you@example.com` |
| ⚙️ Config | `jira_base_url` | `https://YOUR-SITE.atlassian.net` |

Nodes that need a credential selected after import: **Gmail**, **Jira Software**.

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Create an API token at https://id.atlassian.com/manage-profile/security/api-tokens and add a **Jira SW Cloud API** credential (domain + email + token).
2. Schedule Trigger → *Custom (cron)* → `0 9 * * 1-5`.
3. Config: project_key, stale_days, email_to, jira_base_url.
4. **Jira → Issue → Get many**, Return all, Options → JQL. Test your JQL in Jira's own search first!
5. Node Settings → **Always Output Data** on (so an empty result still continues).
6. Code node builds the report, then Gmail.

## 🔍 Node-by-node reference

Every node in this workflow and every setting inside it, generated from [`workflow.json`](workflow.json). Click a node to expand it.

<details><summary><b>1. Weekdays 9 AM</b> · <code>Schedule Trigger</code> v1.2</summary>

> Starts the workflow on a timer or cron expression. Only fires when the workflow is **active**.

| Property | Value |
|---|---|
| `rule.interval.field` | cronExpression |
| `rule.interval.expression` | 0 9 * * 1-5 |

</details>

<details><summary><b>2. ⚙️ Config</b> · <code>Edit Fields (Set)</code> v3.4</summary>

> Creates, renames or overwrites fields without code.

| Property | Value |
|---|---|
| `project_key` | SCRUM |
| `stale_days` | 3 |
| `email_to` | you@example.com |
| `jira_base_url` | https://YOUR-SITE.atlassian.net |

</details>

<details><summary><b>3. Search Stale Stories</b> · <code>Jira Software</code> v1</summary>

> Creates, searches or updates Jira issues.

| Property | Value |
|---|---|
| `operation` | getAll |
| `returnAll` | ✅ on |
| `jql` | `project = {{ $json.project_key }} AND statusCategory = "In Progress" AND updated <= -{{…` |
| `fields` | summary,status,assignee,updated,priority |
| `⚙️ Retry on fail` | ✅ on |
| `⚙️ Max tries` | 3 |
| `⚙️ Wait between tries (ms)` | 3000 |
| `⚙️ Always output data` | ✅ on |

</details>

<details><summary><b>4. Build Report</b> · <code>Code</code> v2</summary>

> Runs JavaScript. *Run once for all items* sees every item; *for each item* sees one at a time.

| Property | Value |
|---|---|
| `jsCode` | (JavaScript, 13 lines, shown below) |

**Code:**

```javascript
const cfg = $('⚙️ Config').first().json;
const issues = $input.all().map(i => i.json).filter(j => j && j.key);
const days = d => Math.floor((Date.now() - Date.parse(d)) / 86400000);
const rows = issues.map(i => {
  const f = i.fields || {};
  return { key: i.key, summary: f.summary, assignee: f.assignee?.displayName || 'Unassigned', status: f.status?.name, days: days(f.updated) };
}).sort((a, b) => b.days - a.days);
const tr = rows.map(r => `<tr><td><a href="${cfg.jira_base_url}/browse/${r.key}">${r.key}</a></td><td>${r.summary}</td><td>${r.assignee}</td><td>${r.status}</td><td style="color:${r.days > 7 ? 'red' : 'inherit'}">${r.days}</td></tr>`).join('');
const byPerson = rows.reduce((m, r) => (m[r.assignee] = (m[r.assignee] || 0) + 1, m), {});
const summary = Object.entries(byPerson).map(([p, n]) => `${p}: ${n}`).join(' · ');
return [{ json: { count: rows.length,
  subject: rows.length ? `⚠️ ${rows.length} stale stories in ${cfg.project_key}` : `✅ No stale stories in ${cfg.project_key}`,
  html: rows.length ? `<p>${summary}</p><table border=1 cellpadding=6 style="border-collapse:collapse"><tr><th>Key</th><th>Summary</th><th>Assignee</th><th>Status</th><th>Days idle</th></tr>${tr}</table>` : '<p>Everything moved in the last few days. 🎉</p>' } }];
```

</details>

<details><summary><b>5. Email Scrum Master</b> · <code>Gmail</code> v2.1</summary>

> Sends, reads or labels email. `sendAndWait` pauses the workflow for a human reply.

| Property | Value |
|---|---|
| `sendTo` | `{{ $('⚙️ Config').item.json.email_to }}` |
| `subject` | `{{ $json.subject }}` |
| `emailType` | html |
| `message` | `{{ $json.html }}` |
| `appendAttribution` | off |
| `⚙️ Retry on fail` | ✅ on |
| `⚙️ Max tries` | 3 |
| `⚙️ Wait between tries (ms)` | 3000 |

</details>

> [!TIP]
> ⚙️ rows come from each node's **Settings** tab, not its Parameters tab. `{{ … }}` values are **expressions** evaluated at run time. See [workflow anatomy](../../docs/workflow-anatomy.md) for what every property means.

## ✅ Test it

> [!TIP]
> **Automated end-to-end test: passed.** 5/5 nodes executed in real n8n (2 credentialed or AI nodes replaced by fixtures, so AI output itself isn't tested), 2 behaviour checks. See [tests/](../../tests/README.md).

- [ ] Set `stale_days` to 0 so you see every in-progress story.
- [ ] Use a project key that doesn't exist. You should get a clear Jira error.

## 🧯 Troubleshooting

Problems specific to this workflow are below. For general ones (expressions, items, triggers, AI), see [common mistakes](../../docs/common-mistakes.md).

<details><summary><b>JQL: field 'statusCategory' does not exist</b></summary>

On older Jira Server, use `status = "In Progress"`.

</details>

<details><summary><b>No email when there are no stale stories</b></summary>

Turn on *Always Output Data* on the Jira node.

</details>

## 🏋️ Practice

Try each challenge **before** opening the hint. Solutions show the exact expressions and code.

**⭐ Challenge 1:** Only include **High/Highest** priority stale stories.

<details><summary>💡 Hint</summary>

Fix it in JQL, not in code, so Jira does the filtering.

</details>
<details><summary>✅ Solution</summary>

Append to the JQL: `AND priority in (High, Highest)`. Filtering at the source means less data, faster runs and an easier workflow.

</details>

**⭐⭐ Challenge 2:** DM each assignee their own list instead of one team email.

<details><summary>💡 Hint</summary>

Group by assignee, then one item per person → Slack/email node runs per item.

</details>
<details><summary>✅ Solution</summary>

Replace the report Code with:
```javascript
const by = {};
for (const i of $input.all().map(x => x.json).filter(j => j.key)) {
  const who = i.fields.assignee?.emailAddress || 'unassigned@example.com';
  (by[who] ??= []).push(`${i.key} ${i.fields.summary}`);
}
return Object.entries(by).map(([email, list]) => ({ json: { email, text: list.join('\n') } }));
```
Send to `{{ $json.email }}`.

</details>

## 🚀 Ideas to extend it

- Post it to the team Slack/Teams channel instead of email.
- Also comment on each stale issue: "Any blockers? 🙂".

---

<p align="center"><a href="../L07-lead-capture-sheets/README.md">← L07 · Lead capture form → Google Sheets + welcome email</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../L09-webhook-expense-api/README.md">L09 · Expense logger API →</a></p>
