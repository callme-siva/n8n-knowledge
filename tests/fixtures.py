"""Mock data for the end-to-end harness.

TRIGGERS[slug]      → list of sample event items emitted instead of the real trigger
FIXTURES[slug][node] → (mode, data) for a stubbed node:
    "all"  = emit this fixed list of items          "each" = emit this object once per input item
    "echo" = pass input through                       for a textClassifier: an int = which output to route to
Values are realistic so every downstream Code node, IF and expression is genuinely exercised.
"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

_today = datetime.now(ZoneInfo("Asia/Kolkata")).date()   # the harness runs n8n with GENERIC_TIMEZONE=Asia/Kolkata
TODAY = _today.isoformat()
D = lambda days: (_today + timedelta(days=days)).isoformat()
MD = _today.strftime("%m-%d")

TRIGGERS = {
    "L06-gmail-pdf-to-drive": [{"id": "m1", "date": "2026-09-20T10:00:00Z", "from": {"text": "billing@airtel.example.com"}, "subject": "Your bill",
        "_binary": {"attachment_0": {"fileName": "bill.pdf", "mimeType": "application/pdf", "file": "invoice-valid.pdf"}, "attachment_1": {"fileName": "logo.png", "mimeType": "image/png"}}}],
    "L07-lead-capture-sheets": [{"Name": "  Asha Rao ", "Email": "Asha@Finlytics.example.com", "Company": "Finlytics", "Interested in": "AI agents", "Monthly budget (INR)": "25k – 1L"}],
    "L09-webhook-expense-api": [{"body": {"amount": 450, "category": "Food", "note": "team lunch", "user": "asha"}}],
    "L10-form-bug-report-jira": [{"Your email": "tester@example.com", "What is broken?": "Login button does nothing", "Steps to reproduce": "1. Open app 2. Click Login", "Severity": "Blocker — cannot work", "Page / module": "Auth"}],
    "L12-meeting-transcript-raid-log": [{"Meeting Title": "Payments Revamp weekly", "Meeting Date": "2026-09-12", "Meeting Type": "Project Status Meeting", "Transcript": "Anita: go-live 15 Oct. Ravi: bank sandbox down twice…"}],
    "L13-rag-policy-chatbot": [{"chatInput": "How many casual leaves can I carry forward?", "sessionId": "s1"}],
    "L14-ai-agent-with-tools": [{"chatInput": "What's 18% GST on 12499?", "sessionId": "s1"}],
    "L15-retro-ai-approval-jira": [{"Sprint": "Sprint 24", "What went well?": "Shipped search early", "What didn't go well?": "Mid-sprint requests", "Suggestions": "Protect scope", "Team morale": "3 - Neutral"}],
    "L17-complaint-handler-multi-agent": [{"customer_email": "rahul@example.com", "order_id": "ORD-88213", "complaint": "Laptop arrived with a cracked screen. Second time!"}],
    "L18-resume-job-fit-multi-agent": [{"Candidate Name": "Test Candidate", "Email": "cand@example.com", "Job Descriptions": "Scrum Master, 5+ years, Jira, SAFe",
        "_binary": {"Resume": {"fileName": "resume.pdf", "mimeType": "application/pdf", "file": "resume-sample.pdf"}}}],
    "L19-global-error-handler": [{"execution": {"id": "231", "url": "https://n8n.example.com/execution/231", "error": {"message": "429 Too Many Requests"}, "lastNodeExecuted": "Get Exchange Rate", "mode": "trigger"}, "workflow": {"id": "7", "name": "L04 · Currency rate alert"}}],
    "L20a-subworkflow-send-branded-email": [{"to": "a@example.com", "title": "Happy birthday!", "body_html": "<p>Cake time</p>", "cta_text": "", "cta_url": ""}],
    "L22-ai-lead-qualifier-router": [{"Name": "Asha Rao", "Work email": "asha@finlytics.example.com", "Company": "Finlytics", "Team size": "51-200", "What do you want to automate?": "Invoice extraction", "When do you want to start?": "This month"}],
    "P01-invoice-processing-pipeline": [{"id": "inv-mail-1", "from": {"text": "ap@vendor.example.com"}, "_binary": {
        "attachment_0": {"fileName": "INV-4411.pdf", "mimeType": "application/pdf", "file": "invoice-valid.pdf"},
        "attachment_1": {"fileName": "INV-9001.pdf", "mimeType": "application/pdf", "file": "invoice-large.pdf"},
        "attachment_2": {"fileName": "INV-4412.pdf", "mimeType": "application/pdf", "file": "invoice-wrong-total.pdf"},
        "attachment_3": {"fileName": "logo.png", "mimeType": "image/png"}}}],
    "P02-support-inbox-copilot": [{"id": "sm1", "threadId": "th1", "From": "priya@example.com", "Subject": "How do I change my plan?", "snippet": "Hi, how can I upgrade my plan to annual?"}],
    "P03-incident-response-orchestrator": [{"body": {"alerts": [
        {"status": "firing", "fingerprint": "fp-pay-1", "labels": {"alertname": "HighErrorRate", "severity": "critical", "service": "payments"}, "annotations": {"summary": "5xx > 5% for 5m"}, "startsAt": "2026-09-24T10:00:00Z"},
        {"status": "firing", "fingerprint": "fp-disk-1", "labels": {"alertname": "DiskFilling", "severity": "warning", "service": "db"}, "annotations": {"summary": "Disk 85%"}, "startsAt": "2026-09-24T10:01:00Z"},
        {"status": "resolved", "fingerprint": "fp-unknown", "labels": {"alertname": "Old", "severity": "warning", "service": "x"}, "annotations": {}, "endsAt": "2026-09-24T10:05:00Z"}]}}],
    "P04-sales-followup-sequence": [{"Name": "Karan", "Email": "Karan@Studio.example.com", "Company": "Pixel Studio", "What do you need?": "Automate social posting"}],
    "P06-purchase-approval-multilevel": [{"Your email": "req@example.com", "Manager email": "mgr@example.com", "Item / service": "MacBook Pro", "Amount (INR)": "215000", "Cost centre": "Engineering", "Justification": "Laptop replacement"}],
    "P07-employee-onboarding-orchestrator": [{"Full name": "Meera Iyer", "Personal email": "meera@example.com", "Role": "Engineer", "Start date": "2026-10-01", "Manager email": "mgr@example.com", "Team Slack channel": "#team-payments"}],
    "P09-deep-research-agent": [{"Question": "Top open-source Zapier alternatives?", "Audience": "Executive (1 page)", "Send report to": "you@example.com"}],
    "P10a-tool-lookup-customer": [{"email": "Asha@Finlytics.example.com"}],
    "P11-pii-safe-ai-gateway": [{"body": {"user": "asha", "text": "Reply to Rahul (rahul@example.com, 9876543210) about refund to card 4111 1111 1111 1111, PAN ABCDE1234F"}}],
    "Q03-telegram-capture-bot": [{"message": {"text": "/exp 120 travel auto to office", "chat": {"id": 42}, "from": {"first_name": "Asha"}}}],
    "Q07-gmail-ai-auto-labeler": [{"id": "g1", "From": "billing@vendor.example.com", "Subject": "Invoice #4411", "snippet": "Please find attached"}],
}

AI = lambda **kw: ("each", kw)

FIXTURES = {
    "L03-job-search-api": {"Search Google Jobs": ("all", [{"jobs_results": [
        {"title": "Agile Coach", "company_name": "Acme", "location": "Bengaluru", "apply_options": [{"link": "https://example.com/1"}], "detected_extensions": {"posted_at": "3 hours ago"}},
        {"title": "Scrum Master <Senior>", "company_name": "Beta & Co", "location": "Remote", "share_link": "https://example.com/2"}]}])},
    "L08-jira-stale-stories": {"Search Stale Stories": ("all", [
        {"key": "SCRUM-12", "fields": {"summary": "Checkout API", "assignee": {"displayName": "Ravi"}, "status": {"name": "In Progress"}, "updated": "2026-09-10T10:00:00Z"}},
        {"key": "SCRUM-15", "fields": {"summary": "Refund flow", "assignee": None, "status": {"name": "In Review"}, "updated": "2026-09-19T10:00:00Z"}}])},
    "L10-form-bug-report-jira": {},
    "L11-ai-news-digest-llm-chain": {"Write Briefing": AI(text="<h3>Top 5</h3><ul><li>Story</li></ul>")},
    "L12-meeting-transcript-raid-log": {"Extract RAID": AI(output={"items": [
        {"category": "Risk", "description": "Bank sandbox unstable", "owner": "Ravi", "impact": "Testing slips", "mitigation": "Chase bank"},
        {"category": "Dependency", "description": "Pen-test sign-off", "owner": "Security", "impact": "Blocks go-live", "mitigation": "Book slot"}]})},
    "L13-rag-policy-chatbot": {"Policy Assistant": AI(output="You can carry forward up to 30 earned leave days (ACME Leave Policy §2).")},
    "L14-ai-agent-with-tools": {"Assistant Agent": AI(output="18% GST on ₹12,499 is ₹2,249.82.")},
    "L15-retro-ai-approval-jira": {"Analyze Retro": AI(output={"sentiment": "mixed", "summary": "Good delivery, too many interruptions.", "action_items": [
        {"title": "Protect sprint scope", "description": "Route new requests to backlog", "priority": "High", "owner_role": "Product Owner"},
        {"title": "Timebox stand-up", "description": "15 minutes max", "priority": "Medium", "owner_role": "Scrum Master"}]})},
    "L16-sprint-report-multi-agent": {
        "Fetch GitHub Project": ("all", [{"data": {"repositoryOwner": {"projectV2": {"title": "Sprint board", "items": {"nodes": [
            {"content": {"title": "Login", "assignees": {"nodes": [{"login": "ravi"}]}}, "fieldValues": {"nodes": [{"name": "Done", "field": {"name": "Status"}}, {"number": 5, "field": {"name": "Story Points"}}, {"title": "Sprint 24", "startDate": "2026-09-15", "duration": 14, "field": {"name": "Iteration"}}]}},
            {"content": {"title": "Checkout", "assignees": {"nodes": [{"login": "meera"}]}}, "fieldValues": {"nodes": [{"name": "In Progress", "field": {"name": "Status"}}, {"number": 8, "field": {"name": "Story Points"}}]}},
            {"content": {"title": "Refunds", "assignees": {"nodes": []}}, "fieldValues": {"nodes": [{"name": "Todo", "field": {"name": "Status"}}, {"number": 3, "field": {"name": "Story Points"}}]}}]}}}}}]),
        **{n: AI(output=f"{n}: analysis text") for n in ("Capacity Planning Agent", "Backlog Health Agent", "Burndown Tracking Agent", "Coordinator Agent")}},
    "L17-complaint-handler-multi-agent": {
        "Understand Complaint": AI(output={"category": "damaged", "urgency": "high", "sentiment": "negative", "product": "Laptop", "order_id": "ORD-88213", "customer_email": "rahul@example.com", "summary": "Cracked screen, repeat issue"}),
        "Investigate Customer/Order": AI(output={"known_facts": "Repeat damage", "missing_info": "Photos", "recommended_lookups": "Courier logs", "confidence": "medium"}),
        "Determine Resolution": AI(output={"resolution_workflow": "replacement", "steps": "Ship replacement", "policy_notes": "Within 7 days"}),
        "Check Escalation": AI(output={"escalate": True, "priority": "high", "reason": "Repeat, high value", "route_to": "senior-support"}),
        "Draft Response": AI(output="Dear Rahul, we're sorry… a replacement is on its way.")},
    "L18-resume-job-fit-multi-agent": {
        **{n: AI(output=f"{n} output") for n in ("Resume Analyst", "Job Fit Analyst", "Interview Question Generator", "Learning Plan Builder")}},
    "L20-subworkflows-caller": {"Read Team Sheet": ("all", [
        {"name": "Asha", "email": "asha@example.com", "birthday": f"1990-{MD}", "joined": f"2022-{MD}"},
        {"name": "Ravi", "email": "ravi@example.com", "birthday": "1991-01-02", "joined": "2024-03-01"}])},
    "L22-ai-lead-qualifier-router": {"Qualify Lead": AI(output={"score": 82, "tier": "hot", "reason": "Clear need, right size, this month", "use_case": "Invoice extraction", "suggested_reply": "Hi Asha, …"})},
    "P01-invoice-processing-pipeline": {
        # Stand-in for the AI extractor: deterministic regex over the REAL text pdf.js extracted from the sample PDFs
        "Extract Invoice Fields": ("code", r"""const t = $json.text || '';
