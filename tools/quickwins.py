from lib import *

Q = "⚡ Quick win"


def Q01(root):
    w = WF("Q01-daily-agenda-calendar", "Q01 · Daily agenda + free slots from Google Calendar")
    w.note("## 📅 Q01 · Start the day knowing your time\nToday's meetings, total meeting load, and **free focus slots** ≥ 45 min between 9:00 and 18:00.", (0, 0), 440)
    w.add("Weekdays 7:30", "scheduleTrigger", 1.2, {"rule": {"interval": [{"field": "cronExpression", "expression": "30 7 * * 1-5"}]}}, (0, 0))
    w.add("Today's Events", "googleCalendar", 1.3, {"operation": "getAll", "calendar": {"__rl": True, "mode": "id", "value": "primary"},
        "returnAll": True, "timeMin": "={{ $today }}", "timeMax": "={{ $today.plus({ days: 1 }) }}", "options": {"singleEvents": True, "orderBy": "startTime"}},
        (220, 0), alwaysOutputData=True)
    w.add("Build Agenda", "code", 2, {"jsCode":
        "const DAY_START = 9, DAY_END = 18, MIN_FOCUS = 45; // hours, hours, minutes\n"
        "const ev = $input.all().map(i => i.json).filter(e => e.start?.dateTime && e.status !== 'cancelled');\n"
        "const t = d => new Date(d);\n"
        "const fmt = d => t(d).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: $now.zoneName });  // workflow timezone\n"
        "const mins = ev.reduce((s, e) => s + (t(e.end.dateTime) - t(e.start.dateTime)) / 60000, 0);\n"
        "// find gaps between meetings inside working hours\n"
        "// $today = midnight in the workflow timezone, so 9:00–18:00 means your local working day.\n"
        "let cursor = $today.set({ hour: DAY_START }).toJSDate(); const end = $today.set({ hour: DAY_END }).toJSDate();\n"
        "const free = [];\n"
        "for (const e of ev) { const s = t(e.start.dateTime); if (s - cursor >= MIN_FOCUS * 60000) free.push([cursor, s]); if (t(e.end.dateTime) > cursor) cursor = t(e.end.dateTime); }\n"
        "if (end - cursor >= MIN_FOCUS * 60000) free.push([cursor, end]);\n"
        "const rows = ev.map(e => `<tr><td>${fmt(e.start.dateTime)}–${fmt(e.end.dateTime)}</td><td>${e.summary || '(no title)'}</td><td>${(e.attendees || []).length}</td></tr>`).join('');\n"
        "const load = mins > 300 ? '🔴 heavy' : mins > 180 ? '🟠 busy' : '🟢 light';\n"
        "return [{ json: { subject: `📅 ${ev.length} meetings · ${Math.round(mins / 60 * 10) / 10} h · ${load}`,\n"
        "  html: `<h3>Meetings</h3>${ev.length ? `<table border=1 cellpadding=6 style=\"border-collapse:collapse\"><tr><th>Time</th><th>Meeting</th><th>People</th></tr>${rows}</table>` : '<p>No meetings 🎉</p>'}`\n"
        "      + `<h3>Focus slots (≥ ${MIN_FOCUS} min)</h3><ul>${free.map(([a, b]) => `<li>${fmt(a)}–${fmt(b)}</li>`).join('') || '<li>None. Consider declining something.</li>'}</ul>` } }];"}, (440, 0))
    w.add("Email Me", "gmail", 2.1, gmail_send(EMAIL, "={{ $json.subject }}", "={{ $json.html }}"), (660, 0))
    w.chain("Weekdays 7:30", "Today's Events", "Build Agenda", "Email Me")
    write(root, w, readme("Q01", "Daily agenda + free focus slots", Q, "Personal productivity", "15 min",
        "Most people open their calendar and react. A 7:30 AM email showing today's meetings, how heavy the day is, and where the **focus slots** are lets you plan deep work before the first call.",
        ["Google Calendar *Get many events* with a time window", "`$today` and Luxon date maths (`$today.plus({ days: 1 })`)",
         "A gap-finding algorithm in the Code node", "`alwaysOutputData` so empty days still send an email"],
        "Schedule (weekdays 7:30) → Google Calendar events today → Code (agenda + free slots) → Gmail",
        ["Google Calendar OAuth2 (same Google Cloud project as Gmail)", "Gmail OAuth2"],
        ["Enable the **Google Calendar API** in your Google Cloud project, then create a *Google Calendar OAuth2* credential.",
         "Add **Google Calendar → Event → Get many**, calendar `primary`, *Return all*, After `{{ $today }}`, Before `{{ $today.plus({ days: 1 }) }}`. Options: *Single events* on, order by start time.",
         "Settings tab → **Always Output Data** on.",
         "Paste the Code node. Change `DAY_START`, `DAY_END` and `MIN_FOCUS` to suit your day.",
         "Gmail to yourself."],
        ["Run on a day with 2+ meetings and check that the gaps are right.", "Run on a weekend. You should get \"No meetings 🎉\"."],
        [("Times are off by a few hours", "Set *Workflow settings → Timezone* to your city. The code reads it via `$now.zoneName` and `$today`."),
         ("Recurring meetings missing", "Turn on *Single events* so recurrences are expanded.")],
        ["Auto-create a \"Focus\" event in the biggest free slot.", "Add tomorrow's first meeting so you can prepare the night before."]))


