from lib import *

B = "🟢 Beginner"
I = "🟡 Integrations"


def L01(root):
    w = WF("L01-hello-n8n", "L01 · Hello n8n — your first workflow")
    w.note("## 👋 L01 · Hello n8n\n1. Click **Execute workflow**\n2. Click each node → look at the **OUTPUT** panel\n3. Change the name in *Set Your Data* and run again\n\nData in n8n = a list of **items**, each item = JSON.", (-60, -260), 420, 240, 5)
    w.add("When clicking 'Execute workflow'", "manualTrigger", 1, {}, (0, 0))
    w.add("Set Your Data", "set", 3.4, assign(name="Learner", city="Chennai", tasks_done=3), (220, 0))
    w.add("Build Greeting", "code", 2, {"jsCode":
        "// Every node receives items and returns items.\n"
        "return $input.all().map(item => ({\n"
        "  json: {\n"
        "    ...item.json,\n"
        "    greeting: `Hello ${item.json.name} from ${item.json.city}! You finished ${item.json.tasks_done} tasks today.`,\n"
        "    generated_at: new Date().toISOString(),\n"
        "  }\n"
        "}));"}, (440, 0))
    w.add("Send to Yourself", "gmail", 2.1, gmail_send(EMAIL, "My first n8n workflow 🎉",
        "=<p>{{ $json.greeting }}</p><p><small>Sent at {{ $json.generated_at }}</small></p>"), (660, 0))
    w.chain("When clicking 'Execute workflow'", "Set Your Data", "Build Greeting", "Send to Yourself")
    r = readme("L01", "Hello n8n — your first workflow", B, "General", "10 min",
        "Everyone starts here. Before automating anything real, you need to understand how data moves between nodes. This workflow takes some values, builds a message and emails it to you.",
        ["Manual Trigger: run a workflow on demand", "Set node: create data without code",
         "Code node: transform items with JavaScript", "Expressions: `{{ $json.field }}`",
         "Reading the INPUT and OUTPUT panels"],
        "Manual Trigger → Set Your Data → Build Greeting (Code) → Send to Yourself (Gmail)",
        ["Gmail OAuth2 — see [docs/credentials.md](../../docs/credentials.md#gmail). *Optional*: delete the Gmail node and the workflow still teaches everything."],
        ["Create a new workflow and name it `L01 · Hello n8n`.",
         "Add a **Manual Trigger** node.",
         "Add an **Edit Fields (Set)** node with three fields: `name` (string), `city` (string), `tasks_done` (number).",
         "Add a **Code** node and paste the code from `workflow.json`. Look at how it spreads `...item.json` to keep the old fields.",
         "Add a **Gmail → Send message** node. In *To*, put your own email. In *Message*, drag `greeting` from the INPUT panel.",
         "Click **Execute workflow**."],
        ["Click each node and open the **OUTPUT** tab: Table, JSON and Schema views show the same data in different shapes.",
         "Change `tasks_done` to 10 and run again."],
        [("`Credentials not found` on Gmail", "Open the node → Credential → *Create new* and sign in with Google."),
         ("Code node: `Cannot read properties of undefined`", "Check the field name spelling — JSON keys are case-sensitive.")],
        ["Add a second item in the Set node (turn on *Include Other Input Fields*) or return two items from Code — watch Gmail send two emails.",
         "Replace Gmail with Telegram or Slack."])
    write(root, w, r)


def L02(root):
    w = WF("L02-daily-weather-email", "L02 · Daily weather email (Schedule + free API)")
    w.note("## ⏰ L02 · Scheduled workflows\nEdit **⚙️ Config** first (city, lat/lon, email).\nThen **Activate** the workflow (toggle top right) — schedules only fire when active.\n\nOpen-Meteo is free, no API key.", (-60, -280), 420, 240, 5)
    w.add("Every Morning 7 AM", "scheduleTrigger", 1.2, {"rule": {"interval": [{"triggerAtHour": 7}]}}, (0, 0))
    w.add("⚙️ Config", "set", 3.4, assign(city="Chennai", latitude=13.0827, longitude=80.2707,
                                           timezone="Asia/Kolkata", email_to=EMAIL), (220, 0))
    w.add("Fetch Weather", "httpRequest", 4.2, {"url": "https://api.open-meteo.com/v1/forecast", "sendQuery": True,
        "queryParameters": {"parameters": [
            {"name": "latitude", "value": "={{ $json.latitude }}"},
            {"name": "longitude", "value": "={{ $json.longitude }}"},
            {"name": "current", "value": "temperature_2m,relative_humidity_2m,wind_speed_10m"},
            {"name": "daily", "value": "temperature_2m_max,temperature_2m_min,precipitation_probability_max"},
            {"name": "timezone", "value": "={{ $json.timezone }}"},
            {"name": "forecast_days", "value": "1"}]},
        "options": {"timeout": 15000}}, (440, 0), retryOnFail=True, maxTries=3, waitBetweenTries=5000)
    w.add("Email Summary", "gmail", 2.1, gmail_send("={{ $('⚙️ Config').item.json.email_to }}",
        "={{ $('⚙️ Config').item.json.city }} weather — {{ $now.toFormat('dd LLL yyyy') }}",
        "=<h2>{{ $('⚙️ Config').item.json.city }} today</h2><ul>"
        "<li>Now: {{ $json.current.temperature_2m }}°C, humidity {{ $json.current.relative_humidity_2m }}%, wind {{ $json.current.wind_speed_10m }} km/h</li>"
        "<li>High / Low: {{ $json.daily.temperature_2m_max[0] }}°C / {{ $json.daily.temperature_2m_min[0] }}°C</li>"
        "<li>Chance of rain: {{ $json.daily.precipitation_probability_max[0] }}% {{ $json.daily.precipitation_probability_max[0] > 50 ? '☔ carry an umbrella' : '' }}</li></ul>"), (660, 0))
    w.chain("Every Morning 7 AM", "⚙️ Config", "Fetch Weather", "Email Summary")
    r = readme("L02", "Daily weather email", B, "Personal productivity", "15 min",
        "You want a short weather summary in your inbox every morning, before you leave home. This is the \"hello world\" of scheduled automation, and it calls a real public API.",
        ["Schedule Trigger and activating workflows", "A **Config node** pattern: keep every setting in one place",
         "HTTP Request with query parameters", "Referencing an earlier node: `$('⚙️ Config').item.json.city`",
         "Retry on fail (node Settings tab)", "Inline JavaScript in expressions (`? :` ternary)"],
        "Schedule (7 AM) → ⚙️ Config → HTTP GET open-meteo.com → Gmail",
        ["Gmail OAuth2"],
        ["Add a **Schedule Trigger** → *Days*, hour 7.",
         "Add a **Set** node named `⚙️ Config` with city, latitude, longitude, timezone and email_to. Get the coordinates from Google Maps (right-click → copy coordinates).",
         "Add an **HTTP Request** node: GET `https://api.open-meteo.com/v1/forecast`, turn on *Send Query Parameters* and map them from Config.",
         "In the HTTP node **Settings** tab, turn on *Retry On Fail* (3 tries, 5000 ms). Public APIs fail sometimes.",
         "Add **Gmail**. Build the HTML body by dragging fields from the INPUT panel.",
         "Run it once manually, then **Activate** it."],
        ["Click *Execute workflow*. A schedule workflow can always be run manually for testing.",
         "Check **Executions** (left sidebar) the next morning to see the automatic run."],
        [("Workflow never runs automatically", "It isn't **Active**, or your n8n instance was asleep (for example a laptop that was closed). Use n8n Cloud or a VPS for 24/7."),
         ("Wrong hour", "Set the timezone in *Workflow settings → Timezone*.")],
        ["Add an **IF** node: send only if the rain chance is above 50% (this previews L04).",
         "Loop over 3 cities by making Config return 3 items."])
    write(root, w, r)