const num = re => { const m = t.match(re); return m ? Number(m[1].replace(/,/g, '')) : undefined; };
const str = re => { const m = t.match(re); return m ? m[1].trim() : undefined; };
return { json: { output: { vendor_name: str(/TAX INVOICE\s+(.+?)\s+\d+ MG Road/), vendor_gstin: str(/GSTIN:\s*(\S+)/), invoice_number: str(/Invoice No:\s*(\S+)/),
  invoice_date: '2026-09-01', due_date: '2026-10-01', subtotal: num(/Subtotal: INR ([\d,\.]+)/), tax_total: num(/IGST 18%: INR ([\d,\.]+)/), grand_total: num(/Grand Total: INR ([\d,\.]+)/), currency: 'INR' } } };""")},
    "P02-support-inbox-copilot": {
        "Triage": 0,
        "Load FAQ": ("all", [{"question": "How do I change my plan?", "answer": "Settings → Billing → Change plan."}, {"question": "Refund policy?", "answer": "Full refund within 14 days."}]),
        "Draft Answer": AI(output={"reply": "Hi Priya, go to Settings → Billing → Change plan.", "confidence": 0.9, "needs_human": False, "faq_used": "How do I change my plan?"})},
    "P03-incident-response-orchestrator": {"Draft Postmortem": AI(text="## Summary\n…")},
    "P05-bulk-ai-enrichment-checkpointed": {
        "Pending Rows Only": ("all", [{"row_id": str(i), "company": f"Co {i}", "website": f"https://co{i}.example.com", "description": "B2B SaaS for invoices", "status": "pending"} for i in range(1, 24)]),
        "Classify Company": AI(output={"industry": "SaaS", "b2b": True, "icp_score": 78, "reason": "Digital, process-heavy"})},
    "P08-sheets-jira-sync-hashing": {"Read Backlog Sheet": ("all", [
        {"row_id": "1", "summary": "New story", "description": "d1", "priority": "High", "jira_key": "", "sync_hash": ""},
        {"row_id": "2", "summary": "Changed story", "description": "edited", "priority": "Low", "jira_key": "SCRUM-7", "sync_hash": "stale"},
        {"row_id": "3", "summary": "", "description": "", "priority": "", "jira_key": "", "sync_hash": ""}])},
    "P09-deep-research-agent": {"Research Agent": AI(output="<h2>Answer in brief</h2><ul><li>n8n</li></ul>")},
    "P10a-tool-lookup-customer": {"Find Customer": ("all", [{"email": "asha@finlytics.example.com", "plan": "Pro", "mrr": 12000, "status": "active"}])},
    "P11-pii-safe-ai-gateway": {"Answer": AI(text="Dear [EMAIL_1], we'll refund to card [CARD_3] shortly. Call us back at [PHONE_2].")},
    "P12-weekly-exec-kpi-report": {
        "Jira: Done Last 7d": ("all", [{"key": "S-1", "fields": {"issuetype": {"name": "Story"}}}, {"key": "S-2", "fields": {"issuetype": {"name": "Bug"}}}]),
        "GitHub: Merged PRs 7d": ("all", [{"total_count": 31, "items": []}]),
        "Sheets: Revenue": ("all", [{"date": "2026-09-22", "revenue": "45000", "orders": "12"}, {"date": "2026-09-15", "revenue": "40000", "orders": "10"}]),
        "Write Narrative": AI(text="<li>Win: 31 PRs merged</li>")},
    "Q01-daily-agenda-calendar": {"Today's Events": ("all", [
        {"summary": "Stand-up", "status": "confirmed", "start": {"dateTime": f"{TODAY}T09:30:00+05:30"}, "end": {"dateTime": f"{TODAY}T09:45:00+05:30"}, "attendees": [{}, {}]},
        {"summary": "Client call", "status": "confirmed", "start": {"dateTime": f"{TODAY}T14:00:00+05:30"}, "end": {"dateTime": f"{TODAY}T15:00:00+05:30"}}])},
    "Q04-github-stale-pr-reminder": {"Open PRs": ("all", [
        {"number": 101, "title": "Fix login", "draft": False, "updated_at": "2026-09-18T00:00:00Z", "html_url": "https://github.com/x/y/pull/101", "user": {"login": "ravi"}, "requested_reviewers": [{"login": "meera"}]},
        {"number": 102, "title": "WIP", "draft": True, "updated_at": "2026-09-01T00:00:00Z", "html_url": "https://github.com/x/y/pull/102", "user": {"login": "asha"}, "requested_reviewers": []}])},
    "Q05-weekly-kpi-chart-email": {"Read Daily Sales": ("all", [{"date": f"2026-{m:02d}-{d:02d}", "revenue": str(20000 + d * 900), "orders": str(d)} for m in (8, 9) for d in range(1, 29, 2)])},
    "Q06-invoice-due-reminders": {"Read Invoices": ("all", [
        {"invoice_no": "INV-1", "client": "Acme", "email": "a@example.com", "amount": "11800", "due_date": D(3), "status": "unpaid", "last_reminded": ""},
        {"invoice_no": "INV-2", "client": "Beta", "email": "b@example.com", "amount": "5000", "due_date": D(-1), "status": "unpaid", "last_reminded": ""},
        {"invoice_no": "INV-3", "client": "Gamma", "email": "c@example.com", "amount": "900", "due_date": D(3), "status": "paid", "last_reminded": ""}])},
    "Q07-gmail-ai-auto-labeler": {"Classify": 0},
}


# ---------------------------------------------------------------- behaviour checks
# Each check: ("count", node, output_index, expected_items)  or  ("contains", node, text)  or  ("absent", node, text)
# count = total items that node emitted on that output (summed over loop iterations).
EXPECT = {
    "L04-currency-alert-switch": [("count", "API OK?", 0, 1)],
    "L05-rss-news-code-node": [("count", "Filter · Dedupe · Sort", 0, 1)],
    "L06-gmail-pdf-to-drive": [("count", "Split PDF Attachments", 0, 1), ("contains", "Split PDF Attachments", "_bill.pdf")],
    "L07-lead-capture-sheets": [("contains", "Clean Lead", "asha@finlytics.example.com"), ("contains", "Clean Lead", "\"Asha Rao\"")],
    "L08-jira-stale-stories": [("contains", "Build Report", "2 stale stories"), ("contains", "Build Report", "Unassigned: 1")],
    "L09-webhook-expense-api": [("count", "Valid?", 0, 1), ("contains", "201 Created", "\"category\":\"food\"")],
    "L10-form-bug-report-jira": [("contains", "Map Severity → Priority", "\"priority\":\"Highest\"")],
    "L12-meeting-transcript-raid-log": [("count", "Split RAID Items", 0, 2)],
    "L15-retro-ai-approval-jira": [("count", "Approved?", 0, 1), ("count", "Create Jira Task", 0, 2)],
    "L19-global-error-handler": [("contains", "Shape Error", "Rate limit")],
    "L20-subworkflows-caller": [("count", "Who Celebrates Today?", 0, 2)],
    "L18-resume-job-fit-multi-agent": [("contains", "Extract Resume Text", "Certified Scrum Master")],
    "L22-ai-lead-qualifier-router": [("count", "Route by Tier", 0, 1)],
    "P01-invoice-processing-pipeline": [("count", "Valid?", 0, 2), ("count", "Valid?", 1, 1), ("count", "Needs Approval?", 0, 1),
                                        ("count", "Append to Ledger", 0, 2), ("contains", "Log Exception", "≠ total"), ("contains", "Validate", "\"invoice_number\":\"INV-9001\""),
                                        ("contains", "PDF → Text", "Grand Total: INR 11,800.00")],
    "P02-support-inbox-copilot": [("count", "Confident?", 0, 1), ("count", "Create Gmail Draft", 0, 1)],
    "P03-incident-response-orchestrator": [("count", "Route", 0, 1), ("count", "Route", 1, 1), ("count", "Route", 3, 1), ("count", "Open Jira Incident", 0, 1)],
    "P04-sales-followup-sequence": [("count", "Replied? #1", 1, 1), ("count", "Replied? #2", 1, 1), ("contains", "CRM: Closed, No Reply", "no_reply_closed")],
    "P05-bulk-ai-enrichment-checkpointed": [("count", "Checkpoint to Sheet", 0, 23), ("contains", "Summary", "\"processed\":23"), ("contains", "Summary", "\"errors\":0")],
    "P06-purchase-approval-multilevel": [("count", "Needs Finance?", 0, 1), ("contains", "Final: Approved", "\"status\":\"approved\"")],
    "P07-employee-onboarding-orchestrator": [("count", "Create Jira Task", 0, 7), ("count", "Book Calendar Event", 0, 4), ("count", "Wait for Both", 0, 1)],
    "P08-sheets-jira-sync-hashing": [("count", "Operation", 0, 1), ("count", "Operation", 1, 1), ("count", "Operation", 2, 1)],
    "P10a-tool-lookup-customer": [("contains", "Shape Answer", "\"found\":true")],
    "P11-pii-safe-ai-gateway": [("contains", "Redact PII", "[EMAIL_1]"), ("contains", "Redact PII", "[CARD_"), ("contains", "Redact PII", "[PAN_"),
                                ("absent", "Audit Row", "rahul@example.com"), ("absent", "Audit Row", "4111"), ("contains", "Restore Tokens for Caller", "rahul@example.com")],
    "P12-weekly-exec-kpi-report": [("contains", "Compute KPIs", "\"prs_merged\":31"), ("contains", "Compute KPIs", "\"bugs_fixed\":1")],
    "Q01-daily-agenda-calendar": [("contains", "Build Agenda", "2 meetings"), ("contains", "Build Agenda", "Focus slots")],
    "Q03-telegram-capture-bot": [("count", "Valid Command?", 0, 1), ("contains", "Parse Command", "\"amount\":120")],
    "Q04-github-stale-pr-reminder": [("contains", "Find Stale", "\"count\":1")],
    "Q05-weekly-kpi-chart-email": [("contains", "Group by Week", "\"labels\"")],
    "Q06-invoice-due-reminders": [("count", "Stage", 0, 1), ("count", "Stage", 1, 1), ("count", "Write Back", 0, 2)],
}