def Q02(root):
    w = WF("Q02-price-drop-tracker", "Q02 · Price drop tracker (web scraping + state)")
    w.note("## 🏷️ Q02 · Watch a product price\nScrapes a product page every 6 h, remembers the last price, alerts when it drops below your target **or** drops by >5%.\nDemo site: books.toscrape.com (built for scraping practice).", (0, 0), 460)
    w.add("Every 6 Hours", "scheduleTrigger", 1.2, {"rule": {"interval": [{"field": "hours", "hoursInterval": 6}]}}, (0, 0))
    w.add("⚙️ Products", "code", 2, {"jsCode":
        "// Add as many products as you like. selector = CSS selector of the price element.\n"
        "// The first demo target (55) is ABOVE the current price (51.77) so your first test run sends an alert. Lower it afterwards.\n"
        "const ALERT_TO = 'you@example.com';\n"
        "return [\n"
        "  { name: 'A Light in the Attic', url: 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html', selector: 'p.price_color', target: 55 },\n"
        "  { name: 'Tipping the Velvet', url: 'https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html', selector: 'p.price_color', target: 50 },\n"
        "].map(p => ({ json: { ...p, alert_to: ALERT_TO } }));"}, (220, 0))
    w.add("Fetch Page", "httpRequest", 4.2, {"url": "={{ $json.url }}", "options": {"response": {"response": {"responseFormat": "text"}},
        "timeout": 15000}}, (440, 0), retryOnFail=True, onError="continueRegularOutput")
    w.add("Extract Price", "html", 1.2, {"operation": "extractHtmlContent", "dataPropertyName": "data",
        "extractionValues": {"values": [{"key": "price_text", "cssSelector": "={{ $('⚙️ Products').item.json.selector }}", "returnValue": "text"}]}, "options": {}}, (660, 0))
    w.add("Compare with Last Price", "code", 2, {"jsCode":
        "const state = $getWorkflowStaticData('global'); state.prices ??= {};\n"
        "const products = $('⚙️ Products').all().map(i => i.json);\n"
        "return $input.all().map((it, i) => {\n"
        "  const p = products[i];\n"
        "  const price = parseFloat(String(it.json.price_text || '').replace(/[^0-9.]/g, ''));\n"
        "  const last = state.prices[p.url];\n"
        "  const dropPct = last ? Math.round((last - price) / last * 1000) / 10 : 0;\n"
        "  const alert = Number.isFinite(price) && (price <= p.target || dropPct >= 5);\n"
        "  if (Number.isFinite(price)) state.prices[p.url] = price;\n"
        "  return { json: { ...p, price, last: last ?? null, dropPct, alert, ok: Number.isFinite(price) } };\n"
        "});"}, (880, 0))
    w.note("⚠️ **No email?** Check `alert` in this node's output.\nFires only if `price ≤ target` **or** it dropped `≥5%` since the last check (set in *Compare with Last Price*).\nTo test: set `target` above the current price, then run it.", (1100, 220), 300, 160, 4)
    w.add("Worth Alerting?", "filter", 2.2, {"conditions": conditions(cond("={{ $json.alert }}", "boolean", "true")), "options": {}}, (1100, 0))
    w.add("Price Alert", "gmail", 2.1, gmail_send("={{ $json.alert_to }}", "=🏷️ {{ $json.name }} now {{ $json.price }} ({{ $json.dropPct }}% drop)",
        "=<p><b>{{ $json.name }}</b> is now <b>{{ $json.price }}</b> (was {{ $json.last ?? 'unknown' }}, target {{ $json.target }}).</p><p><a href=\"{{ $json.url }}\">Open product</a></p>"), (1320, 0))
    w.chain("Every 6 Hours", "⚙️ Products", "Fetch Page", "Extract Price", "Compare with Last Price", "Worth Alerting?", "Price Alert")
    write(root, w, readme("Q02", "Price drop tracker", Q, "Shopping / e-commerce ops", "20 min",
        "Waiting for a laptop to go on sale, watching a competitor's pricing, or checking a supplier's rates: all of it is \"check a web page, remember a number, tell me when it changes\". The same pattern works for stock availability, job postings and government notices.",
        ["HTTP Request returning raw **HTML text**", "**HTML node**: extract values with CSS selectors", "Parsing prices safely (`replace(/[^0-9.]/g,'')`)",
         "Remembering values between runs with `$getWorkflowStaticData`", "Two alert rules: absolute target and relative drop"],
        "Schedule (6 h) → Code (product list) → HTTP GET page → HTML extract price → Code (compare with stored price) → Filter → Gmail",
        ["Gmail OAuth2 (scraping needs no key)"],
        ["Add products in *⚙️ Products*. To find a selector, right-click the price in Chrome → *Inspect* → right-click the element → *Copy → Copy selector*.",
         "**HTTP Request**: URL `{{ $json.url }}`, Options → Response → *Response format: Text*.",
         "**HTML → Extract HTML content** from the `data` field with your selector.",
         "Paste the compare Code node, then Filter `alert is true` → Gmail.",
         "**Activate** it. Static data only persists in active runs."],
        ["Run it once as-is: the first demo product's target (55) is above its price, so you get an alert. Run it again with targets below the price: no alert, because nothing dropped.",
         "**Manual runs don't save static data.** *Compare with Last Price* only remembers prices between **active** (scheduled) runs, so `last` stays `null` while you test by hand. See L21 for the same pattern.", "Check that a broken URL doesn't stop the other products (*On Error → Continue*)."],
        [("Price is `NaN`", "The selector matched nothing. Check it in the browser dev tools; many shops render prices with JavaScript (use their API or a headless-browser service instead)."),
         ("Blocked / 403", "Some sites block bots. Respect robots.txt and terms of service, and prefer official APIs or affiliate feeds.")],
        ["Log every price to Sheets and chart the history (see Q05).", "Send to Telegram instead of email (see Q03)."]))


