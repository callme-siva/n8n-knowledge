import json, os, copy
from lib import *

A = "🟠 AI"
P = "🔴 Multi-agent & production"


# ---------- converter for the team's original workflows ----------
def convert(slug, name, note, note_pos=(-60, -380), fixups=None):
    """Re-normalise an already-sanitised community workflow (idempotent)."""
    d = json.load(open(os.path.join(os.path.dirname(__file__), "..", "workflows", slug, "workflow.json")))
    w = WF(slug, name)
    for n in d["nodes"]:
        if n["type"].endswith("stickyNote"):
            continue
        n = copy.deepcopy(n)
        for k in ("credentials", "webhookId", "notesInFlow", "notes"):
            n.pop(k, None)
        if n["type"].endswith("lmChatOpenAi"):
            temp = n["parameters"].get("options", {}).get("temperature", 0.2)
            n["type"], n["typeVersion"] = "@n8n/n8n-nodes-langchain.lmChatGoogleGemini", 1
            n["parameters"] = {"modelName": GEMINI_MODEL, "options": {"temperature": temp}}
        if n["type"].endswith("lmChatGoogleGemini"):
            n["typeVersion"] = 1
            n["parameters"] = {"modelName": GEMINI_MODEL, "options": n["parameters"].get("options", {})}
        if n["type"].endswith(".gmail"):
            to = n["parameters"].get("sendTo", "")
            if "@" in to and not to.startswith("="):
                n["parameters"]["sendTo"] = EMAIL
        w.nodes.append(n)
    w.conns = d["connections"]
    if fixups:
        fixups(w)
    w.note(note, note_pos, 520, 300, 5)
    return w


def node(w, name):
    return next(n for n in w.nodes if n["name"] == name)