def L03(root):
    w = WF("L03-job-search-api", "L03 · Daily job search digest (HTTP API + Code)")
    w.note("## 🌐 L03 · Calling any REST API\nSerpAPI → Google Jobs.\nFree key: serpapi.com (100 searches/month).\nEdit the query in **⚙️ Config**.", (-60, -260), 400, 200, 5)
    w.add("Every Morning 8 AM", "scheduleTrigger", 1.2, {"rule": {"interval": [{"triggerAtHour": 8}]}}, (0, 0))
    w.add("⚙️ Config", "set", 3.4, assign(query="Scrum Master OR Agile Coach", location="India", email_to=EMAIL, max_jobs=15), (220, 0))
    w.add("Search Google Jobs", "httpRequest", 4.2, {"url": "https://serpapi.com/search.json",
        "authentication": "predefinedCredentialType", "nodeCredentialType": "serpApi", "sendQuery": True,
        "queryParameters": {"parameters": [{"name": "engine", "value": "google_jobs"},
            {"name": "q", "value": "={{ $json.query }}"}, {"name": "location", "value": "={{ $json.location }}"},
            {"name": "chips", "value": "date_posted:today"}]}, "options": {}}, (440, 0), retryOnFail=True, maxTries=2)
    w.add("Format Email", "code", 2, {"jsCode":
        "const cfg = $('⚙️ Config').first().json;\n"
        "const jobs = ($input.first().json.jobs_results || []).slice(0, cfg.max_jobs);\n"
        "const today = new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });\n"
        "const esc = s => String(s ?? '').replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));\n"
        "const rows = jobs.map(j => {\n"
        "  const link = j.apply_options?.[0]?.link || j.share_link || '#';\n"
        "  return `<tr><td><a href=\"${link}\">${esc(j.title)}</a></td><td>${esc(j.company_name)}</td><td>${esc(j.location)}</td><td>${esc(j.detected_extensions?.posted_at || '')}</td></tr>`;\n"
        "}).join('');\n"
        "const html = jobs.length\n"
        "  ? `<h2>${jobs.length} new jobs · ${today}</h2><table border=\"1\" cellpadding=\"6\" style=\"border-collapse:collapse\"><tr><th>Role</th><th>Company</th><th>Location</th><th>Posted</th></tr>${rows}</table>`\n"
        "  : `<p>No new jobs today for <b>${esc(cfg.query)}</b>. Try widening the query.</p>`;\n"
        "return [{ json: { subject: `Job digest: ${jobs.length} × ${cfg.query} (${today})`, html, count: jobs.length } }];"}, (660, 0))
    w.add("Send Digest", "gmail", 2.1, gmail_send("={{ $('⚙️ Config').item.json.email_to }}", "={{ $json.subject }}", "={{ $json.html }}"), (880, 0))
    w.chain("Every Morning 8 AM", "⚙️ Config", "Search Google Jobs", "Format Email", "Send Digest")
    r = readme("L03", "Daily job search digest", B, "Career / HR", "20 min",
        "Job hunting means checking portals every day. This workflow searches Google Jobs every morning and emails you one clean table of today's postings.",
        ["HTTP Request with a **predefined credential** (SerpAPI)", "Reading nested API JSON (`jobs_results[].apply_options[0].link`)",
         "Code node that turns many items into one HTML email", "Optional chaining `?.` so missing fields don't crash the code",
         "Escaping HTML so a job title can't break your email"],
        "Schedule → ⚙️ Config → HTTP (SerpAPI google_jobs) → Code (HTML table) → Gmail",
        ["SerpAPI key: free at serpapi.com. In n8n: Credentials → *SerpAPI*", "Gmail OAuth2"],
        ["Sign up at serpapi.com and copy your API key. In n8n, create a **SerpApi** credential.",
         "Build the Schedule → Config chain as in L02.",
         "Add an **HTTP Request** node: Authentication = *Predefined credential type → SerpApi*; query `engine=google_jobs`, `q`, `location`, `chips=date_posted:today`.",
         "Run it and **study the output JSON**. Find `jobs_results`. This is the most important skill with any API.",
         "Add a **Code** node that loops over jobs and builds an HTML table (copy it from workflow.json).",
         "Add **Gmail** with subject/body = `{{ $json.subject }}` / `{{ $json.html }}`."],
        ["Change `query` to your own role and run it manually.", "Set `location` to a city (for example `Bengaluru, Karnataka, India`)."],
        [("401 / Invalid API key", "Re-create the SerpApi credential."),
         ("Email says 0 jobs", "`date_posted:today` is strict. Remove the `chips` parameter to test."),
         ("Monthly quota used up", "The free tier gives 100 searches a month. A daily run uses about 30.")],
        ["Save jobs to Google Sheets and skip ones you've already seen (dedupe by `job_id`).",
         "Add Gemini to score each job against your resume (see L18)."])
    write(root, w, r)