def Q03(root):
    w = WF("Q03-telegram-capture-bot", "Q03 · Telegram quick-capture bot (todos, notes, expenses)")
    w.note("## 💬 Q03 · Your pocket inbox\nSend the bot:\n`/todo call CA about GST`\n`/exp 450 food lunch`\n`/note idea: weekly retro bot`\nIt files each into Google Sheets and replies ✅.", (0, 0), 420)
    w.add("On Telegram Message", "telegramTrigger", 1.2, {"updates": ["message"], "additionalFields": {}}, (0, 0))
    w.add("Parse Command", "code", 2, {"mode": "runOnceForEachItem", "jsCode":
        "const text = ($json.message?.text || '').trim();\n"
        "const [cmd, ...rest] = text.split(/\\s+/);\n"
        "const body = rest.join(' ');\n"
        "const base = { time: new Date().toISOString(), chat_id: $json.message.chat.id, from: $json.message.from?.first_name || '' };\n"
        "if (cmd === '/exp') {\n"
        "  const [amt, category, ...note] = rest;\n"
        "  const amount = Number(amt);\n"
        "  if (!Number.isFinite(amount)) return { json: { ...base, kind: 'error', reply: '⚠️ Usage: /exp 450 food lunch' } };\n"
        "  return { json: { ...base, kind: 'expense', amount, category: category || 'other', text: note.join(' '), reply: `✅ ₹${amount} logged under ${category || 'other'}` } };\n"
        "}\n"
        "if (cmd === '/todo' || cmd === '/note') return { json: { ...base, kind: cmd.slice(1), text: body, reply: `✅ ${cmd.slice(1)} saved` } };\n"
        "return { json: { ...base, kind: 'error', reply: 'Commands: /todo …, /note …, /exp <amount> <category> <note>' } };"}, (220, 0))
    w.add("Valid Command?", "if", 2.2, {"conditions": conditions(cond("={{ $json.kind }}", "string", "notEquals", "error")), "options": {}}, (440, 0))
    w.add("Save to Inbox Sheet", "googleSheets", 4.5, sheet_append("Inbox"), (660, -100))
    w.add("Reply", "telegram", 1.2, {"chatId": "={{ $('Parse Command').item.json.chat_id }}", "text": "={{ $('Parse Command').item.json.reply }}", "additionalFields": {"appendAttribution": False}}, (880, 0))
    w.chain("On Telegram Message", "Parse Command", "Valid Command?")
    w.link("Valid Command?", "Save to Inbox Sheet", 0); w.link("Save to Inbox Sheet", "Reply"); w.link("Valid Command?", "Reply", 1)
    write(root, w, readme("Q03", "Telegram quick-capture bot", Q, "Personal productivity / finance", "20 min",
        "Ideas, todos and expenses happen on the move. Opening a spreadsheet on a phone is painful, but a chat message isn't. A bot that files everything into one sheet is the cheapest personal system you can build, and the same pattern works for field staff logging site visits or sales reps logging calls.",
        ["**Telegram Trigger** (a webhook managed for you)", "Parsing simple commands in Code", "Validating input and replying with help text",
         "Sending the reply on both branches"],
        "Telegram message → Code (parse /todo /note /exp) → IF valid\n  ├ yes → Sheets append → Telegram reply ✅\n  └ no  → Telegram reply (usage help)",
        ["Telegram bot token: talk to **@BotFather** → `/newbot`", "Google Sheets OAuth2 (tab `Inbox`: time, chat_id, from, kind, amount, category, text, reply)"],
        ["In Telegram, message **@BotFather**, `/newbot`, and copy the token. Create a *Telegram API* credential in n8n.",
         "Add **Telegram Trigger** → updates: *message*.",
         "Paste the Parse Command code (*for each item*).",
         "IF `kind ≠ error` → Sheets append → Telegram *Send message* to `chat_id`.",
         "Wire the IF false branch to the same Reply node.",
         "**Activate**. Telegram needs the production webhook, and your n8n must be reachable over HTTPS."],
        ["Send `/exp 120 travel auto` and check the new row.", "Send `hello`. You should get the usage message."],
        [("Bot never replies", "The workflow isn't active, or n8n isn't reachable over public HTTPS. Telegram can't call localhost."),
         ("Anyone can use my bot", "Add an IF on `message.from.id` equal to your own Telegram ID.")],
        ["Add `/today` that reads today's expenses and replies with a total.", "Accept voice notes and transcribe them with an AI node."]))


