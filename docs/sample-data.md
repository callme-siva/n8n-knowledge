<div align="center">

# 🧾 Sample data for testing

**Made-up inputs for testing every AI lesson.**

</div>

---

All names and companies below are fictional.

## Meeting transcript
*(for L12)*
```
Weekly status: Payments Revamp, 12 Sept
Anita (PM): We're still targeting go-live on 15 October.
Ravi (Tech lead): The bank's sandbox API has been down twice this week. If they don't fix it by the 25th, integration testing slips.
Meera (QA): We're assuming the UAT environment will be ready by 1 October. Infra hasn't confirmed.
Anita: Also, the new refund screen crashes on Android 12. That's blocking the demo.
Ravi: We need the security team's pen-test sign-off before go-live; they're booked until the 3rd.
Anita: Ravi, please chase the bank today. Meera, confirm UAT with infra by Friday.
```
Expected: about 2 Risks, 1 Assumption, 1 Issue, 1 Dependency.

## HR policy
*(for L13; paste into a doc and export it as a PDF)*
```
ACME Leave & Remote Work Policy (2026)
1. Casual leave: 12 days per calendar year, max 3 consecutive days. Unused casual leave lapses on 31 Dec.
2. Earned leave: 18 days per year, carry forward up to 30 days.
3. Work from home: up to 2 days per week with manager approval. Broadband reimbursed up to $50/month with bill.
4. Travel: economy class for flights under 4 hours. Hotel limit $200/night in major cities.
5. Sick leave beyond 2 days requires a medical certificate.
```
Try asking: *How many casual leaves can I carry forward?* · *Is broadband reimbursed?* · *What's the hotel limit in Mumbai?* · *What is the CEO's salary?* (it should refuse)

## Retro feedback
*(for L15)*
- **Went well:** Shipped the search feature two days early. Pairing between frontend and backend worked great.
- **Didn't go well:** Three urgent requests from sales landed mid-sprint. Stand-ups ran 30+ minutes. The test environment was down on Wednesday.
- **Suggestions:** Protect the sprint scope; timebox stand-up to 15 min; set up an alert for the test environment.
- **Morale:** 3 - Neutral

## Customer complaints
*(for L17)*
1. **Angry, high value:** "I paid $899 for the laptop (order ORD-88213) and it arrived with a cracked screen. This is the second time. I want a replacement TODAY or I'm going to consumer court."
2. **Mild:** "Hi, my order ORD-10022 shows delivered but I can't find it. Could you check with the courier? Thanks."

## Sales leads
*(for L22)*
| Name | Email | Company | Size | Need | Timeline | Expected |
|---|---|---|---|---|---|---|
| Asha Rao | asha@finlytics.example.com | Finlytics | 51-200 | Automate invoice extraction from 2,000 PDFs a month into our ERP, and approvals in Slack | This month | 🔥 hot |
| Karan | karan@studio.example.com | Pixel Studio | 11-50 | Maybe automate some social media posting | This quarter | 🌤 warm |
| Test | test123@freemail.example.com | na | 1-10 | just looking | Just exploring | ❄️ cold |

## Expense API
*(for L09)*
```bash
curl -X POST http://localhost:5678/webhook-test/expense -H 'Content-Type: application/json' -d '{"amount":450,"category":"food","note":"team lunch"}'
```
```bash
curl -X POST http://localhost:5678/webhook-test/expense -H 'Content-Type: application/json' -d '{"amount":-5,"category":"pizza"}'
```

---

<p align="center"><a href="../README.md">← Back to the learning path</a> · <a href="architecture.md">🏗️ Architecture</a></p>