def L04(root):
    w = WF("L04-currency-alert-switch", "L04 · Currency rate alert (IF + Switch)")
    w.note("## 🔀 L04 · Branching\n**IF** = two roads (true/false).\n**Switch** = many roads.\nUSD→INR is checked every hour; you get an email only when something interesting happens.", (-60, -300), 420, 220, 5)
    w.add("Every Hour", "scheduleTrigger", 1.2, {"rule": {"interval": [{"field": "hours", "hoursInterval": 1}]}}, (0, 0))
    w.add("⚙️ Config", "set", 3.4, assign(base="USD", target="INR", high=88.5, low=83.0, email_to=EMAIL), (220, 0))
    w.add("Get Exchange Rate", "httpRequest", 4.2, {"url": "=https://open.er-api.com/v6/latest/{{ $json.base }}", "options": {}}, (440, 0), retryOnFail=True)
    w.add("API OK?", "if", 2.2, {"conditions": conditions(cond("={{ $json.result }}", "string", "equals", "success")), "options": {}}, (660, 0))
    w.add("Extract Rate", "set", 3.4, assign(rate="={{ $json.rates[$('⚙️ Config').item.json.target] }}",
                                              updated="={{ $json.time_last_update_utc }}"), (880, -100))
    w.nodes[-1]["parameters"]["assignments"]["assignments"][0]["type"] = "number"
    w.add("Which Zone?", "switch", 3.2, {"rules": {"values": [
        {"conditions": conditions(cond("={{ $json.rate }}", "number", "gte", "={{ $('⚙️ Config').item.json.high }}")), "renameOutput": True, "outputKey": "High"},
        {"conditions": conditions(cond("={{ $json.rate }}", "number", "lte", "={{ $('⚙️ Config').item.json.low }}")), "renameOutput": True, "outputKey": "Low"}]},
        "options": {"fallbackOutput": "extra", "renameFallbackOutput": "Normal"}}, (1100, -100))
    cfg = "$('⚙️ Config').item.json"
    w.add("Alert: Rate High", "gmail", 2.1, gmail_send(f"={{{{ {cfg}.email_to }}}}", f"=📈 {{{{ {cfg}.base }}}}→{{{{ {cfg}.target }}}} is HIGH: {{{{ $json.rate }}}}",
        "=<p>Rate is <b>{{ $json.rate }}</b>, above your threshold. Good time to send money home.</p><p>Updated: {{ $json.updated }}</p>"), (1340, -240))
    w.add("Alert: Rate Low", "gmail", 2.1, gmail_send(f"={{{{ {cfg}.email_to }}}}", f"=📉 {{{{ {cfg}.base }}}}→{{{{ {cfg}.target }}}} is LOW: {{{{ $json.rate }}}}",
        "=<p>Rate is <b>{{ $json.rate }}</b>, below your threshold. Good time to buy USD.</p><p>Updated: {{ $json.updated }}</p>"), (1340, -80))
    w.add("Normal — do nothing", "noOp", 1, {}, (1340, 80))
    w.add("API Failed — log it", "stopAndError", 1, {"errorMessage": "=Exchange-rate API returned: {{ $json['error-type'] || 'unknown error' }}"}, (880, 120))
    w.chain("Every Hour", "⚙️ Config", "Get Exchange Rate", "API OK?")
    w.link("API OK?", "Extract Rate", 0); w.link("API OK?", "API Failed — log it", 1)
    w.link("Extract Rate", "Which Zone?")
    w.link("Which Zone?", "Alert: Rate High", 0); w.link("Which Zone?", "Alert: Rate Low", 1); w.link("Which Zone?", "Normal — do nothing", 2)
    r = readme("L04", "Currency rate alert", B, "Finance / personal", "20 min",
        "If you send money abroad, pay overseas freelancers or invoice in USD, the exchange rate matters. You don't want to check it by hand, and you don't want an email every hour either. You want one only when the rate crosses a threshold.",
        ["**IF** node: validate an API response before trusting it", "**Switch** node with named outputs plus a fallback",
         "Comparing numbers against Config values", "**Stop and Error**: fail loudly so your error workflow (L19) catches it",
         "Dynamic URLs: `https://…/latest/{{ $json.base }}`"],
        "Schedule (hourly) → Config → HTTP → IF ok?\n   ├─ true → Extract Rate → Switch ─ High → Gmail\n   │                               ├ Low  → Gmail\n   │                               └ Normal → (nothing)\n   └─ false → Stop and Error",
        ["Gmail OAuth2 (open.er-api.com needs no key)"],
        ["Schedule Trigger → *Hours*, every 1.",
         "Config: base, target, high, low, email_to.",
         "HTTP GET `https://open.er-api.com/v6/latest/{{ $json.base }}`.",
         "**IF**: `{{ $json.result }}` *is equal to* `success`.",
         "On true, add a **Set** node that extracts `rate = {{ $json.rates[$('⚙️ Config').item.json.target] }}` as a *Number*.",
         "Add a **Switch** in *Rules* mode. Rule 1: rate ≥ high, rename the output to `High`. Rule 2: rate ≤ low, `Low`. Options → *Fallback output* → Extra output, named `Normal`.",
         "Connect a Gmail node to High and to Low, and a **No Operation** to Normal.",
         "On IF false, add **Stop and Error**."],
        ["Set `high` to 1 and run it. You should get the HIGH email.", "Set `base` to `XYZ` and run it. You should hit the Stop and Error branch."],
        [("Switch always goes to Normal", "The rate was saved as a string. Set its type to *Number* in the Set node."),
         ("Too many emails", "Add a cooldown: store the last alert time with `$getWorkflowStaticData` (see L21).")],
        ["Track 3 currencies at once (Config returns 3 items).", "Log every reading to Google Sheets and chart it."])
    write(root, w, r)