def Q04(root):
    w = WF("Q04-github-stale-pr-reminder", "Q04 · Stale pull-request reminder (GitHub API → Slack)")
    w.note("## 🔁 Q04 · Unblock code review\nEvery weekday 10:00, lists open PRs untouched for 2+ days (drafts skipped) and posts one Slack message with owners and reviewers.", (0, 0), 460)
    w.add("Weekdays 10:00", "scheduleTrigger", 1.2, {"rule": {"interval": [{"field": "cronExpression", "expression": "0 10 * * 1-5"}]}}, (0, 0))
    w.add("⚙️ Config", "set", 3.4, assign(repo="n8n-io/n8n", stale_days=2, slack_channel="#dev"), (220, 0))
    w.add("Open PRs", "httpRequest", 4.2, {"url": "=https://api.github.com/repos/{{ $json.repo }}/pulls", "authentication": "predefinedCredentialType",
        "nodeCredentialType": "githubApi", "sendQuery": True, "queryParameters": {"parameters": [{"name": "state", "value": "open"}, {"name": "per_page", "value": "100"},
        {"name": "sort", "value": "updated"}, {"name": "direction", "value": "asc"}]}, "options": {}}, (440, 0), retryOnFail=True)
    w.add("Find Stale", "code", 2, {"jsCode":
        "const cfg = $('⚙️ Config').first().json;\n"
        "const days = d => Math.floor((Date.now() - Date.parse(d)) / 86400000);\n"
        "const prs = $input.all().map(i => i.json).filter(p => p.number && !p.draft && days(p.updated_at) >= cfg.stale_days);\n"
        "const lines = prs.map(p => `• <${p.html_url}|#${p.number} ${p.title}> by *${p.user.login}* · ${days(p.updated_at)}d idle · reviewers: ${(p.requested_reviewers || []).map(r => '@' + r.login).join(', ') || '_none assigned_'}`);\n"
        "return [{ json: { count: prs.length, text: `:hourglass: *${prs.length} PRs waiting ${cfg.stale_days}+ days in ${cfg.repo}*\\n${lines.join('\\n')}` } }];"}, (660, 0))
    w.add("Any Stale?", "if", 2.2, {"conditions": conditions(cond("={{ $json.count }}", "number", "gt", 0)), "options": {}}, (880, 0))
    w.add("Post to Slack", "slack", 2.3, slack_post("={{ $('⚙️ Config').item.json.slack_channel }}", "={{ $json.text }}"), (1100, -80))
    w.chain("Weekdays 10:00", "⚙️ Config", "Open PRs", "Find Stale", "Any Stale?"); w.link("Any Stale?", "Post to Slack", 0)
    write(root, w, readme("Q04", "Stale pull-request reminder", Q, "Engineering / DevOps", "15 min",
        "Code review is the most common hidden bottleneck in software teams. PRs sit for days and nobody notices until the sprint ends. One daily nudge in the team channel with the owner and reviewers named cuts review time dramatically.",
        ["GitHub REST API with a **predefined credential**", "Filtering by age and draft status", "Slack message formatting (`<url|text>` links, `*bold*`)",
         "Only posting when there's something to say"],
        "Schedule → Config → HTTP GET /repos/{repo}/pulls → Code (stale filter) → IF count>0 → Slack",
        ["GitHub API token (read access to the repo)", "Slack app with `chat:write` scope"],
        ["Create a GitHub credential (classic PAT with `repo`, or a fine-grained token with *Pull requests: read*).",
         "Create a Slack app at api.slack.com → OAuth scopes `chat:write` → install → copy the Bot token into a *Slack API* credential. Invite the bot to the channel.",
         "Set repo, stale_days and channel in Config.", "Run it."],
        ["Point it at a busy public repo (the default `n8n-io/n8n`) with `stale_days = 1`. You should see a list."],
        [("`not_in_channel`", "Invite the bot: `/invite @your-bot` in the channel."),
         ("Only 100 PRs", "Add pagination (HTTP node → Options → Pagination) for very large repos.")],
        ["DM each reviewer instead of posting in the channel.", "Add CI status per PR from the `/commits/{sha}/status` endpoint."]))


