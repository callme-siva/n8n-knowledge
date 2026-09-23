<div align="center">

# Q04 · Stale pull-request reminder

![level: Quick win](https://img.shields.io/badge/level-Quick_win-0EA5E9?style=flat-square) ![domain: Engineering / DevOps](https://img.shields.io/badge/domain-Engineering_/_DevOps-334155?style=flat-square) ![build time: 15 min](https://img.shields.io/badge/build_time-15_min-0EA5E9?style=flat-square) ![nodes: 6](https://img.shields.io/badge/nodes-6-7C3AED?style=flat-square) ![e2e test: passed · 1 checks](https://img.shields.io/badge/e2e_test-passed_%C2%B7_1_checks-2EA44F?style=flat-square)

<img src="canvas.svg" alt="Workflow canvas snapshot" width="100%">

</div>

> [!NOTE]
> **The real-world problem.** Code review is the most common hidden bottleneck in software teams. PRs sit for days and nobody notices until the sprint ends. One daily nudge in the team channel with the owner and reviewers named cuts review time dramatically.

## 💡 Concept first

**📌 Key idea:** Surface **stuck work** where the team already is, with names, so it gets unblocked.

**🧠 Mental model:** A polite colleague who walks the floor at 10 AM asking "who's waiting on a review?".

**🚫 When *not* to use it:** Don't nudge on drafts or weekends. Filter the noise, or people mute the channel.

## 🎯 What you'll learn

- GitHub REST API with a **predefined credential**
- Filtering by age and draft status
- Slack message formatting (`<url|text>` links, `*bold*`)
- Only posting when there's something to say

## 🏗️ Architecture

**System context:** who and what this workflow talks to, and what crosses each boundary. 🔑 = needs a credential · 🧑 = a human decides.

```mermaid
flowchart LR
  s0(["⏰ Schedule"]):::time
  core{{"⚙️ n8n workflow<br/><small>6 nodes</small>"}}:::n8n
  s1["🌐 api.github.com 🔑"]:::ext
  s2["💬 Slack 🔑"]:::saas
  s0 -->|"fires"| core
  core <-->|"HTTPS request"| s1
  core -->|"posts messages"| s2
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
  n0(["Weekdays 10:00"]):::trigger
  n1["⚙️ Config"]:::code
  n2["Open PRs"]:::http
  n3["Find Stale"]:::code
  n4{"Any Stale?"}:::logic
  n5["Post to Slack"]:::msg
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  n4 --> n5
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
Schedule → Config → HTTP GET /repos/{repo}/pulls → Code (stale filter) → IF count>0 → Slack
```

</details>

## 🔑 Credentials

| You need | Where to get it |
|---|---|
| GitHub API token (read access to the repo) | [docs/credentials.md](../../docs/credentials.md) |
| Slack app with `chat:write` scope | [docs/credentials.md](../../docs/credentials.md) |

## 📝 Before you run it

No placeholder values. It runs as-is once the credentials are connected.

Nodes that need a credential selected after import: **HTTP Request**.

## 🛠️ Build it step by step

> [!TIP]
> In a hurry? Import [`workflow.json`](workflow.json) (copy → paste on the n8n canvas). Learning? Build it yourself using the steps below, then compare.

1. Create a GitHub credential (classic PAT with `repo`, or a fine-grained token with *Pull requests: read*).
2. Create a Slack app at api.slack.com → OAuth scopes `chat:write` → install → copy the Bot token into a *Slack API* credential. Invite the bot to the channel.
3. Set repo, stale_days and channel in Config.
4. Run it.

## 🔍 Node-by-node reference

Every node in this workflow and every setting inside it, generated from [`workflow.json`](workflow.json). Click a node to expand it.

<details><summary><b>1. Weekdays 10:00</b> · <code>Schedule Trigger</code> v1.2</summary>

> Starts the workflow on a timer or cron expression. Only fires when the workflow is **active**.

| Property | Value |
|---|---|
| `rule.interval.field` | cronExpression |
| `rule.interval.expression` | 0 10 * * 1-5 |

</details>

<details><summary><b>2. ⚙️ Config</b> · <code>Edit Fields (Set)</code> v3.4</summary>

> Creates, renames or overwrites fields without code.

| Property | Value |
|---|---|
| `repo` | n8n-io/n8n |
| `stale_days` | 2 |
| `slack_channel` | #dev |

</details>

<details><summary><b>3. Open PRs</b> · <code>HTTP Request</code> v4.2</summary>

> Calls any REST API. Use it whenever there's no dedicated node.

| Property | Value |
|---|---|
| `url` | `https://api.github.com/repos/{{ $json.repo }}/pulls` |
| `authentication` | predefinedCredentialType |
| `nodeCredentialType` | githubApi |
| `sendQuery` | ✅ on |
| `queryParameters.state` | open |
| `queryParameters.per_page` | 100 |
| `queryParameters.sort` | updated |
| `queryParameters.direction` | asc |
| `⚙️ Retry on fail` | ✅ on |

</details>

<details><summary><b>4. Find Stale</b> · <code>Code</code> v2</summary>

> Runs JavaScript. *Run once for all items* sees every item; *for each item* sees one at a time.

| Property | Value |
|---|---|
| `jsCode` | (JavaScript, 5 lines, shown below) |

**Code:**

```javascript
const cfg = $('⚙️ Config').first().json;
const days = d => Math.floor((Date.now() - Date.parse(d)) / 86400000);
const prs = $input.all().map(i => i.json).filter(p => p.number && !p.draft && days(p.updated_at) >= cfg.stale_days);
const lines = prs.map(p => `• <${p.html_url}|#${p.number} ${p.title}> by *${p.user.login}* · ${days(p.updated_at)}d idle · reviewers: ${(p.requested_reviewers || []).map(r => '@' + r.login).join(', ') || '_none assigned_'}`);
return [{ json: { count: prs.length, text: `:hourglass: *${prs.length} PRs waiting ${cfg.stale_days}+ days in ${cfg.repo}*\n${lines.join('\n')}` } }];
```

</details>

<details><summary><b>5. Any Stale?</b> · <code>If</code> v2.2</summary>

> Splits items into a **true** and a **false** branch.

| Property | Value |
|---|---|
| `condition` | `{{ $json.count }} > 0` |

</details>

<details><summary><b>6. Post to Slack</b> · <code>slack</code> v2.3</summary>



| Property | Value |
|---|---|
| `select` | channel |
| `channelId` | `{{ $('⚙️ Config').item.json.slack_channel }}` |
| `text` | `{{ $json.text }}` |

</details>

> [!TIP]
> ⚙️ rows come from each node's **Settings** tab, not its Parameters tab. `{{ … }}` values are **expressions** evaluated at run time. See [workflow anatomy](../../docs/workflow-anatomy.md) for what every property means.

## ✅ Test it

> [!TIP]
> **Automated end-to-end test: passed.** 6/6 nodes executed in real n8n (2 credentialed nodes replaced by realistic mocks), 1 behaviour checks. See [tests/](../../tests/README.md).

- [ ] Point it at a busy public repo (the default `n8n-io/n8n`) with `stale_days = 1`. You should see a list.

## 🧯 Troubleshooting

Problems specific to this workflow are below. For general ones (expressions, items, triggers, AI), see [common mistakes](../../docs/common-mistakes.md).

<details><summary><b>not_in_channel</b></summary>

Invite the bot: `/invite @your-bot` in the channel.

</details>

<details><summary><b>Only 100 PRs</b></summary>

Add pagination (HTTP node → Options → Pagination) for very large repos.

</details>

## 🚀 Level up

- DM each reviewer instead of posting in the channel.
- Add CI status per PR from the `/commits/{sha}/status` endpoint.

---

<p align="center"><a href="../Q03-telegram-capture-bot/README.md">← Q03 · Telegram quick-capture bot</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; <a href="../Q05-weekly-kpi-chart-email/README.md">Q05 · Weekly KPI chart email →</a></p>