# ---------- L11 ----------
def L11(root):
    w = WF("L11-ai-news-digest-llm-chain", "L11 · AI news briefing (Basic LLM Chain + Gemini)")
    w.note("## 🤖 L11 · Your first LLM call\nSame pipeline as L05, but **Gemini** turns 25 headlines into a 5-bullet executive briefing.\nFree Gemini key: aistudio.google.com → Get API key.", (-60, -420), 460, 220, 5)
    w.add("Every Morning 8 AM", "scheduleTrigger", 1.2, {"rule": {"interval": [{"triggerAtHour": 8}]}}, (0, 0))
    feeds = [("Google News · AI", "https://news.google.com/rss/search?q=artificial+intelligence+when:1d&hl=en-IN&gl=IN&ceid=IN:en"),
             ("TechCrunch · AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
             ("The Verge · AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml")]
    w.add("Merge Feeds", "merge", 3, {"numberInputs": 3}, (480, 0))
    for i, (n, u) in enumerate(feeds):
        w.add(n, "rssFeedRead", 1.1, {"url": u, "options": {}}, (240, -160 + i * 160), onError="continueRegularOutput")
        w.link("Every Morning 8 AM", n); w.link(n, "Merge Feeds", inp=i)
    # reuse the exact L05 Code node (single source of truth)
    src = json.load(open(os.path.join(root, "workflows", "L05-rss-news-code-node", "workflow.json")))
    code = next(n for n in src["nodes"] if n["name"] == "Filter · Dedupe · Sort")["parameters"]
    w.add("Filter · Dedupe · Sort", "code", 2, code, (700, 0))
    w.lc("Write Briefing", "chainLlm", 1.5, {"promptType": "define",
        "text": "=Here are today's AI news headlines ({{ $json.count }} items):\n\n{{ $json.listText }}",
        "messages": {"messageValues": [{"message":
            "You are a news editor writing for busy professionals in India. From the headlines, write:\n"
            "1. **Top 5 stories**: one bullet each, max 2 sentences: what happened + why it matters. Include the link.\n"
            "2. **One-line trend of the day.**\n"
            "Rules: merge duplicates, skip clickbait, never invent facts beyond the headline. Output clean HTML (<h3>, <ul>, <li>, <a>), no markdown."}]}},
        (920, 0))
    w.gemini("Gemini", (920, 200), 0.3)
    w.add("Email Briefing", "gmail", 2.1, gmail_send(EMAIL, "=☕ AI briefing · {{ $now.toFormat('dd LLL yyyy') }}",
        "={{ $json.text }}<hr><details><summary>All {{ $('Filter · Dedupe · Sort').item.json.count }} headlines</summary>{{ $('Filter · Dedupe · Sort').item.json.html }}</details>"), (1160, 0))
    w.chain("Merge Feeds", "Filter · Dedupe · Sort", "Write Briefing", "Email Briefing")
    w.ai("Gemini", "Write Briefing", "ai_languageModel")
    r = readme("L11", "AI news briefing with a Basic LLM Chain", A, "Learning / research", "20 min",
        "25 headlines is still too many to read. An LLM can turn them into 5 bullets that say *why each story matters*, which is what a good executive briefing does.",
        ["Basic LLM Chain node: prompt in, text out", "Connecting a **Chat Model sub-node** (Gemini)",
         "Writing a system prompt with rules and an output format", "Temperature: 0.3 for factual summaries",
         "Keeping the raw data in the email as a fallback, so the AI never hides the source"],
        "Schedule → 3× RSS → Merge → Code (from L05) → LLM Chain ⇐ Gemini → Gmail",
        ["Google Gemini (PaLM) API key: free at https://aistudio.google.com/app/apikey", "Gmail OAuth2"],
        ["Start from your finished **L05** (duplicate it).",
         "Get a Gemini API key from AI Studio. In n8n, create a *Google Gemini(PaLM) Api* credential (host is the default).",
         "Between Code and Gmail, add **Basic LLM Chain**. Prompt = *Define below*, and put `{{ $json.listText }}` in the prompt.",
         "Click **+ Chat Model** under the chain and choose **Google Gemini Chat Model** → `gemini-2.5-flash`.",
         "Add a *System* message (Chat Messages → System) with the editor rules.",
         "Gmail body = `{{ $json.text }}`."],
        ["Run it and compare the briefing to the raw headlines. Did the model invent anything?", "Change the system prompt to *Explain like I'm a school student* and run it again."],
        [("429 / quota exceeded", "The free tier has per-minute limits. Wait a minute, or use `gemini-2.5-flash-lite`."),
         ("Output shows ```html fences", "Add \"no code fences\" to the prompt, or strip them with `.replace(/```html|```/g,'')`.")],
        ["Ask for JSON and render your own template (this previews L12).", "Send it to Telegram as a morning message."])
    write(root, w, r)


# ---------- L12 ----------
def L12(root):
    def fix(w):
        s = node(w, "Append RAID to Sheet")["parameters"]
        s["documentId"] = {"__rl": True, "mode": "url", "value": "PASTE_YOUR_GOOGLE_SHEET_URL"}
        s["sheetName"] = {"__rl": True, "mode": "name", "value": "RAID"}
    w = convert("L12-meeting-transcript-raid-log",
        "L12 · Meeting transcript → RAID log (Structured Output)",
        "## 🧩 L12 · Structured output\nPaste a meeting transcript → Gemini returns **JSON that follows a schema** → one Sheet row per Risk / Assumption / Issue / Dependency.\n\nThis is the most useful AI pattern in business: *unstructured text → rows*.", fixups=fix)
    r = readme("L12", "Meeting transcript → RAID log", A, "Project management", "30 min",
        "After a steering committee or status meeting, someone should update the RAID log. Usually nobody does. Paste the transcript (from Teams, Zoom or Meet) and every risk, assumption, issue and dependency lands in a sheet with owner, impact and due date.",
        ["**Structured Output Parser**: force the LLM to follow a JSON schema", "`hasOutputParser` on the LLM Chain",
         "**Split Out**: one AI answer → many items", "Mapping AI fields to spreadsheet columns"],
        "Form (transcript) → LLM Chain ⇐ Gemini, ⇐ Structured Parser → Split Out items → Set row → Sheets append",
        ["Google Gemini API key", "Google Sheets OAuth2"],
        ["Create a Sheet tab **RAID** whose headers match the fields in *Build RAID Row*.",
         "Form Trigger: meeting title, date, transcript (textarea).",
         "**Basic LLM Chain** → turn on *Require Specific Output Format* → attach a **Structured Output Parser** and paste an example JSON (`items: [{category, description, owner, impact, ...}]`).",
         "Attach the Gemini model.",
         "**Split Out** on `output.items`.",
         "**Set** the row columns, then **Sheets → Append**."],
        ["Paste a sample transcript from [docs/sample-data.md](../../docs/sample-data.md#meeting-transcript).",
         "Check that every row has a category from Risk/Assumption/Issue/Dependency and nothing else."],
        [("`Model output doesn't fit required format`", "Lower the temperature to 0, simplify the schema example, or turn on auto-fix (L17 shows this)."),
         ("Only one row appears", "Split Out must point to the array path, `output.items`.")],
        ["Email the owner of each high-impact risk.", "Run it over every transcript file dropped in a Drive folder."])
    write(root, w, r)


# ---------- L13 RAG ----------
def L13(root):
    w = WF("L13-rag-policy-chatbot", "L13 · HR policy chatbot (RAG over your PDFs)")
    w.note("## 📚 L13 · RAG = Retrieval-Augmented Generation\n**Part A (top):** upload PDFs → split → embed → store.\n**Part B (bottom):** chat → agent searches the store → answers *with sources*.\n\nIn-memory store = perfect for learning; resets on restart. Production: swap for Supabase/Pinecone/Qdrant.", (-60, -520), 520, 260, 5)
    w.add("Upload Policy PDFs", "formTrigger", 2.2, {"formTitle": "Upload policy documents", "formDescription": "PDFs only. They will be indexed for the chatbot.",
        "formFields": {"values": [{"fieldLabel": "Documents", "fieldType": "file", "acceptFileTypes": ".pdf", "requiredField": True}]}, "options": {}}, (0, -200))
    w.lc("Store in Vector DB", "vectorStoreInMemory", 1.1, {"mode": "insert", "memoryKey": "hr_policies"}, (260, -200))
    w.lc("Gemini Embeddings (insert)", "embeddingsGoogleGemini", 1, {"modelName": EMBED_MODEL}, (200, -20))
    w.lc("PDF Loader", "documentDefaultDataLoader", 1, {"dataType": "binary", "options": {}}, (380, -20))
    w.lc("Chunker", "textSplitterRecursiveCharacterTextSplitter", 1, {"chunkSize": 1000, "chunkOverlap": 150, "options": {}}, (460, 140))
    w.link("Upload Policy PDFs", "Store in Vector DB")
    w.ai("Gemini Embeddings (insert)", "Store in Vector DB", "ai_embedding")
    w.ai("PDF Loader", "Store in Vector DB", "ai_document")
    w.ai("Chunker", "PDF Loader", "ai_textSplitter")
    w.lc("Chat with Employees", "chatTrigger", 1.1, {"options": {}}, (0, 360))
    w.lc("Policy Assistant", "agent", 2.2, {"options": {"systemMessage":
        "You are the HR policy assistant. ALWAYS search the policy_documents tool before answering. "
        "Answer only from what the tool returns; quote the policy name. If the documents don't cover it, say "
        "\"I couldn't find that in our policies — please contact HR\" — never guess. Keep answers under 120 words."}}, (260, 360))
    w.gemini("Gemini Chat", (160, 560), 0.1)
    w.lc("Chat Memory", "memoryBufferWindow", 1.3, {"contextWindowLength": 8}, (300, 560))
    w.lc("policy_documents", "vectorStoreInMemory", 1.1, {"mode": "retrieve-as-tool", "toolName": "policy_documents",
        "toolDescription": "Search the company HR policy documents (leave, WFH, travel, reimbursement, code of conduct).", "memoryKey": "hr_policies", "topK": 4}, (460, 560))
    w.lc("Gemini Embeddings (search)", "embeddingsGoogleGemini", 1, {"modelName": EMBED_MODEL}, (460, 740))
    w.link("Chat with Employees", "Policy Assistant")
    w.ai("Gemini Chat", "Policy Assistant", "ai_languageModel")
    w.ai("Chat Memory", "Policy Assistant", "ai_memory")
    w.ai("policy_documents", "Policy Assistant", "ai_tool")
    w.ai("Gemini Embeddings (search)", "policy_documents", "ai_embedding")
    r = readme("L13", "HR policy chatbot with RAG", A, "HR / internal support", "35 min",
        "Employees keep asking HR the same questions (\"How many casual leaves do I get?\", \"Is my broadband reimbursed?\") when the answer is already in a 40-page PDF. RAG lets a chatbot answer from *your* documents, not from what the model remembers from the internet.",
        ["The RAG idea: **chunk → embed → store → retrieve → answer**", "Embeddings with Gemini (`gemini-embedding-001`)",
         "Vector store *insert* mode vs *retrieve-as-tool* mode", "AI Agent + tool + memory", "Grounding prompts that stop the model from guessing"],
        "PART A  Form (PDF upload) → Vector Store insert ⇐ Embeddings, ⇐ Loader ⇐ Chunker\nPART B  Chat Trigger → AI Agent ⇐ Gemini, ⇐ Memory, ⇐ Tool: Vector Store (retrieve) ⇐ Embeddings",
        ["Google Gemini API key (used for chat and embeddings)"],
        ["**Part A**: Form Trigger with a *File* field (accept `.pdf`).",
         "Add **In-Memory Vector Store**, mode *Insert Documents*, memory key `hr_policies`.",
         "Attach **Embeddings Google Gemini** + **Default Data Loader** (type *Binary*) + **Recursive Character Text Splitter** (1000 / 150).",
         "Open the form, upload a policy PDF, and check how many chunks were inserted.",
         "**Part B**: add a **Chat Trigger** → **AI Agent**. Attach Gemini, **Window Buffer Memory**, and a second **In-Memory Vector Store** in *Retrieve documents (as tool)* mode with the **same memory key** and its own embeddings node.",
         "Write the strict system prompt (see workflow.json).",
         "Click **Open chat** and ask a question."],
        ["Use the sample policy in [docs/sample-data.md](../../docs/sample-data.md#hr-policy) (save it as a PDF).",
         "Ask something that *isn't* in the policy (\"What's the CEO's salary?\"). It must refuse.",
         "Open the agent's execution log to see which chunks were retrieved."],
        [("The agent answers without searching", "Make the tool description specific and say \"ALWAYS search\" in the system prompt."),
         ("Nothing found after restarting n8n", "In-memory storage is wiped on restart. Re-upload, or move to a persistent vector DB."),
         ("Embedding dimension mismatch", "Use the *same* embedding model for insert and search.")],
        ["Swap in Supabase / Qdrant / Pinecone for persistent storage.", "Serve it inside Slack or Teams instead of n8n chat.", "Add a Google Drive trigger so new policies index themselves."])
    write(root, w, r)


# ---------- L14 agent with tools ----------
def L14(root):
    w = WF("L14-ai-agent-with-tools", "L14 · Personal assistant agent (tools + memory)")
    w.note("## 🛠️ L14 · Agents decide which tool to call\nTools here: 🌦️ weather (HTTP), 🧮 calculator, 📖 Wikipedia, 💱 currency (HTTP).\nTry: *\"Is it rainy in Pune tomorrow and what's 18% GST on ₹12,499?\"*\nWatch the **Logs** panel to see each tool call.", (-60, -440), 500, 240, 5)
    w.lc("Chat", "chatTrigger", 1.1, {"options": {}}, (0, 0))
    w.lc("Assistant Agent", "agent", 2.2, {"options": {"systemMessage":
        "=You are a helpful personal assistant for a user in India. Today is {{ $now.toFormat('cccc, dd LLL yyyy') }}. "
        "Use tools for any fact that can change (weather, exchange rates) and the calculator for ANY arithmetic. "
        "For weather you need latitude/longitude — use your own knowledge of city coordinates. Be concise.", "maxIterations": 8}}, (260, 0))
    w.gemini("Gemini", (0, 240), 0.2)
    w.lc("Memory", "memoryBufferWindow", 1.3, {"contextWindowLength": 10}, (140, 240))
    w.lc("Calculator", "toolCalculator", 1, {}, (280, 240))
    w.lc("Wikipedia", "toolWikipedia", 1, {}, (400, 240))
    w.lc("get_weather", "toolHttpRequest", 1.1, {"toolDescription": "Get current weather and 3-day forecast for a location. Needs latitude and longitude.",
        "url": "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&forecast_days=3&timezone=auto",
        "placeholderDefinitions": {"values": [{"name": "lat", "description": "latitude in decimal degrees", "type": "number"},
                                              {"name": "lon", "description": "longitude in decimal degrees", "type": "number"}]},
        "optimizeResponse": True}, (520, 240))
    w.lc("get_exchange_rate", "toolHttpRequest", 1.1, {"toolDescription": "Get latest exchange rates for a base currency code like USD, EUR, INR.",
        "url": "https://open.er-api.com/v6/latest/{base}",
        "placeholderDefinitions": {"values": [{"name": "base", "description": "3-letter ISO currency code", "type": "string"}]},
        "optimizeResponse": True, "dataField": "rates", "fieldsToInclude": "all"}, (640, 240))
    w.link("Chat", "Assistant Agent")
    w.ai("Gemini", "Assistant Agent", "ai_languageModel"); w.ai("Memory", "Assistant Agent", "ai_memory")
    for t in ("Calculator", "Wikipedia", "get_weather", "get_exchange_rate"):
        w.ai(t, "Assistant Agent", "ai_tool")
    r = readme("L14", "Personal assistant agent with tools", A, "Personal productivity", "30 min",
        "A plain LLM can't know today's weather and often gets arithmetic wrong. An **agent** can call tools. It reads the question, picks the right tool, calls it, and writes the answer from the result.",
        ["AI Agent node (tools agent)", "Built-in tools: Calculator, Wikipedia", "**HTTP Request Tool** with `{placeholders}` the model fills in",
         "Window Buffer Memory for multi-turn chat", "Tool descriptions are prompts: write them carefully", "Max iterations as a safety limit"],
        "Chat → AI Agent ⇐ Gemini, ⇐ Memory, ⇐ Calculator, ⇐ Wikipedia, ⇐ get_weather (HTTP), ⇐ get_exchange_rate (HTTP)",
        ["Google Gemini API key (all tools used here are free and keyless)"],
        ["Chat Trigger → **AI Agent**.", "Attach Gemini + Window Buffer Memory.",
         "Attach **Calculator** and **Wikipedia** tools.",
         "Attach **HTTP Request Tool**: name `get_weather`, URL with `{lat}` and `{lon}` placeholders, and define both placeholders.",
         "Attach a second HTTP tool, `get_exchange_rate`, with a `{base}` placeholder.",
         "Write a system prompt that tells the agent *when* to use tools."],
        ["\"What's 17.5% of 84,999?\" should use Calculator.", "\"Weather in Bengaluru?\" should use get_weather with about 12.97, 77.59.",
         "\"Who founded Infosys?\" should use Wikipedia.", "Follow-up: \"and in USD?\" tests memory and the currency tool."],
        [("The agent answers from memory and skips tools", "Make the system prompt stricter (\"ALWAYS use…\") and set a lower temperature."),
         ("`Too many iterations`", "The tool keeps failing. Open the Logs panel to see the tool error."),
         ("Huge tool responses / token errors", "Turn on *Optimize Response* on HTTP tools and pick only the fields you need.")],
        ["Add a Google Calendar tool (\"what's on my calendar tomorrow?\").", "Add a Gmail tool, but put an approval step in front of it (L15)."])
    write(root, w, r)


# ---------- L15 human in the loop ----------
def L15(root):
    w = WF("L15-retro-ai-approval-jira", "L15 · Retrospective → AI action items → human approval → Jira")
    w.note("## ✋ L15 · Human-in-the-loop\nAI drafts the action items, but **a human approves** before anything is created in Jira.\nGmail *Send and Wait for Response* pauses the execution until the Scrum Master clicks Approve / Decline.", (-60, -420), 500, 240, 5)
    w.add("Retrospective Form", "formTrigger", 2.2, {"formTitle": "Sprint Retrospective", "formDescription": "Honest, blameless feedback. Takes 2 minutes.",
        "formFields": {"values": [form_field("Sprint", required=True, placeholder="Sprint 24"), form_field("What went well?", "textarea"),
            form_field("What didn't go well?", "textarea"), form_field("Suggestions", "textarea"),
            form_field("Team morale", "dropdown", True, ["1 - Very low", "2 - Low", "3 - Neutral", "4 - Good", "5 - Excellent"])]}, "options": {}}, (0, 0))
    w.lc("Analyze Retro", "chainLlm", 1.5, {"promptType": "define", "hasOutputParser": True,
        "text": "=Sprint: {{ $json.Sprint }}\nMorale: {{ $json['Team morale'] }}\n\nWent well:\n{{ $json['What went well?'] }}\n\nDidn't go well:\n{{ $json[\"What didn't go well?\"] }}\n\nSuggestions:\n{{ $json.Suggestions }}",
        "messages": {"messageValues": [{"message": "You are an experienced agile coach. Summarise the feedback, rate sentiment, and propose at most 3 SMART action items (specific, owner role, measurable). Only include items the team can act on next sprint."}]}}, (240, 0))
    w.gemini("Gemini", (180, 200), 0.2)
    w.lc("Retro Schema", "outputParserStructured", 1.2, {"jsonSchemaExample": json.dumps({
        "sentiment": "mixed", "summary": "Delivery was good but too many unplanned requests.",
        "action_items": [{"title": "Limit mid-sprint scope changes", "description": "PO to route new requests to the backlog; SM tracks count.", "priority": "High", "owner_role": "Product Owner"}]}, indent=2)}, (340, 200))
    w.add("Build Approval Message", "code", 2, {"jsCode":
        "const o = $input.first().json.output;\n"
        "const li = (o.action_items || []).map((a, i) => `<li><b>${i + 1}. ${a.title}</b> (${a.priority}, ${a.owner_role})<br>${a.description}</li>`).join('');\n"
        "return [{ json: { ...o, sprint: $('Retrospective Form').first().json.Sprint,\n"
        "  html: `<p><b>Sentiment:</b> ${o.sentiment}</p><p>${o.summary}</p><p>Proposed Jira tasks:</p><ol>${li}</ol><p>Approve to create them in Jira.</p>` } }];"}, (560, 0))
    w.add("Ask Scrum Master", "gmail", 2.1, {"operation": "sendAndWait", "sendTo": EMAIL,
        "subject": "=Approve retro action items for {{ $json.sprint }}?", "message": "={{ $json.html }}",
        "approvalOptions": {"values": {"approvalType": "double"}}, "options": {"limitWaitTime": {"values": {"limitType": "afterTimeInterval", "resumeAmount": 2, "resumeUnit": "days"}}}}, (780, 0))
    w.add("Approved?", "if", 2.2, {"conditions": conditions(cond("={{ $json.data.approved }}", "boolean", "true")), "options": {}}, (1000, 0))
    w.add("Restore Items", "code", 2, {"jsCode": "return $('Build Approval Message').first().json.action_items.map(a => ({ json: { ...a, sprint: $('Build Approval Message').first().json.sprint } }));"}, (1220, -100))
    w.add("Create Jira Task", "jira", 1, {"project": {"__rl": True, "mode": "id", "value": "REPLACE_PROJECT_ID"},
        "issueType": {"__rl": True, "mode": "id", "value": "REPLACE_TASK_ISSUE_TYPE_ID"}, "summary": "=[Retro {{ $json.sprint }}] {{ $json.title }}",
        "additionalFields": {"description": "={{ $json.description }}\n\nOwner role: {{ $json.owner_role }}\nPriority suggested by AI: {{ $json.priority }}\n\nApproved by Scrum Master via n8n.", "labels": ["retro-action"]}}, (1440, -100))
    w.add("Declined — stop", "noOp", 1, {}, (1220, 120))
    w.chain("Retrospective Form", "Analyze Retro", "Build Approval Message", "Ask Scrum Master", "Approved?")
    w.link("Approved?", "Restore Items", 0); w.link("Approved?", "Declined — stop", 1)
    w.link("Restore Items", "Create Jira Task")
    w.ai("Gemini", "Analyze Retro", "ai_languageModel"); w.ai("Retro Schema", "Analyze Retro", "ai_outputParser")
    r = readme("L15", "Retrospective → AI action items → human approval → Jira", A, "Agile / Scrum", "35 min",
        "AI is good at turning messy retro notes into clear action items. But you don't want it filling Jira with junk tickets on its own. The Scrum Master gets an email with the proposal and clicks **Approve** or **Decline**, and only approved items become tasks.",
        ["**Send and Wait for Response**: pause a workflow for a human decision", "Wait time limits (auto-timeout after 2 days)",
         "Structured output for a list of action items", "Keeping data across a pause: `$('Node').first()`",
         "Responsible-AI design: the AI proposes and a human decides"],
        "Form → LLM Chain ⇐ Gemini, ⇐ Schema → Code (HTML) → Gmail send-and-wait ⏸ → IF approved\n   ├─ yes → one item per action → Jira create task\n   └─ no  → stop",
        ["Google Gemini API key", "Gmail OAuth2", "Jira Software Cloud API token"],
        ["Build the form (sprint, 3 textareas, morale dropdown).",
         "**Basic LLM Chain** + Gemini + **Structured Output Parser** with the example JSON.",
         "Code: build an HTML summary for the approver.",
         "**Gmail → Send and Wait for Response**, response type *Approval*, *Approve and Disapprove* buttons. Limit the wait to 2 days.",
         "**IF** `{{ $json.data.approved }}` is true.",
         "Code: turn `action_items` back into items, then **Jira → Create issue** for each one."],
        ["Submit a retro from [docs/sample-data.md](../../docs/sample-data.md#retro-feedback). You should get an approval email and see the execution *Waiting*.",
         "Click **Approve**: 1–3 Jira tasks should appear. Try again and click **Decline**: no tasks."],
        [("Approval link opens an error page", "Your n8n must be reachable from where you click. Set `WEBHOOK_URL` if you self-host behind a tunnel or domain."),
         ("`approved` is undefined", "Check the output of the Gmail node. The decision lives in `data.approved`.")],
        ["Collect retros from the whole team for a week, then analyse all of them together (Aggregate node).", "Post the approval to Slack instead (the Slack node also has *Send and Wait*)."])
    write(root, w, r)


# ---------- L16–L18: team originals, converted ----------
def L16(root):
    def fix(w):
        cfg = node(w, "Config")["parameters"]["assignments"]["assignments"]
        for a in cfg:
            if a["name"] == "org":
                a["value"] = "https://github.com/YOUR_GITHUB_USER_OR_ORG"
            if isinstance(a.get("value"), str) and "@" in a["value"]:
                a["value"] = EMAIL
        t = node(w, "Weekdays 9 AM")
        t["parameters"] = {"rule": {"interval": [{"field": "cronExpression", "expression": "0 9 * * 1-5"}]}}
    w = convert("L16-sprint-report-multi-agent",
        "L16 · Sprint progress report (4 cooperating agents)",
        "## 👥 L16 · Multi-agent pipeline\nGitHub Projects (GraphQL) → metrics → **Capacity → Backlog → Burndown → Coordinator** agents, each reading the previous agent's output.\nSet `org` and `projectNumber` in **Config**.", fixups=fix)
    r = readme("L16", "Sprint progress report with 4 cooperating agents", P, "Agile / engineering management", "45 min",
        "A delivery lead needs one daily email: is the sprint on track, who is overloaded, is the backlog healthy? Each question needs a different lens, so one specialist agent handles each lens and a coordinator writes the final report.",
        ["GitHub **GraphQL** API via HTTP Request", "Computing metrics in code *before* the LLM sees them (cheaper, and no maths mistakes)",
         "**Sequential multi-agent** pattern: each agent reads the metrics plus the earlier agents' notes", "A coordinator agent that merges the specialists' output into one report"],
        "Schedule → Config → Code (GraphQL query) → HTTP POST api.github.com/graphql → Code (metrics)\n → Capacity agent → Backlog agent → Burndown agent → Coordinator agent → Gmail",
        ["GitHub API token (classic PAT with `read:project`, `repo`)", "Google Gemini API key", "Gmail OAuth2"],
        ["Create a GitHub Project (v2) with Status, Estimate and Iteration fields, and add some issues.",
         "Create a GitHub credential with a PAT.",
         "Config: `org` (your user/org URL), `projectNumber`, recipient email.",
         "Import this workflow and run it up to *Compute Sprint Metrics*. Read the metrics JSON before any AI step runs.",
         "Run the full chain and read each agent's output in order."],
        ["Change a few issue statuses in GitHub, run it again, and compare the burndown text."],
        [("GraphQL `Could not resolve to a ProjectV2`", "Wrong project number, or it's a user project and the query expects an org. The code handles both, so check `org`."),
         ("The report contradicts the metrics", "Lower the temperature, and tell agents to quote the numbers from the JSON.")],
        ["Swap GitHub for Jira (Jira node, sprint JQL).", "Run the three specialist agents in **parallel** and merge them, which is faster."])
    write(root, w, r)


def L17(root):
    w = convert("L17-complaint-handler-multi-agent",
        "L17 · Customer complaint handler (5 agents + auto-fixing parsers)",
        "## 🎧 L17 · Production-style AI pipeline\nUnderstand → Investigate → Resolve → Escalate? → Draft reply.\nEvery agent returns **validated JSON**; each parser has its own *fix model* that repairs bad JSON automatically.\n⚠️ Add a human approval (L15) before auto-sending in real life.")
    r = readme("L17", "Customer complaint handler (5 agents)", P, "Customer support", "45 min",
        "Support teams spend the first 10 minutes of every complaint just working out what it is. This pipeline classifies it (category, urgency, sentiment), investigates, proposes a resolution and a goodwill gesture, decides whether to escalate, and drafts an empathetic reply.",
        ["Chained agents, each with its **own schema**", "**Auto-fixing output parser** (a second model repairs malformed JSON)",
         "Referencing any earlier step: `$('Understand Complaint').item.json.output`", "Designing escalation rules as explicit JSON (`escalate`, `priority`, `route_to`)"],
        "Form → Understand ⇐(model, schema⇐fix model) → Investigate ⇐… → Resolve ⇐… → Escalate? ⇐… → Draft reply ⇐model → Gmail",
        ["Google Gemini API key", "Gmail OAuth2"],
        ["Import it and connect the Gemini credential. There are 10 model nodes: select them all and set the credential once.",
         "Open the form and submit a complaint from [docs/sample-data.md](../../docs/sample-data.md#customer-complaints).",
         "Click each agent in the execution and read its `output`. Look at how context builds up.",
         "Change the email node to send to **yourself** while testing."],
        ["Try an angry high-value complaint (it should escalate) and a mild one (it shouldn't)."],
        [("`Could not parse LLM output`", "The fix model is supposed to catch this. Check that each *Fix Model* is connected to its parser."),
         ("It emails real customers during testing", "Put your own email in *Send Response Email* until you're ready.")],
        ["Add a real order lookup tool (Google Sheets or your DB) to the Investigate agent.", "Route escalations to a Slack channel and a Jira Service Management ticket.",
         "Insert an approval step (L15) before *Send Response Email*."])
    write(root, w, r)


def L18(root):
    w = convert("L18-resume-job-fit-multi-agent",
        "L18 · Resume ↔ job fit analyser (4 specialist agents)",
        "## 📄 L18 · Document AI + specialists\nUpload a PDF resume + paste a job description → Analyst, Fit Scorer, Interview Coach and Learning-Plan agents → one email report.")
    r = readme("L18", "Resume ↔ job fit analyser", P, "Career / HR / recruiting", "35 min",
        "Job seekers want to know *\"Am I a fit, and what should I prepare?\"*. Recruiters want a quick first screen. The same workflow answers both: it extracts the resume text, scores the fit, lists the gaps, drafts likely interview questions and builds a learning plan.",
        ["**Extract From File** (PDF → text)", "Specialist agents with narrow, focused prompts", "One consolidated HTML email built from 4 outputs",
         "Privacy: resumes are personal data, so don't log them to public places"],
        "Form (PDF + JD) → Extract text → Resume Analyst → Job Fit Analyst → Interview Questions → Learning Plan → Gmail",
        ["Google Gemini API key", "Gmail OAuth2"],
        ["Import it and connect the credentials.", "Open the form, upload your resume, and paste a real JD from LinkedIn or Naukri.",
         "Compare the fit score with your own judgement. Then tune the Job Fit prompt: add a scoring rubric (skills 40, experience 30, domain 20, extras 10)."],
        ["Try the same resume against 2 very different JDs. The scores should differ clearly."],
        [("Empty resume text", "Scanned or image PDFs have no text layer. Add OCR, or ask for a text-based PDF."),
         ("Scores are always about 75", "Add a rubric and examples of low and high scores to the prompt.")],
        ["Store results in Sheets to build a candidate pipeline.", "Loop over 20 resumes against one JD and rank them (see L20 sub-workflows)."])
    write(root, w, r)


# ---------- L19 error workflow ----------
def L19(root):
    w = WF("L19-global-error-handler", "L19 · Global error handler (alerts for every failing workflow)")
    w.note("## 🚨 L19 · Never fail silently\n1. Save this workflow.\n2. In **every other workflow**: ⋯ → Settings → *Error workflow* → pick **L19**.\n3. Any failed production run now sends a formatted alert **and** logs it to a sheet.\n\nTest: run *L04* with base = XYZ.", (-60, -400), 480, 260, 3)
    w.add("On Any Workflow Error", "errorTrigger", 1, {}, (0, 0))
    w.add("Shape Error", "code", 2, {"jsCode":
        "const e = $input.first().json;\n"
        "const ex = e.execution || {}; const wf = e.workflow || {};\n"
        "const msg = ex.error?.message || e.trigger?.error?.message || 'Unknown error';\n"
        "const node = ex.lastNodeExecuted || 'trigger';\n"
        "const hint = /401|403|credential|unauthori/i.test(msg) ? 'Check / reconnect the credential.'\n"
        "  : /429|rate|quota/i.test(msg) ? 'Rate limit — add Retry on Fail or slow the schedule.'\n"
        "  : /timeout|ETIMEDOUT|ECONNRESET/i.test(msg) ? 'Network/API timeout — enable retries.'\n"
        "  : 'Open the execution to debug.';\n"
        "return [{ json: { time: new Date().toISOString(), workflow: wf.name, workflow_id: wf.id, node, message: msg.slice(0, 500), hint, url: ex.url || '', mode: ex.mode || '' } }];"}, (220, 0))
    w.add("Email Alert", "gmail", 2.1, gmail_send(EMAIL, "=🚨 n8n failure: {{ $json.workflow }} → {{ $json.node }}",
        "=<p><b>Workflow:</b> {{ $json.workflow }}<br><b>Node:</b> {{ $json.node }}<br><b>Time:</b> {{ $json.time }}</p><pre>{{ $json.message }}</pre><p>💡 {{ $json.hint }}</p><p><a href=\"{{ $json.url }}\">Open execution</a></p>"), (440, -100), onError="continueRegularOutput")
    w.add("Log to Error Sheet", "googleSheets", 4.5, sheet_append("Errors"), (440, 100), onError="continueRegularOutput")
    w.chain("On Any Workflow Error", "Shape Error"); w.link("Shape Error", "Email Alert"); w.link("Shape Error", "Log to Error Sheet")
    r = readme("L19", "Global error handler", P, "Operations / reliability", "20 min",
        "Automation that fails silently is worse than none, because you think the reports are going out when they aren't. One error workflow can watch *all* your workflows, email you with a plain-English hint, and keep a log you can review every week.",
        ["**Error Trigger** and the *Error workflow* setting", "Error payload: `execution.error.message`, `lastNodeExecuted`, `execution.url`",
         "Pattern-matching errors into actionable hints", "Node-level *On Error: continue* so the alerting itself never crashes",
         "The full reliability toolkit: Retry on Fail · Continue on Error · Stop and Error · Error workflow"],
        "Error Trigger → Code (shape + hint) ─┬→ Gmail alert\n                                    └→ Sheets log",
        ["Gmail OAuth2", "Google Sheets OAuth2 (tab `Errors`: time, workflow, workflow_id, node, message, hint, url, mode)"],
        ["Add **Error Trigger** (this workflow never needs to be *active*).", "Add the Code node to shape the error and generate a hint.",
         "Add Gmail and Sheets in parallel, each with *On Error → Continue*.",
         "Open **every** other workflow → *Settings* → **Error workflow** → choose this one."],
        ["Activate **L04** with `base = XYZ` (or disconnect a credential) and let it run. The alert should arrive within seconds.",
         "Note: error workflows fire for **production** executions, not manual test runs."],
        [("No alert when testing manually", "That's expected. Only automatic (trigger or production) executions call the error workflow."),
         ("Alert loop", "Never set L19 as its own error workflow.")],
        ["Add Slack / Telegram alerts.", "Weekly summary: read the Errors sheet → group by workflow → email the top offenders."])
    write(root, w, r)


# ---------- L20 sub-workflows ----------
def L20(root):
    sub = WF("L20a-subworkflow-send-branded-email", "L20a · SUB — Send branded email (reusable)")
    sub.note("## ♻️ Sub-workflow (callee)\nInput: `to`, `title`, `body_html`, optional `cta_text` / `cta_url`.\nAny workflow can call this — change the branding **once**, every email updates.", (-60, -320), 460, 220, 6)
    sub.add("When Called by Another Workflow", "executeWorkflowTrigger", 1.1, {"workflowInputs": {"values": [
        {"name": "to"}, {"name": "title"}, {"name": "body_html"}, {"name": "cta_text"}, {"name": "cta_url"}]}}, (0, 0))
    sub.add("Wrap in Template", "code", 2, {"mode": "runOnceForEachItem", "jsCode":
        "const j = $json;\n"
        "const cta = j.cta_url ? `<p style=\"margin:24px 0\"><a href=\"${j.cta_url}\" style=\"background:#EA4B71;color:#fff;padding:10px 18px;border-radius:6px;text-decoration:none\">${j.cta_text || 'Open'}</a></p>` : '';\n"
        "const html = `<div style=\"font-family:Segoe UI,Arial;max-width:600px;margin:auto;border:1px solid #eee;border-radius:8px\">\n"
        "<div style=\"background:#1f2937;color:#fff;padding:16px 20px;font-size:18px\">${j.title}</div>\n"
        "<div style=\"padding:20px;color:#111\">${j.body_html}${cta}</div>\n"
        "<div style=\"padding:12px 20px;color:#888;font-size:12px;border-top:1px solid #eee\">Sent by n8n automation · reply to this email if something looks wrong</div></div>`;\n"
        "return { json: { ...j, html } };"}, (220, 0))
    sub.add("Send", "gmail", 2.1, gmail_send("={{ $json.to }}", "={{ $json.title }}", "={{ $json.html }}"), (440, 0))
    sub.add("Return Result", "set", 3.4, assign(sent=True, to="={{ $('Wrap in Template').item.json.to }}", message_id="={{ $json.id }}"), (660, 0))
    sub.chain("When Called by Another Workflow", "Wrap in Template", "Send", "Return Result")
    write(root, sub, "# L20a · Sub-workflow: send branded email\n\nThis is the **callee** used by [L20 · Sub-workflows](../L20-subworkflows-caller/README.md). Import it first, save it, then copy its workflow ID into the caller.\n\n[← Back to the learning path](../../README.md)")

    w = WF("L20-subworkflows-caller", "L20 · Sub-workflows — weekly birthday & anniversary wishes")
    w.note("## 🧱 L20 · Build once, reuse everywhere\nThis caller reads a team sheet, finds today's birthdays / work anniversaries and calls **L20a** once per person.\nSet the sub-workflow in *Call: Send Branded Email* (From list → L20a).", (-60, -360), 480, 240, 6)
    w.add("Every Day 9 AM", "scheduleTrigger", 1.2, {"rule": {"interval": [{"triggerAtHour": 9}]}}, (0, 0))
    w.add("Read Team Sheet", "googleSheets", 4.5, {"documentId": {"__rl": True, "mode": "url", "value": "PASTE_YOUR_GOOGLE_SHEET_URL"},
        "sheetName": {"__rl": True, "mode": "name", "value": "Team"}, "options": {}}, (220, 0))
    w.add("Who Celebrates Today?", "code", 2, {"jsCode":
        "// Sheet columns: name | email | birthday (YYYY-MM-DD) | joined (YYYY-MM-DD)\n"
        "const today = new Date(); const md = d => d && d.slice(5, 10);\n"
        "const tmd = today.toISOString().slice(5, 10);\n"
        "const out = [];\n"
        "for (const { json: p } of $input.all()) {\n"
        "  if (md(p.birthday) === tmd) out.push({ json: { to: p.email, title: `Happy birthday, ${p.name}! 🎂`, body_html: `<p>Wishing you a fantastic year ahead, ${p.name}. Cake is on the team today!</p>`, cta_text: '', cta_url: '' } });\n"
        "  if (md(p.joined) === tmd) { const yrs = today.getFullYear() - Number(p.joined.slice(0, 4));\n"
        "    if (yrs > 0) out.push({ json: { to: p.email, title: `Happy ${yrs}-year work anniversary, ${p.name}! 🎉`, body_html: `<p>Thank you for ${yrs} great year${yrs > 1 ? 's' : ''} with us.</p>`, cta_text: '', cta_url: '' } }); }\n"
        "}\n"
        "return out;"}, (440, 0))
    w.add("Call: Send Branded Email", "executeWorkflow", 1.2, {"workflowId": {"__rl": True, "mode": "id", "value": "REPLACE_WITH_L20a_WORKFLOW_ID"},
        "workflowInputs": {"mappingMode": "defineBelow", "value": {"to": "={{ $json.to }}", "title": "={{ $json.title }}", "body_html": "={{ $json.body_html }}", "cta_text": "={{ $json.cta_text }}", "cta_url": "={{ $json.cta_url }}"},
                           "matchingColumns": [], "schema": [{"id": k, "displayName": k, "type": "string", "required": False, "display": True, "canBeUsedToMatch": True, "defaultMatch": False, "removed": False} for k in ("to", "title", "body_html", "cta_text", "cta_url")]},
        "options": {}}, (660, 0))
    w.chain("Every Day 9 AM", "Read Team Sheet", "Who Celebrates Today?", "Call: Send Branded Email")
    r = readme("L20", "Sub-workflows: reusable building blocks", P, "HR / team culture", "30 min",
        "After 10 workflows you'll have copy-pasted the same email template 10 times. Sub-workflows are functions for n8n: build *Send branded email* once and call it from anywhere. The example use is automatic birthday and work-anniversary wishes, which every HR and team lead wants.",
        ["**Execute Workflow Trigger** with typed inputs (the callee)", "**Execute Workflow** node (the caller) with mapped inputs",
         "Returning data from a sub-workflow", "Code that returns 0..N items (no one celebrating today means nothing runs)", "Designing for reuse: small, single-purpose workflows"],
        "CALLER  Schedule → Sheets read → Code (filter today) → Execute Workflow(L20a)\nCALLEE  Execute Workflow Trigger → Code (template) → Gmail → Set (return)",
        ["Google Sheets OAuth2", "Gmail OAuth2"],
        ["Import **L20a** first and save it. Copy its ID from the URL (`/workflow/<ID>`).",
         "Create a sheet tab **Team** with `name, email, birthday, joined` (dates as YYYY-MM-DD). Put today's date in one row for testing.",
         "Import **L20**. In *Call: Send Branded Email*, select L20a *From list* (or paste the ID).",
         "Run it."],
        ["Look at the Execute Workflow output: it contains `sent: true` returned by the sub-workflow.",
         "Change the header colour in L20a and run again. Every caller gets the new look."],
        [("`Workflow does not exist`", "Wrong ID, or L20a wasn't saved."),
         ("The sub-workflow receives empty fields", "Input names must match exactly on both sides.")],
        ["Call L20a from L02, L08 and L19 to give every email the same branding.", "Make an L20b *Log to Sheet* sub-workflow for audit logs."])
    write(root, w, r)


# ---------- L21 uptime monitor ----------
def L21(root):
    w = WF("L21-website-uptime-monitor", "L21 · Website & API uptime monitor (state + alerts on change)")
    w.note("## 📡 L21 · Ops monitoring\nEvery 5 min: check each URL, measure status + response time.\nAlerts only when a site **changes** state (UP→DOWN, DOWN→UP) — state kept with `$getWorkflowStaticData`.\n⚠️ Static data persists only for **active** (production) runs.", (-60, -400), 500, 240, 3)
    w.add("Every 5 Minutes", "scheduleTrigger", 1.2, {"rule": {"interval": [{"field": "minutes", "minutesInterval": 5}]}}, (0, 0))
    w.add("Sites to Watch", "code", 2, {"jsCode":
        "return [\n  { url: 'https://n8n.io', name: 'n8n website' },\n  { url: 'https://api.github.com', name: 'GitHub API' },\n  { url: 'https://httpstat.us/503', name: 'Demo: always down' },\n].map(s => ({ json: { ...s, started: Date.now() } }));"}, (220, 0))
    w.add("Check Site", "httpRequest", 4.2, {"url": "={{ $json.url }}", "options": {"timeout": 10000, "redirect": {"redirect": {}},
        "response": {"response": {"fullResponse": True, "neverError": True}}}}, (440, 0), onError="continueRegularOutput")
    w.add("Compare with Last State", "code", 2, {"jsCode":
        "const state = $getWorkflowStaticData('global');\n"
        "state.sites = state.sites || {};\n"
        "const sites = $('Sites to Watch').all();\n"
        "return $input.all().map((r, i) => {\n"
        "  const site = sites[i].json;\n"
        "  const code = r.json.statusCode || 0;\n"
        "  const ms = Date.now() - site.started;\n"
        "  const up = code >= 200 && code < 400;\n"
        "  const prev = state.sites[site.url]?.up;\n"
        "  const changed = prev !== undefined && prev !== up;\n"
        "  const since = changed || prev === undefined ? new Date().toISOString() : state.sites[site.url].since;\n"
        "  state.sites[site.url] = { up, since };\n"
        "  return { json: { time: new Date().toISOString(), name: site.name, url: site.url, status: up ? 'UP' : 'DOWN', code, ms, changed, since, error: r.json.error?.message || '' } };\n"
        "});"}, (660, 0))
    w.add("Log Every Check", "googleSheets", 4.5, sheet_append("Uptime"), (880, -120), onError="continueRegularOutput")
    w.add("State Changed?", "filter", 2.2, {"conditions": conditions(cond("={{ $json.changed }}", "boolean", "true")), "options": {}}, (880, 80))
    w.add("Alert", "gmail", 2.1, gmail_send(EMAIL, "={{ $json.status === 'DOWN' ? '🔴' : '🟢' }} {{ $json.name }} is {{ $json.status }}",
        "=<p><b>{{ $json.name }}</b> ({{ $json.url }}) is now <b>{{ $json.status }}</b>.</p><p>HTTP {{ $json.code }} · {{ $json.ms }} ms · since {{ $json.since }}</p><p>{{ $json.error }}</p>"), (1100, 80))
    w.chain("Every 5 Minutes", "Sites to Watch", "Check Site", "Compare with Last State")
    w.link("Compare with Last State", "Log Every Check"); w.link("Compare with Last State", "State Changed?"); w.link("State Changed?", "Alert")
    r = readme("L21", "Website & API uptime monitor", P, "DevOps / IT", "30 min",
        "Paid uptime tools cost money, and simple ones spam you every 5 minutes while a site is down. This monitor checks your sites and APIs, logs response times, and alerts only when the state *changes*: once when a site goes down and once when it recovers.",
        ["HTTP Request with **Full Response + Never Error** (read status codes instead of crashing)",
         "**Workflow static data**: memory that survives between executions",
         "Alert on *change* instead of on *state*, which avoids alert fatigue", "Filter node", "Fan-out: log everything, alert on some"],
        "Schedule (5 min) → Code (site list) → HTTP (full response, never error) → Code (compare state)\n   ├→ Sheets log (every check)\n   └→ Filter changed → Gmail alert",
        ["Gmail OAuth2", "Google Sheets OAuth2 (tab `Uptime`: time, name, url, status, code, ms, changed, since, error)"],
        ["Edit the site list in *Sites to Watch*.",
         "HTTP Request: URL `{{ $json.url }}`, Options → *Response → Include full response* + *Never error*, timeout 10 s.",
         "Code: read and update `$getWorkflowStaticData('global')`.",
         "Filter `changed = true` → Gmail.", "**Activate** it (static data isn't saved in manual runs)."],
        ["The `httpstat.us/503` demo site should alert DOWN on the second automatic run.",
         "Replace it with `https://httpstat.us/200` and you should get an 🟢 recovery alert."],
        [("Alerts never fire", "Static data only persists in *active* executions. Manual runs start fresh every time."),
         ("Every site shows DOWN", "Check that *Never error* and *Full response* are both on, so `statusCode` exists.")],
        ["Add a slowness alert (ms > 3000 for 3 checks in a row).", "Weekly uptime % report from the Uptime sheet.", "Check SSL certificate expiry via an API."])
    write(root, w, r)


# ---------- L22 AI lead qualifier ----------
def L22(root):
    w = WF("L22-ai-lead-qualifier-router", "L22 · AI lead qualifier & router (Sales capstone)")
    w.note("## 🏁 L22 · Capstone: everything together\nForm → Gemini scores the lead (BANT) with **structured output** → **Switch** routes Hot / Warm / Cold → CRM sheet, instant sales alert, tailored reply.\nErrors → L19. Emails → could call L20a.", (-60, -440), 500, 240, 4)
    w.add("Enquiry Form", "formTrigger", 2.2, {"formTitle": "Talk to us", "formDescription": "Tell us what you want to automate.",
        "formFields": {"values": [form_field("Name", required=True), form_field("Work email", "email", True), form_field("Company", required=True),
            form_field("Team size", "dropdown", True, ["1-10", "11-50", "51-200", "200+"]), form_field("What do you want to automate?", "textarea", True),
            form_field("When do you want to start?", "dropdown", True, ["This month", "This quarter", "Just exploring"])]}, "options": {}}, (0, 0))
    w.lc("Qualify Lead", "chainLlm", 1.5, {"promptType": "define", "hasOutputParser": True,
        "text": "=Name: {{ $json.Name }}\nEmail: {{ $json['Work email'] }}\nCompany: {{ $json.Company }}\nTeam size: {{ $json['Team size'] }}\nTimeline: {{ $json['When do you want to start?'] }}\nNeed: {{ $json['What do you want to automate?'] }}",
        "messages": {"messageValues": [{"message": "You are a B2B sales development rep for an automation consultancy. Score the lead 0-100 using BANT (Budget signals, Authority, Need clarity, Timeline). Personal email domains (gmail, yahoo) lower authority. tier = hot (>=70), warm (40-69), cold (<40). Be strict and explain briefly."}]}}, (240, 0))
    w.gemini("Gemini", (180, 200), 0)
    w.lc("Lead Schema", "outputParserStructured", 1.2, {"jsonSchemaExample": json.dumps({"score": 78, "tier": "hot", "reason": "Clear need, 51-200 team, starting this month.",
        "use_case": "Invoice processing", "suggested_reply": "Hi Asha, thanks — invoice automation is a sweet spot for us..."}, indent=2)}, (340, 200))
    w.add("Build CRM Row", "set", 3.4, assign(time="={{ $now.toISO() }}", name="={{ $('Enquiry Form').item.json.Name }}",
        email="={{ $('Enquiry Form').item.json['Work email'] }}", company="={{ $('Enquiry Form').item.json.Company }}",
        score="={{ $json.output.score }}", tier="={{ $json.output.tier }}", reason="={{ $json.output.reason }}",
        use_case="={{ $json.output.use_case }}", reply="={{ $json.output.suggested_reply }}"), (480, 0))
    w.add("Save to CRM Sheet", "googleSheets", 4.5, sheet_append("Leads"), (700, 0))
    w.add("Route by Tier", "switch", 3.2, {"rules": {"values": [
        {"conditions": conditions(cond("={{ $('Build CRM Row').item.json.tier }}", "string", "equals", "hot")), "renameOutput": True, "outputKey": "Hot"},
        {"conditions": conditions(cond("={{ $('Build CRM Row').item.json.tier }}", "string", "equals", "warm")), "renameOutput": True, "outputKey": "Warm"}]},
        "options": {"fallbackOutput": "extra", "renameFallbackOutput": "Cold"}}, (920, 0))
    row = "$('Build CRM Row').item.json"
    w.add("🔥 Alert Sales Now", "gmail", 2.1, gmail_send(EMAIL, f"=🔥 HOT lead ({{{{ {row}.score }}}}): {{{{ {row}.company }}}}",
        f"=<p><b>{{{{ {row}.name }}}}</b> · {{{{ {row}.email }}}}</p><p>{{{{ {row}.reason }}}}</p><p>Call within 1 hour.</p>"), (1160, -200))
    w.add("Personal Reply (Hot/Warm)", "gmail", 2.1, gmail_send(f"={{{{ {row}.email }}}}", "=Re: automating {{ $('Build CRM Row').item.json.use_case }}",
        f"=<p>{{{{ {row}.reply }}}}</p><p>Pick a slot: https://cal.com/your-link</p>"), (1400, -100))
    w.add("Nurture Email (Cold)", "gmail", 2.1, gmail_send(f"={{{{ {row}.email }}}}", "=Thanks for reaching out, {{ $('Build CRM Row').item.json.name }}",
        "=<p>Thanks for your interest! Here are 3 free guides to get started with automation: https://github.com/YOUR_USER/n8n-knowledge</p>"), (1160, 160))
    w.chain("Enquiry Form", "Qualify Lead", "Build CRM Row", "Save to CRM Sheet", "Route by Tier")
    w.link("Route by Tier", "🔥 Alert Sales Now", 0); w.link("🔥 Alert Sales Now", "Personal Reply (Hot/Warm)")
    w.link("Route by Tier", "Personal Reply (Hot/Warm)", 1); w.link("Route by Tier", "Nurture Email (Cold)", 2)
    w.ai("Gemini", "Qualify Lead", "ai_languageModel"); w.ai("Lead Schema", "Qualify Lead", "ai_outputParser")
    r = readme("L22", "AI lead qualifier & router (capstone)", P, "Sales", "40 min",
        "Sales teams waste hours on tyre-kickers while hot leads go cold. This capstone scores every enquiry with AI (BANT), logs it to a CRM sheet, alerts sales straight away for hot leads, sends a personalised reply, and sends cold leads a nurture email.",
        ["Combines **everything**: form, structured AI output, Set, Sheets, Switch routing, multiple Gmail branches",
         "AI as a *decision-maker* with explicit, auditable reasons", "Temperature 0 for consistent scoring", "Designing the fallback path (cold leads still get a reply)"],
        "Form → LLM Chain ⇐ Gemini, ⇐ Schema → Set CRM row → Sheets → Switch\n   ├ Hot  → Alert sales → Personal reply\n   ├ Warm → Personal reply\n   └ Cold → Nurture email",
        ["Google Gemini API key", "Google Sheets OAuth2 (tab `Leads`: time, name, email, company, score, tier, reason, use_case, reply)", "Gmail OAuth2"],
        ["Build it yourself using L07 + L12 + L04 as references. That is the capstone test.",
         "If you get stuck, import `workflow.json` and compare node by node.",
         "Set the workflow's *Error workflow* to L19."],
        ["Submit the 3 sample leads in [docs/sample-data.md](../../docs/sample-data.md#sales-leads): one each should come out hot, warm and cold."],
        [("Every lead is 'warm'", "Make the rubric stricter and give examples in the system prompt."),
         ("A replied lead gets 2 emails", "Hot goes through alert → reply once. Check you didn't also wire Hot directly to *Personal Reply*.")],
        ["Replace the Sheet with HubSpot / Zoho CRM nodes.", "Add an approval step (L15) before the AI reply goes out.", "Enrich with company data via an API before scoring."])
    write(root, w, r)


ALL = [L11, L12, L13, L14, L15, L16, L17, L18, L19, L20, L21, L22]