def Q05(root):
    w = WF("Q05-weekly-kpi-chart-email", "Q05 · Weekly KPI chart email (Sheets → QuickChart → Gmail)")
    w.note("## 📈 Q05 · A chart in the inbox\nReads daily numbers from a sheet, groups them by week, draws a chart and emails it every Monday. No BI tool needed.", (0, 0), 440)
    w.add("Mondays 8:00", "scheduleTrigger", 1.2, {"rule": {"interval": [{"field": "cronExpression", "expression": "0 8 * * 1"}]}}, (0, 0))
    w.add("Read Daily Sales", "googleSheets", 4.5, sheet_read("Sales"), (220, 0))
    w.add("Group by Week", "code", 2, {"jsCode":
        "// Sheet columns: date (YYYY-MM-DD) | revenue | orders\n"
        "const weekKey = d => DateTime.fromISO(String(d).slice(0, 10), { zone: 'utc' }).startOf('week').toISODate();  // Monday of that week\n"
        "const weeks = {};\n"
        "for (const { json: r } of $input.all()) { if (!r.date) continue; const k = weekKey(r.date); weeks[k] ??= { revenue: 0, orders: 0 }; weeks[k].revenue += Number(r.revenue) || 0; weeks[k].orders += Number(r.orders) || 0; }\n"
        "const keys = Object.keys(weeks).sort().slice(-8);\n"
        "const rev = keys.map(k => Math.round(weeks[k].revenue));\n"
        "const last = rev.at(-1) || 0, prev = rev.at(-2) || 0;\n"
        "const change = prev ? Math.round((last - prev) / prev * 1000) / 10 : 0;\n"
        "return [{ json: { labels: keys.map(k => k.slice(5)), revenue: rev, last, prev, change } }];"}, (440, 0))
    w.add("Draw Chart", "quickChart", 1, {"chartType": "bar", "labelsMode": "array", "labelsArray": "={{ $json.labels }}", "data": "={{ $json.revenue }}",
        "output": "chart", "chartOptions": {"width": 700, "height": 320, "backgroundColor": "#ffffff"}, "datasetOptions": {"label": "Weekly revenue (₹)", "backgroundColor": "#7C3AED"}}, (660, 0))
    w.add("Email Report", "gmail", 2.1, {"sendTo": EMAIL, "subject": "=Weekly revenue ₹{{ $json.last.toLocaleString('en-IN') }} ({{ $json.change >= 0 ? '▲' : '▼' }} {{ $json.change }}%)",
        "emailType": "html", "message": "=<p>Last week: <b>₹{{ $json.last.toLocaleString('en-IN') }}</b>, previous: ₹{{ $json.prev.toLocaleString('en-IN') }} ({{ $json.change }}%).</p><p>Chart attached (last 8 weeks).</p>",
        "options": {"appendAttribution": False, "attachmentsUi": {"attachmentsBinary": [{"property": "chart"}]}}}, (880, 0))
    w.chain("Mondays 8:00", "Read Daily Sales", "Group by Week", "Draw Chart", "Email Report")
    write(root, w, readme("Q05", "Weekly KPI chart email", Q, "Management / sales", "20 min",
        "Small businesses keep numbers in a spreadsheet but never look at the trend. A Monday email with one chart and the week-over-week change is often all the \"BI\" a team needs.",
        ["Google Sheets *read rows*", "Grouping by ISO week in Code", "**QuickChart** node: data to PNG chart as binary",
         "Attaching binary files to Gmail", "Week-over-week % change"],
        "Schedule (Mon 8:00) → Sheets read → Code (group by week) → QuickChart (bar PNG) → Gmail with attachment",
        ["Google Sheets OAuth2 (tab `Sales`: date, revenue, orders)", "Gmail OAuth2"],
        ["Create a `Sales` tab with daily rows (use `=RANDBETWEEN(20000,90000)` to fake 60 days).",
         "Sheets → *Get row(s)* from `Sales`.", "Paste the Group-by-Week code.",
         "**QuickChart**: type Bar, labels *from array* `{{ $json.labels }}`, data `{{ $json.revenue }}`, output field `chart`.",
         "Gmail → Options → **Attachments** → property `chart`."],
        ["Run it and open the PNG in the QuickChart output's Binary tab before emailing."],
        [("Chart is empty", "Revenue values were strings with commas. The code uses `Number()`, so strip `₹` and `,` in the sheet."),
         ("No attachment", "The attachment property name must match the QuickChart *output* field (`chart`).")],
        ["Add an AI narrative of the trend (see P12).", "Chart orders and revenue as two datasets."]))