def L05(root):
    w = WF("L05-rss-news-code-node", "L05 · Tech news digest (RSS + Merge + Code)")
    w.note("## 🧑‍💻 L05 · Code node superpowers\nThree RSS feeds → Merge → **one Code node** that:\n• keeps the last 24 h\n• removes duplicates\n• sorts newest first\n• builds HTML\n(No AI yet. L11 adds Gemini on top of this.)", (-60, -380), 440, 260, 5)
    w.add("Every Morning 8 AM", "scheduleTrigger", 1.2, {"rule": {"interval": [{"triggerAtHour": 8}]}}, (0, 0))
    feeds = [("Google News · AI", "https://news.google.com/rss/search?q=artificial+intelligence+when:1d&hl=en-IN&gl=IN&ceid=IN:en"),
             ("TechCrunch · AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
             ("The Verge · AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml")]
    w.add("Merge Feeds", "merge", 3, {"numberInputs": 3}, (480, 0))
    for i, (n, u) in enumerate(feeds):
        w.add(n, "rssFeedRead", 1.1, {"url": u, "options": {}}, (240, -160 + i * 160), onError="continueRegularOutput")
        w.link("Every Morning 8 AM", n); w.link(n, "Merge Feeds", inp=i)
    w.add("Filter · Dedupe · Sort", "code", 2, {"jsCode":
        "const cutoff = Date.now() - 24 * 3600 * 1000;\n"
        "const seen = new Set();\n"
        "const norm = t => String(t || '').toLowerCase().replace(/[^a-z0-9 ]/g, '').slice(0, 60);\n"
        "const articles = $input.all().map(i => i.json)\n"
        "  .filter(a => a.title && a.link)\n"
        "  .map(a => ({ title: a.title.trim(), link: a.link, source: a.creator || (a.link.match(/https?:\\/\\/(?:www\\.)?([^/]+)/) || [])[1] || 'unknown', ts: Date.parse(a.isoDate || a.pubDate || '') || 0 }))\n"
        "  .filter(a => a.ts >= cutoff)\n"
        "  .filter(a => { const k = norm(a.title); if (seen.has(k)) return false; seen.add(k); return true; })\n"
        "  .sort((a, b) => b.ts - a.ts)\n"
        "  .slice(0, 25);\n"
        "const li = articles.map(a => `<li><a href=\"${a.link}\">${a.title}</a> <small>(${a.source})</small></li>`).join('');\n"
        "const listText = articles.map((a, i) => `${i + 1}. ${a.title} — ${a.link}`).join('\\n');\n"
        "return [{ json: { count: articles.length, html: `<ol>${li}</ol>`, listText } }];"}, (700, 0))
    w.add("Anything New?", "if", 2.2, {"conditions": conditions(cond("={{ $json.count }}", "number", "gt", 0)), "options": {}}, (920, 0))
    w.add("Email Digest", "gmail", 2.1, gmail_send(EMAIL, "=Tech news · {{ $json.count }} stories · {{ $now.toFormat('dd LLL') }}",
        "=<h2>Last 24 hours in AI</h2>{{ $json.html }}"), (1140, -80))
    w.chain("Merge Feeds", "Filter · Dedupe · Sort", "Anything New?")
    w.link("Anything New?", "Email Digest", 0)
    r = readme("L05", "Tech news digest with the Code node", B, "Learning / research", "25 min",
        "You follow 3 news sites and see the same story three times. This merges the feeds, removes duplicates and sends one clean list.",
        ["RSS Read node", "**Merge** node with 3 inputs (append mode)", "Code node: filter / map / sort / dedupe / reduce many items into one",
         "*On Error → Continue*: one broken feed shouldn't kill the run", "An IF guard so you don't get empty emails"],
        "Schedule ─┬─ RSS Google News ─┐\n          ├─ RSS TechCrunch  ─┼─ Merge → Code (filter/dedupe/sort) → IF count>0 → Gmail\n          └─ RSS The Verge   ─┘",
        ["Gmail OAuth2"],
        ["Add a Schedule Trigger and 3 **RSS Read** nodes, each connected to the trigger.",
         "On each RSS node: Settings → *On Error* → **Continue**.",
         "Add **Merge** → *Number of inputs* 3, and wire each feed to its own input.",
         "Add a **Code** node (*Run once for all items*) and paste the code. Read it line by line; each `.filter` / `.map` is one idea.",
         "Add an **IF** node: `count > 0`.",
         "Add Gmail on the true branch."],
        ["Run it and open the Code node output. `listText` is prepared for the AI version in L11.",
         "Replace one feed URL with a broken one. The workflow should still finish."],
        [("Merge waits forever or outputs nothing", "Every input must be connected. Check the numbered input dots on Merge."),
         ("All articles filtered out", "Some feeds use `pubDate` and not `isoDate`. The code handles both, so check your feed's field names.")],
        ["Add your own feeds (company blog, Hacker News `https://hnrss.org/frontpage`).", "Continue to **L11** to have Gemini summarise this."])
    write(root, w, r)


def L06(root):
    w = WF("L06-gmail-pdf-to-drive", "L06 · Save Gmail PDF attachments to Google Drive")
    w.note("## 📎 L06 · Gmail → Drive\nEvery 5 minutes: new unread mail with a PDF → upload to a Drive folder → **mark the email as read** so it is never processed twice.\n\nSet the Drive folder in *Upload to Drive*.", (-60, -300), 440, 220, 5)
    w.add("New Email with Attachment", "gmailTrigger", 1.2, {"pollTimes": {"item": [{"mode": "everyX", "value": 5, "unit": "minutes"}]},
        "simple": False, "filters": {"q": "has:attachment filename:pdf", "readStatus": "unread"},
        "options": {"downloadAttachments": True, "dataPropertyAttachmentsPrefixName": "attachment_"}}, (0, 0))
    w.add("Split PDF Attachments", "code", 2, {"jsCode":
        "// One email can carry many files. Output one item per PDF.\n"
        "const out = [];\n"
        "for (const item of $input.all()) {\n"
        "  for (const [key, bin] of Object.entries(item.binary || {})) {\n"
        "    const name = bin.fileName || key;\n"
        "    if (bin.mimeType === 'application/pdf' || name.toLowerCase().endsWith('.pdf')) {\n"
        "      const date = (item.json.date ? DateTime.fromISO(new Date(item.json.date).toISOString()) : $now).setZone($now.zoneName).toISODate();\n"
        "      out.push({ json: { fileName: `${date}_${name}`, from: item.json.from?.text || '', subject: item.json.subject || '', messageId: item.json.id }, binary: { data: bin } });\n"
        "    }\n"
        "  }\n"
        "}\n"
        "return out;"}, (220, 0))
    w.add("Upload to Drive", "googleDrive", 3, {"name": "={{ $json.fileName }}",
        "driveId": {"__rl": True, "mode": "list", "value": "My Drive"},
        "folderId": {"__rl": True, "mode": "url", "value": "PASTE_YOUR_DRIVE_FOLDER_URL"}, "options": {}}, (440, 0), retryOnFail=True)
    w.add("Mark Email as Read", "gmail", 2.1, {"operation": "markAsRead", "messageId": "={{ $('Split PDF Attachments').item.json.messageId }}"}, (660, 0))
    w.chain("New Email with Attachment", "Split PDF Attachments", "Upload to Drive", "Mark Email as Read")
    r = readme("L06", "Gmail PDF attachments → Google Drive", I, "Admin / finance", "20 min",
        "Invoices, bills, payslips and statements arrive as PDFs in email and get lost. This workflow files every PDF into one Drive folder with a date prefix, so you can find them at tax time.",
        ["Gmail Trigger (polling) with Gmail search filters", "Working with **binary data** (files) in n8n",
         "Splitting one email into many file items", "**Idempotency**: mark as read so the same email is never processed twice",
         "Google Drive upload into a folder"],
        "Gmail Trigger (every 5 min, unread + PDF) → Code (1 item per PDF) → Drive upload → Gmail mark as read",
        ["Gmail OAuth2", "Google Drive OAuth2 (the same Google Cloud project works, see docs/credentials.md)"],
        ["Add **Gmail Trigger**: poll every 5 minutes. Turn *Simplify* off. Filters: search `has:attachment filename:pdf`, read status *Unread*. Options: *Download attachments* on.",
         "Send yourself a test email with a PDF, then click *Fetch test event*. Look at the **Binary** tab of the output.",
         "Add the **Code** node: it loops over `item.binary` and emits one item per PDF.",
         "Add **Google Drive → Upload file**. Folder: paste your folder URL. File name: `{{ $json.fileName }}`.",
         "Add **Gmail → Mark as read** with `messageId` from the Code node.",
         "Activate it."],
        ["Email yourself 2 PDFs and 1 image. Exactly 2 files should appear in Drive.", "Check that the email is now read and that the next poll doesn't re-upload it."],
        [("Same file uploaded again and again", "This was the bug in the original version: nothing marked the email as read. Keep the last node."),
         ("No binary data", "*Download attachments* is off, or *Simplify* is on."),
         ("Drive 404 folder", "Use the folder URL, and make sure your Google account owns the folder.")],
        ["Route by sender: bank → /Bank, employer → /Payslips (use Switch).", "Use Gemini to read the PDF and rename it `2026-09 Airtel bill ₹799.pdf` (see L12)."])
    write(root, w, r)


def L07(root):
    w = WF("L07-lead-capture-sheets", "L07 · Lead capture form → Google Sheets + welcome email")
    w.note("## 📋 L07 · Forms + Sheets (Sales)\nOpen the **Form URL** from the trigger (Test URL while building, Production URL when active).\nCreate a Sheet with headers:\n`timestamp | name | email | company | interest | budget | source`", (-60, -300), 460, 220, 5)
    w.add("Lead Form", "formTrigger", 2.2, {"formTitle": "Book a free demo", "formDescription": "Tell us a little about you. We reply within one business day.",
        "formFields": {"values": [form_field("Name", required=True), form_field("Email", "email", True),
            form_field("Company"), form_field("Interested in", "dropdown", True, ["Automation consulting", "n8n training", "AI agents", "Other"]),
            form_field("Monthly budget (INR)", "dropdown", False, ["< 25k", "25k – 1L", "> 1L"])]},
        "options": {"respondWithOptions": {"values": {"formSubmittedText": "Thanks! Check your inbox for a confirmation."}}}}, (0, 0))
    w.add("Clean Lead", "set", 3.4, assign(timestamp="={{ $now.toISO() }}", name="={{ $json.Name.trim() }}",
        email="={{ $json.Email.trim().toLowerCase() }}", company="={{ $json.Company || '-' }}",
        interest="={{ $json['Interested in'] }}", budget="={{ $json['Monthly budget (INR)'] || 'not given' }}", source="web-form"), (220, 0))
    w.add("Append to Leads Sheet", "googleSheets", 4.5, sheet_append("Leads"), (440, 0))
    w.add("Welcome Email", "gmail", 2.1, gmail_send("={{ $('Clean Lead').item.json.email }}", "=Thanks {{ $('Clean Lead').item.json.name }} — your demo request",
        "=<p>Hi {{ $('Clean Lead').item.json.name }},</p><p>Thanks for your interest in <b>{{ $('Clean Lead').item.json.interest }}</b>. We'll reply within one business day with a few slots.</p><p>— Team</p>"), (660, 0))
    w.chain("Lead Form", "Clean Lead", "Append to Leads Sheet", "Welcome Email")
    r = readme("L07", "Lead capture form → Sheets → welcome email", I, "Sales / marketing", "20 min",
        "A small business or freelancer needs a *Contact us* form that stores the lead somewhere useful and replies instantly. No Typeform, no CRM subscription.",
        ["n8n **Form Trigger**: a hosted form with no web developer needed", "Cleaning input (trim, lowercase) in a Set node",
         "Google Sheets **Append row** with auto-mapped columns", "Sending a personalised email to the submitter"],
        "Form → Set (clean) → Google Sheets append → Gmail welcome",
        ["Google Sheets OAuth2", "Gmail OAuth2"],
        ["Create a Google Sheet named *Leads* with header row: `timestamp, name, email, company, interest, budget, source`.",
         "Add **n8n Form Trigger** with the 5 fields (Email field type = *Email*).",
         "Open the **Test URL**, submit once, and look at the output keys: they are the field labels.",
         "Add a **Set** node that renames and cleans the fields so they match your sheet headers exactly.",
         "Add **Google Sheets → Append row**. Paste the sheet URL, pick the tab, *Map automatically*.",
         "Add Gmail to `{{ $('Clean Lead').item.json.email }}`."],
        ["Submit the form 3 times with different data. You should see 3 rows and 3 emails.", "Activate it and share the **Production URL**."],
        [("Columns are empty in the sheet", "The header names don't exactly match the Set field names. Spaces and case matter."),
         ("The Test URL stops working", "Test URLs listen only while you click *Execute*. Use the Production URL once the workflow is active.")],
        ["Add a duplicate check: *Sheets → Get rows* filtered by email before appending.", "Score the lead with AI and route hot leads to Slack (see **L22**)."])
    write(root, w, r)


def L08(root):
    w = WF("L08-jira-stale-stories", "L08 · Daily stale Jira stories report")
    w.note("## 🧭 L08 · Jira for Scrum teams\nFinds In-Progress stories with no update for N days and emails the list.\nEdit the JQL in *Search Stale Stories* (project key!) and the days in **⚙️ Config**.", (-60, -300), 440, 220, 5)
    w.add("Weekdays 9 AM", "scheduleTrigger", 1.2, {"rule": {"interval": [{"field": "cronExpression", "expression": "0 9 * * 1-5"}]}}, (0, 0))
    w.add("⚙️ Config", "set", 3.4, assign(project_key="SCRUM", stale_days=3, email_to=EMAIL, jira_base_url="https://YOUR-SITE.atlassian.net"), (220, 0))
    w.add("Search Stale Stories", "jira", 1, {"operation": "getAll", "returnAll": True, "options": {
        "jql": "=project = {{ $json.project_key }} AND statusCategory = \"In Progress\" AND updated <= -{{ $json.stale_days }}d ORDER BY updated ASC",
        "fields": "summary,status,assignee,updated,priority"}}, (440, 0), alwaysOutputData=True)
    w.add("Build Report", "code", 2, {"jsCode":
        "const cfg = $('⚙️ Config').first().json;\n"
        "const issues = $input.all().map(i => i.json).filter(j => j && j.key);\n"
        "const days = d => Math.floor((Date.now() - Date.parse(d)) / 86400000);\n"
        "const rows = issues.map(i => {\n"
        "  const f = i.fields || {};\n"
        "  return { key: i.key, summary: f.summary, assignee: f.assignee?.displayName || 'Unassigned', status: f.status?.name, days: days(f.updated) };\n"
        "}).sort((a, b) => b.days - a.days);\n"
        "const tr = rows.map(r => `<tr><td><a href=\"${cfg.jira_base_url}/browse/${r.key}\">${r.key}</a></td><td>${r.summary}</td><td>${r.assignee}</td><td>${r.status}</td><td style=\"color:${r.days > 7 ? 'red' : 'inherit'}\">${r.days}</td></tr>`).join('');\n"
        "const byPerson = rows.reduce((m, r) => (m[r.assignee] = (m[r.assignee] || 0) + 1, m), {});\n"
        "const summary = Object.entries(byPerson).map(([p, n]) => `${p}: ${n}`).join(' · ');\n"
        "return [{ json: { count: rows.length,\n"
        "  subject: rows.length ? `⚠️ ${rows.length} stale stories in ${cfg.project_key}` : `✅ No stale stories in ${cfg.project_key}`,\n"
        "  html: rows.length ? `<p>${summary}</p><table border=1 cellpadding=6 style=\"border-collapse:collapse\"><tr><th>Key</th><th>Summary</th><th>Assignee</th><th>Status</th><th>Days idle</th></tr>${tr}</table>` : '<p>Everything moved in the last few days. 🎉</p>' } }];"}, (660, 0))
    w.add("Email Scrum Master", "gmail", 2.1, gmail_send("={{ $('⚙️ Config').item.json.email_to }}", "={{ $json.subject }}", "={{ $json.html }}"), (880, 0))
    w.chain("Weekdays 9 AM", "⚙️ Config", "Search Stale Stories", "Build Report", "Email Scrum Master")
    r = readme("L08", "Daily stale Jira stories report", I, "Agile / Scrum", "20 min",
        "Stories sit \"In Progress\" for days without anyone saying so at stand-up. A Scrum Master wants a list every weekday morning of what's stuck and who owns it, so the stand-up can start with it.",
        ["Jira Software node + **JQL** queries", "Cron expression for weekdays only (`0 9 * * 1-5`)",
         "`alwaysOutputData`: still send the ✅ email when Jira returns nothing", "Grouping and counting with `reduce`",
         "Conditional styling in HTML (red if more than 7 days)"],
        "Schedule (Mon–Fri 9 AM) → Config → Jira search (JQL) → Code (table + per-person count) → Gmail",
        ["Jira Software Cloud: email + API token from id.atlassian.com → Security → API tokens", "Gmail OAuth2"],
        ["Create an API token at https://id.atlassian.com/manage-profile/security/api-tokens and add a **Jira SW Cloud API** credential (domain + email + token).",
         "Schedule Trigger → *Custom (cron)* → `0 9 * * 1-5`.",
         "Config: project_key, stale_days, email_to, jira_base_url.",
         "**Jira → Issue → Get many**, Return all, Options → JQL. Test your JQL in Jira's own search first!",
         "Node Settings → **Always Output Data** on (so an empty result still continues).",
         "Code node builds the report, then Gmail."],
        ["Set `stale_days` to 0 so you see every in-progress story.", "Use a project key that doesn't exist. You should get a clear Jira error."],
        [("`JQL: field 'statusCategory' does not exist`", "On older Jira Server, use `status = \"In Progress\"`."),
         ("No email when there are no stale stories", "Turn on *Always Output Data* on the Jira node.")],
        ["Post it to the team Slack/Teams channel instead of email.", "Also comment on each stale issue: \"Any blockers? 🙂\"."])
    write(root, w, r)


def L09(root):
    w = WF("L09-webhook-expense-api", "L09 · Expense logger API (Webhook + validation + response)")
    w.note("## 🔌 L09 · Build your own API\nProtected by **Header Auth**: every call must send `X-API-Key`.\n```\ncurl -X POST <url> -H 'X-API-Key: <your key>' \\\n -H 'Content-Type: application/json' \\\n -d '{\"amount\":450,\"category\":\"food\"}'\n```\nNo/wrong key → 403 · invalid body → 400.", (-60, -360), 480, 260, 5)
    w.add("POST /expense", "webhook", 2, {"httpMethod": "POST", "path": "expense", "authentication": "headerAuth", "responseMode": "responseNode", "options": {}}, (0, 0))
    w.add("Validate", "code", 2, {"mode": "runOnceForEachItem", "jsCode":
        "const b = $json.body || {};\n"
        "const allowed = ['food', 'travel', 'office', 'software', 'other'];\n"
        "const errors = [];\n"
        "const amount = Number(b.amount);\n"
        "if (!Number.isFinite(amount) || amount <= 0) errors.push('amount must be a positive number');\n"
        "if (!allowed.includes(String(b.category || '').toLowerCase())) errors.push(`category must be one of ${allowed.join(', ')}`);\n"
        "return { json: { valid: errors.length === 0, errors,\n"
        "  row: { date: b.date || $today.toISODate(), amount, category: String(b.category || '').toLowerCase(), note: b.note || '', submitted_by: b.user || 'api' } } };"}, (220, 0))
    w.add("Valid?", "if", 2.2, {"conditions": conditions(cond("={{ $json.valid }}", "boolean", "true")), "options": {}}, (440, 0))
    w.add("Prepare Row", "set", 3.4, {"mode": "raw", "jsonOutput": "={{ JSON.stringify($json.row) }}", "options": {}}, (660, -100))
    w.add("Append to Expenses Sheet", "googleSheets", 4.5, sheet_append("Expenses"), (880, -100))
    w.add("201 Created", "respondToWebhook", 1.1, {"respondWith": "json", "responseBody": "={{ { ok: true, saved: $('Validate').item.json.row } }}", "options": {"responseCode": 201}}, (1100, -100))
    w.add("400 Bad Request", "respondToWebhook", 1.1, {"respondWith": "json", "responseBody": "={{ { ok: false, errors: $json.errors } }}", "options": {"responseCode": 400}}, (660, 120))
    w.chain("POST /expense", "Validate", "Valid?")
    w.link("Valid?", "Prepare Row", 0); w.link("Valid?", "400 Bad Request", 1)
    w.chain("Prepare Row", "Append to Expenses Sheet", "201 Created")
    r = readme("L09", "Expense logger API with Webhook", I, "Finance / developer", "25 min",
        "You want to log expenses from anywhere: an iPhone Shortcut, a Telegram bot, a Google Form or another app. A webhook turns n8n into your own small API with validation and proper HTTP status codes.",
        ["**Webhook** node (POST, JSON body in `$json.body`)", "**Header Auth**: never expose an unauthenticated webhook to the internet", "*Respond to Webhook* for custom status codes (201 / 400)",
         "Input validation in Code (*Run once for each item*)", "Set node in raw JSON mode", "Test URL and Production URL"],
        "Webhook POST /expense → Code validate → IF valid\n  ├─ true  → Set row → Sheets append → Respond 201\n  └─ false → Respond 400 {errors}",
        ["Google Sheets OAuth2", "Header Auth credential: name `X-API-Key`, value = a long random string (e.g. `openssl rand -hex 24`)"],
        ["Create a sheet tab *Expenses* with headers `date, amount, category, note, submitted_by`.",
         "Add **Webhook**: method POST, path `expense`, Respond = *Using 'Respond to Webhook' node*.",
         "Webhook → Authentication → **Header Auth** → create the credential (`X-API-Key` + random value). Unauthenticated calls are rejected with 403 before your workflow even runs.",
         "Click *Listen for test event*, then run the curl command from the sticky note using the **Test URL**.",
         "Add the **Validate** Code node (mode: *Run once for each item*).",
         "Add **IF** `valid is true`, then on the true branch Set (raw JSON) → Sheets append → **Respond to Webhook** (201).",
         "On the false branch, **Respond to Webhook** with 400."],
        ["`curl ... -H 'X-API-Key: <key>' -d '{\"amount\":450,\"category\":\"food\"}'` should return 201.", "`curl ... -H 'X-API-Key: <key>' -d '{\"amount\":-5,\"category\":\"pizza\"}'` should return 400 with 2 errors.",
         "The same call **without** the header should return 403.",
         "iPhone: Shortcuts app → *Get contents of URL* → POST JSON. That gives you a one-tap expense logger."],
        [("`Webhook node not correctly configured`", "Respond mode must be *Using Respond to Webhook node* when you use that node."),
         ("404 on the production URL", "The workflow isn't active. Test URLs use `/webhook-test/`, production uses `/webhook/`."),
         ("403 Forbidden", "The header name or value doesn't match the credential exactly (names are case-insensitive, values are not).")],
        ["Rotate the key: create a second credential, update clients, then delete the old one.", "Add a daily 9 PM summary: *Sheets get rows* → sum by category → email."])
    write(root, w, r)


def L10(root):
    w = WF("L10-form-bug-report-jira", "L10 · Bug report form → Jira issue + reporter confirmation")
    w.note("## 🐞 L10 · Form → Jira\nNon-technical users report bugs on a friendly form; n8n creates a proper Jira Bug with priority mapped from severity, then emails the reporter the ticket link.\nSet project and issue type IDs in *Create Jira Bug*.", (-60, -320), 480, 240, 5)
    w.add("Bug Report Form", "formTrigger", 2.2, {"formTitle": "Report a problem", "formDescription": "Found something broken? Tell us and we will track it.",
        "formFields": {"values": [form_field("Your email", "email", True), form_field("What is broken?", required=True, placeholder="Login button does nothing"),
            form_field("Steps to reproduce", "textarea", True), form_field("Severity", "dropdown", True, ["Blocker — cannot work", "Major — workaround exists", "Minor — cosmetic"]),
            form_field("Page / module")]}, "options": {}}, (0, 0))
    w.add("Map Severity → Priority", "code", 2, {"mode": "runOnceForEachItem", "jsCode":
        "const sev = $json['Severity'] || '';\n"
        "const priority = sev.startsWith('Blocker') ? 'Highest' : sev.startsWith('Major') ? 'High' : 'Low';\n"
        "return { json: { ...$json, priority,\n"
        "  summary: `[${$json['Page / module'] || 'General'}] ${$json['What is broken?']}`.slice(0, 250),\n"
        "  description: `*Reported by:* ${$json['Your email']}\\n*Severity:* ${sev}\\n\\n*Steps to reproduce:*\\n${$json['Steps to reproduce']}\\n\\n_Created automatically by n8n_` } };"}, (220, 0))
    w.add("Create Jira Bug", "jira", 1, {"project": {"__rl": True, "mode": "id", "value": "REPLACE_PROJECT_ID"},
        "issueType": {"__rl": True, "mode": "id", "value": "REPLACE_BUG_ISSUE_TYPE_ID"}, "summary": "={{ $json.summary }}",
        "additionalFields": {"description": "={{ $json.description }}", "labels": ["from-form"]}}, (440, 0))
    w.add("Confirm to Reporter", "gmail", 2.1, gmail_send("={{ $('Map Severity → Priority').item.json['Your email'] }}",
        "=We logged your report: {{ $json.key }}",
        "=<p>Thanks! Your report is now ticket <b>{{ $json.key }}</b> with priority {{ $('Map Severity → Priority').item.json.priority }}.</p><p>We'll update you when it's fixed.</p>"), (660, 0))
    w.chain("Bug Report Form", "Map Severity → Priority", "Create Jira Bug", "Confirm to Reporter")
    r = readme("L10", "Bug report form → Jira issue", I, "Agile / product support", "20 min",
        "Users, testers and business teams report bugs in chat and email, and half the details are missing. A structured form creates a proper Jira Bug with priority set, and the reporter gets the ticket number straight away.",
        ["Form fields with dropdowns and validation", "Mapping business language to system values (Severity → Priority)",
         "Jira **Create issue** with labels", "Using the output of a *create* call (`$json.key`) in the next step"],
        "Form → Code (map severity, build summary) → Jira create Bug → Gmail confirmation with ticket key",
        ["Jira Software Cloud API token", "Gmail OAuth2"],
        ["Find your project ID and Bug issue type ID. In the Jira node, switch the fields to *From list* and pick them, which fills the IDs.",
         "Build the form with 5 fields.",
         "Add a Code node (*for each item*) that builds `summary`, `description` and `priority`.",
         "Add **Jira → Issue → Create**. Add labels `from-form`. (Priority needs your Jira priority IDs; add it under *Additional fields* once you know them.)",
         "Add Gmail using `{{ $json.key }}` from the Jira output."],
        ["Submit a Blocker bug. Check that the Jira issue exists and that the email shows the key."],
        [("`issuetype: Specify a valid issue type`", "Team-managed and company-managed projects use different issue-type IDs. Pick them from the list."),
         ("Description formatting looks odd", "Jira Cloud v3 uses ADF, and n8n converts plain text. Keep it simple, or use the Jira REST API via HTTP for rich text.")],
        ["Accept a screenshot upload (form *File* field) and attach it to the issue.", "Let AI detect duplicates before creating the issue (L14 agent + Jira search tool)."])
    write(root, w, r)


ALL = [L01, L02, L03, L04, L05, L06, L07, L08, L09, L10]