def Q06(root):
    w = WF("Q06-invoice-due-reminders", "Q06 · Invoice due & overdue reminders (Sheets as a mini-CRM)")
    w.note("## 💸 Q06 · Get paid on time\nDaily: finds unpaid invoices due in 3 days (friendly nudge) or overdue (firm reminder), emails the client, and writes `last_reminded` back so nobody gets spammed.", (0, 0), 480)
    w.add("Daily 10:00", "scheduleTrigger", 1.2, {"rule": {"interval": [{"triggerAtHour": 10}]}}, (0, 0))
    w.add("Read Invoices", "googleSheets", 4.5, sheet_read("Invoices"), (220, 0))
    w.add("Who Needs a Reminder?", "code", 2, {"jsCode":
        "// Columns: invoice_no | client | email | amount | due_date (YYYY-MM-DD) | status (paid/unpaid) | last_reminded\n"
        "// $today follows the workflow timezone. new Date() is UTC-based and is off by a day near midnight.\n"
        "const today = $today.toISODate();\n"
        "const daysTo = d => Math.round(DateTime.fromISO(String(d).slice(0, 10), { zone: $today.zoneName }).diff($today, 'days').days);\n"
        "return $input.all().map(i => i.json)\n"
        "  .filter(r => String(r.status).toLowerCase() !== 'paid' && r.due_date && r.last_reminded !== today)\n"
        "  .map(r => ({ ...r, days: daysTo(r.due_date) }))\n"
        "  .filter(r => r.days === 3 || r.days < 0 && (-r.days) % 7 === 1)   // 3 days before, then weekly once overdue\n"
        "  .map(r => ({ json: { ...r, stage: r.days >= 0 ? 'upcoming' : 'overdue' } }));"}, (440, 0))
    w.add("Stage", "switch", 3.2, {"rules": {"values": [
        {"conditions": conditions(cond("={{ $json.stage }}", "string", "equals", "upcoming")), "renameOutput": True, "outputKey": "Upcoming"},
        {"conditions": conditions(cond("={{ $json.stage }}", "string", "equals", "overdue")), "renameOutput": True, "outputKey": "Overdue"}]}, "options": {}}, (660, 0))
    w.add("Friendly Nudge", "gmail", 2.1, gmail_send("={{ $json.email }}", "=Invoice {{ $json.invoice_no }} due on {{ $json.due_date }}",
        "=<p>Hi {{ $json.client }},</p><p>A quick heads-up that invoice <b>{{ $json.invoice_no }}</b> for ₹{{ $json.amount }} is due on {{ $json.due_date }}.</p><p>Thank you!</p>"), (900, -100))
    w.add("Firm Reminder", "gmail", 2.1, gmail_send("={{ $json.email }}", "=Overdue: invoice {{ $json.invoice_no }} ({{ -$json.days }} days)",
        "=<p>Hi {{ $json.client }},</p><p>Invoice <b>{{ $json.invoice_no }}</b> for ₹{{ $json.amount }} was due on {{ $json.due_date }} and is now {{ -$json.days }} days overdue.</p><p>Please arrange payment or reply if there's an issue.</p>"), (900, 100))
    w.add("Mark Reminded", "set", 3.4, assign(invoice_no="={{ $('Who Needs a Reminder?').item.json.invoice_no }}", last_reminded="={{ $today.toISODate() }}"), (1120, 0))
    w.add("Write Back", "googleSheets", 4.5, sheet_upsert("Invoices", "invoice_no"), (1340, 0))
    w.chain("Daily 10:00", "Read Invoices", "Who Needs a Reminder?", "Stage")
    w.link("Stage", "Friendly Nudge", 0); w.link("Stage", "Firm Reminder", 1)
    w.link("Friendly Nudge", "Mark Reminded"); w.link("Firm Reminder", "Mark Reminded"); w.link("Mark Reminded", "Write Back")
    write(root, w, readme("Q06", "Invoice due & overdue reminders", Q, "Finance / freelancers / SMB", "25 min",
        "Freelancers and small businesses lose real money to late payments simply because nobody follows up. A polite, consistent, automatic reminder schedule is one of the highest-ROI automations there is.",
        ["Date maths for *due in N days* / *N days overdue*", "Switch routing to different email tones",
         "**Append or update** a row by key (`invoice_no`) to write state back", "Preventing duplicates with a `last_reminded` column"],
        "Schedule → Sheets read → Code (pick reminders) → Switch\n  ├ Upcoming → friendly email ┐\n  └ Overdue  → firm email     ┴→ Set last_reminded → Sheets upsert by invoice_no",
        ["Google Sheets OAuth2 (tab `Invoices`)", "Gmail OAuth2"],
        ["Create the `Invoices` tab with the columns in the Code comment.",
         "Sheets *Get row(s)* → paste the selector code.",
         "Switch on `stage` → two Gmail nodes.",
         "Both → **Set** `invoice_no` + `last_reminded` → Sheets **Append or update**, matching column `invoice_no`."],
        ["Add a row due in exactly 3 days with your own email, then run it. You should get one email, and `last_reminded` should be filled in.", "Run again the same day. There should be no second email."],
        [("Every run re-sends", "`matchingColumns` must be `invoice_no`, and the header must match exactly."),
         ("Wrong day counts", "Dates must be plain `YYYY-MM-DD` text. Format the column as *Plain text* in Sheets.")],
        ["Attach the invoice PDF from Drive.", "Escalate to a phone call task (Jira/Todoist) after 21 days overdue."]))


def Q07(root):
    w = WF("Q07-gmail-ai-auto-labeler", "Q07 · Gmail AI auto-labeler (Text Classifier)")
    w.note("## 🏷️ Q07 · Inbox zero, assisted\nEvery 5 min: classifies new emails into Billing / Support / Sales lead / Newsletter with Gemini and applies a Gmail label. Nothing is sent or deleted.", (0, 0), 460)
    w.add("New Unread Email", "gmailTrigger", 1.2, {"pollTimes": {"item": [{"mode": "everyX", "value": 5, "unit": "minutes"}]}, "simple": True,
        "filters": {"readStatus": "unread", "q": "-category:promotions -label:ai-labeled"}, "options": {}}, (0, 0))
    w.lc("Classify", "textClassifier", 1.1, {"inputText": "=From: {{ $json.From }}\nSubject: {{ $json.Subject }}\n\n{{ $json.snippet }}",
        "categories": {"categories": [
            {"category": "Billing", "description": "Invoices, payments, refunds, receipts, subscription charges"},
            {"category": "Support", "description": "A customer or user reporting a problem or asking how to do something"},
            {"category": "Sales lead", "description": "Someone interested in buying, requesting a demo, pricing or a quote"},
            {"category": "Newsletter", "description": "Bulk updates, digests, marketing, notifications from tools"}]},
        "options": {"fallback": "other"}}, (240, 0))
    w.gemini("Gemini", (240, 220), 0)
    labels = [("Billing", "REPLACE_LABEL_ID_BILLING"), ("Support", "REPLACE_LABEL_ID_SUPPORT"), ("Sales lead", "REPLACE_LABEL_ID_SALES"),
              ("Newsletter", "REPLACE_LABEL_ID_NEWSLETTER"), ("Other", "REPLACE_LABEL_ID_OTHER")]
    for i, (cat, lid) in enumerate(labels):
        name = f"Label: {cat}"
        w.add(name, "gmail", 2.1, {"operation": "addLabels", "messageId": "={{ $json.id }}", "labelIds": [lid, "REPLACE_LABEL_ID_AI_LABELED"]}, (520, -260 + i * 130))
        w.link("Classify", name, i)
    w.link("New Unread Email", "Classify"); w.ai("Gemini", "Classify", "ai_languageModel")
    write(root, w, readme("Q07", "Gmail AI auto-labeler", Q, "Productivity / support", "20 min",
        "A shared inbox (support@, info@) mixes invoices, customer problems, sales enquiries and noise. Labelling them automatically means each person only looks at their own label, and nothing gets missed or sent by mistake because the AI only *labels*.",
        ["**Text Classifier** node: one output per category", "Category descriptions are the prompt, so write them carefully",
         "A *fallback* category for anything uncertain", "A marker label (`ai-labeled`) so each email is processed once"],
        "Gmail Trigger (unread, not yet labelled) → Text Classifier ⇐ Gemini → 5 outputs → Gmail add labels",
        ["Gmail OAuth2", "Google Gemini API key"],
        ["In Gmail, create labels: `Billing`, `Support`, `Sales lead`, `Newsletter`, `Other`, `ai-labeled`.",
         "Get the label IDs: add a temporary Gmail node *Label → Get many* and run it. Paste the IDs over the `REPLACE_LABEL_ID_…` values.",
         "Gmail Trigger: *Simplify* on, unread, search `-label:ai-labeled`.",
         "**Text Classifier**: input = from + subject + snippet; add the 4 categories with good descriptions; Options → *When no clear match* → **Other**.",
         "Wire each output to a Gmail *Add label* node."],
        ["Send yourself test emails: a fake invoice, a \"your app is broken\", a \"can I get pricing?\". Check the labels."],
        [("Everything lands in Other", "Descriptions are too vague. Add typical words and examples."),
         ("Same email labelled every 5 min", "The `ai-labeled` label or the search exclusion is missing.")],
        ["Route Support to P02 (AI reply drafts).", "Post Sales leads to Slack instantly."]))


def Q08(root):
    w = WF("Q08-rss-to-telegram-dedupe", "Q08 · Auto-post new articles to a Telegram channel (dedupe across runs)")
    w.note("## 📣 Q08 · Channel autopilot\nEvery 30 min: reads a feed, keeps the last few days, and uses **Remove Duplicates → seen in previous executions** so each link is posted exactly once, ever.", (0, 0), 460)
    w.add("Every 30 Minutes", "scheduleTrigger", 1.2, {"rule": {"interval": [{"field": "minutes", "minutesInterval": 30}]}}, (0, 0))
    w.add("⚙️ Config", "set", 3.4, assign(feed_url="https://blog.n8n.io/rss/", channel="@your_channel_name", max_age_days=3), (220, 0))
    w.add("Read Feed", "rssFeedRead", 1.1, {"url": "={{ $json.feed_url }}", "options": {}}, (440, 0), onError="continueRegularOutput")
    w.add("Recent Only", "filter", 2.2, {"conditions": conditions(cond("={{ $json.isoDate }}", "dateTime", "after", "={{ $now.minus({ days: $('⚙️ Config').first().json.max_age_days }).toISO() }}")), "options": {}}, (660, 0))
    w.add("Oldest First", "sort", 1, {"sortFieldsUi": {"sortField": [{"fieldName": "isoDate"}]}, "options": {}}, (880, 0))
    w.note("⚠️ **Nothing posted?** A link is remembered the moment it passes this node, so a 2nd run posts nothing (that's the point).\nTo re-test: change `historySize` or recreate the node.\nNo `Limit` after this node on purpose: anything cut after dedupe would be marked seen and never posted.", (1100, 200), 320, 190, 4)
    w.add("Only New Links", "removeDuplicates", 2, {"operation": "removeItemsSeenInPreviousExecutions", "dedupeValue": "={{ $json.link }}", "options": {"historySize": 5000}}, (1100, 0))
    w.add("Post to Channel", "telegram", 1.2, {"chatId": "={{ $('⚙️ Config').first().json.channel }}", "text": "=📰 <b>{{ $json.title }}</b>\n{{ ($json.contentSnippet || '').slice(0, 200) }}…\n{{ $json.link }}",
        "additionalFields": {"parse_mode": "HTML", "appendAttribution": False}}, (1320, 0))
    w.chain("Every 30 Minutes", "⚙️ Config", "Read Feed", "Recent Only", "Oldest First", "Only New Links", "Post to Channel")
    write(root, w, readme("Q08", "RSS → Telegram channel with dedupe across runs", Q, "Marketing / community", "15 min",
        "Communities and company channels need a steady flow of relevant links, and nobody wants to post them by hand. The hard part is never posting the same link twice, even across restarts. n8n's *Remove Duplicates* node now remembers what it has seen between executions.",
        ["**Remove Duplicates → Remove items seen in previous executions**", "History size and what happens when it fills",
         "Why **filter before dedupe, never limit after it**: anything dropped after dedupe is marked seen and lost", "Sorting so the channel reads in publish order", "Telegram HTML formatting"],
        "Schedule (30 min) → Config → RSS → keep last 3 days → oldest first → Remove Duplicates (by link, across runs) → Telegram channel",
        ["Telegram bot token (add the bot as an **admin** of your channel)"],
        ["Create a channel and add your bot as admin with *Post messages*.", "Set the feed URL, channel and `max_age_days` in **⚙️ Config**.",
         "**Filter** `isoDate` is after `{{ $now.minus({ days: 3 }) }}`, then **Sort** by `isoDate` (ascending). This stops the first run flooding the channel with the whole feed.",
         "**Remove Duplicates** → operation *Remove items processed in previous executions*, value `{{ $json.link }}`.",
         "Telegram *Send message* to `{{ $('⚙️ Config').first().json.channel }}`, parse mode HTML."],
        ["Run twice. The second run should post nothing.", "The first run posts only articles from the last 3 days, oldest first.", "**Activate** it. Like static data, dedupe history only builds up in real (active) runs you keep."],
        [("`chat not found`", "Use `@channelusername` for public channels, or the numeric `-100…` ID for private ones. The bot must be an admin."),
         ("Posts everything again after editing", "Dedupe history is per node. Deleting or recreating the node resets it."),
         ("A post failed and never came back", "The link was already marked seen. *Post to Channel* retries 3 times; if Telegram is down longer, repost by hand.")],
        ["Add AI to write a one-line hook per article.", "Merge several feeds (see L05)."]))


ALL = [Q01, Q02, Q03, Q04, Q05, Q06, Q07, Q08]
