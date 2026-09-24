"""Debug challenges: each spec builds a deliberately broken workflow.json and a fixed solution.json.
The last node (✅ Check) inspects the data and throws a hint for every bug that is still there,
so learners get real feedback inside n8n. The harness verifies the broken copy fails and the solution passes."""
import json, os
from lib import *

X = "🐞 Debug challenge"


def _write_solution(root, w):
    with open(os.path.join(root, "workflows", w.slug, "solution.json"), "w") as fh:
        json.dump(w.to_json(), fh, indent=2, ensure_ascii=False)


# ---------- X01: expressions, case sensitivity, $json in all-items mode ----------
def _x01(fixed):
    w = WF("X01-debug-order-report", "X01 · Debug me: the paid-orders report")
    w.note("## 🐞 X01 · This workflow has 3 bugs\nIt should list the **3 paid orders**, each with 18% tax added and its own label.\n1. Click **Execute workflow**.\n2. Read the error from **✅ Check**: it names what's still wrong.\n3. Fix one bug, run again, repeat until it says *All fixed*.\nDon't edit ✅ Check or Orders.", (0, 0), 460, 250, 5)
    w.add("When clicking 'Execute workflow'", "manualTrigger", 1, {}, (0, 0))
    w.add("Orders", "code", 2, {"jsCode":
        "// Test data. Don't change this node.\n"
        "return [\n"
        "  { order_id: 101, customer: 'Asha', amount: 1000, status: 'Paid' },\n"
        "  { order_id: 102, customer: 'Ravi', amount: 250, status: 'Unpaid' },\n"
        "  { order_id: 103, customer: 'Meera', amount: 499.5, status: 'Paid' },\n"
        "  { order_id: 104, customer: 'Karan', amount: 80, status: 'Unpaid' },\n"
        "  { order_id: 105, customer: 'Priya', amount: 3200, status: 'Paid' },\n"
        "].map(o => ({ json: o }));"}, (220, 0))
    field = "amount" if fixed else "ammount"
    w.add("Add Tax", "set", 3.4, {"assignments": {"assignments": [{"id": "a0", "name": "total", "value": f"={{{{ Math.round($json.{field} * 118) / 100 }}}}", "type": "number"}]},
                                  "includeOtherFields": True, "include": "all",
                                  "options": {"ignoreConversionErrors": True}}, (440, 0))
    label = "i.json" if fixed else "$json"
    w.add("Add Label", "code", 2, {"jsCode":
        "// Runs ONCE for all items.\n"
        f"return $input.all().map(i => ({{ json: {{ ...i.json, label: `#${{{label}.order_id}} · ${{{label}.customer}}` }} }}));"}, (660, 0))
    w.add("Paid Only", "filter", 2.2, {"conditions": {**conditions(cond("={{ $json.status }}", "string", "equals", "paid")),
                                                      "options": {"caseSensitive": not fixed, "leftValue": "", "typeValidation": "loose", "version": 2}},
                                       "options": {}}, (880, 0), alwaysOutputData=True)
    w.add("✅ Check", "code", 2, {"jsCode":
        "// Don't edit this node: it tells you which bugs are left.\n"
        "const items = $input.all().map(i => i.json).filter(j => j.order_id);\n"
        "const bugs = [];\n"
        "if (items.length !== 3) bugs.push(`Paid Only let ${items.length} order(s) through, expected 3. Compare the status values in Orders with the filter value, letter by letter.`);\n"
        "const taxed = $('Add Tax').all().map(i => i.json);\n"
        "if (taxed.some(j => typeof j.total !== 'number' || Number.isNaN(j.total))) bugs.push('Add Tax: total is empty. Open the node and check the field name inside the expression (the INPUT panel shows the real names).');\n"
        "else if (taxed.some(j => j.total !== Math.round(j.amount * 118) / 100)) bugs.push('Add Tax: total is not amount + 18%.');\n"
        "const labels = $('Add Label').all().map(i => i.json.label);\n"
        "if (new Set(labels).size !== labels.length) bugs.push(`Add Label: every order got the label \"${labels[0]}\". In \"run once for all items\" mode, $json is only the FIRST item. Use the loop variable.`);\n"
        "if (bugs.length) throw new Error(`🐞 ${bugs.length} bug(s) left: ` + bugs.map((b, i) => `(${i + 1}) ${b}`).join('  '));\n"
        "return [{ json: { result: '🎉 All fixed! 3 paid orders, tax added, labels correct.', orders: items } }];"}, (1100, 0))
    w.chain("When clicking 'Execute workflow'", "Orders", "Add Tax", "Add Label", "Paid Only", "✅ Check")
    return w


def X01(root):
    w = _x01(False)
    write(root, w, readme("X01", "Debug me: the paid-orders report", X, "Any", "20 min",
        "Most of the time you spend in n8n isn't building, it's working out why a workflow ran \"successfully\" and still produced the wrong data. This workflow runs, but it's wrong in 3 ways, each of them a mistake people make every week. Find them using only the INPUT and OUTPUT panels.",
        ["Reading the **INPUT / OUTPUT** panels to find where data first goes wrong", "Expression typos that silently give `undefined`",
         "Case-sensitive comparisons in Filter / IF", "`$json` vs the loop variable in *Run once for all items* Code nodes"],
        "Manual → Orders (test data) → Add Tax (Set) → Add Label (Code) → Paid Only (Filter) → ✅ Check (throws until fixed)",
        [],
        ["Import `workflow.json` (not `solution.json`) and click **Execute workflow**.",
         "Open **✅ Check** and read the error. It lists every bug that's still there.",
         "Walk the nodes left to right. For each one, compare INPUT with OUTPUT and ask: is this what I expected?",
         "Fix one bug and run again. Repeat until ✅ Check says *All fixed*.",
         "Stuck? Each bug has a hint and a solution under **Practice** below. The fixed workflow is [`solution.json`](solution.json)."],
        ["✅ Check outputs `🎉 All fixed!` with 3 orders (101, 103, 105), totals 1180, 589.41 and 3776, and 3 different labels."],
        [("I fixed everything but it still fails", "Run the whole workflow again (not just one node), so ✅ Check sees fresh data from every node.")],
        ["Break it again in a new way and ask a friend to find it.", "Try X02 next."]))
    _write_solution(root, _x01(True))


# ---------- X02: merge keys, string vs number, node order ----------
def _x02(fixed):
    w = WF("X02-debug-top-leads", "X02 · Debug me: the top-2 leads list")
    w.note("## 🐞 X02 · This workflow has 3 bugs\nIt should join leads with company data and return the **2 leads from the biggest companies**, biggest first.\nRun it, read **✅ Check**, fix, repeat. Don't edit Leads, Companies or ✅ Check.", (0, 0), 460, 200, 5)
    w.add("When clicking 'Execute workflow'", "manualTrigger", 1, {}, (0, 0))
    w.add("Leads", "code", 2, {"jsCode":
        "// From your form. Don't change this node.\n"
        "return [\n"
        "  { name: 'Asha', company: 'Finlytics' },\n"
        "  { name: 'Ravi', company: 'Kiranmart' },\n"
        "  { name: 'Meera', company: 'Pixel Studio' },\n"
        "  { name: 'Karan', company: 'Zenlogix' },\n"
        "].map(j => ({ json: j }));"}, (220, -100))
    w.add("Companies", "code", 2, {"jsCode":
        "// From your CRM export. Don't change this node.\n"
        "return [\n"
        "  { Company: 'Finlytics', employees: 120 },\n"
        "  { Company: 'Kiranmart', employees: 1200 },\n"
        "  { Company: 'Pixel Studio', employees: 9 },\n"
        "  { Company: 'Zenlogix', employees: 450 },\n"
        "].map(j => ({ json: j }));"}, (220, 100))
    match = {"mode": "combine", "advanced": True, "mergeByFields": {"values": [{"field1": "company", "field2": "Company"}]}, "options": {}} if fixed \
        else {"mode": "combine", "fieldsToMatchString": "company", "options": {}}
    w.add("Join on Company", "merge", 3, match, (440, 0), alwaysOutputData=True)
    w.add("Size", "set", 3.4, {"assignments": {"assignments": [{"id": "a0", "name": "size", "value": "={{ $json.employees }}", "type": "number" if fixed else "string"}]},
                               "includeOtherFields": True, "include": "all", "options": {}}, (660, 0))
    w.add("Biggest First", "sort", 1, {"sortFieldsUi": {"sortField": [{"fieldName": "size", "order": "descending"}]}, "options": {}}, (880 if fixed else 1100, 0))
    w.add("Top 2", "limit", 1, {"maxItems": 2}, (1100 if fixed else 880, 0))
    w.add("✅ Check", "code", 2, {"jsCode":
        "// Don't edit this node: it tells you which bugs are left.\n"
        "const items = $input.all().map(i => i.json).filter(j => j.name);\n"
        "const bugs = [];\n"
        "if (!items.length) bugs.push('Join on Company matched nothing. Look at the field names in Leads and Companies: are they spelled the same, including capitals?');\n"
        "else {\n"
        "  if (items.some(j => typeof j.size !== 'number')) bugs.push('Size: size is text, so \"9\" sorts above \"1200\". Check the type of the field in the Set node.');\n"
        "  const names = items.map(j => j.name).join(', ');\n"
        "  if (names !== 'Ravi, Karan') bugs.push(`Got [${names}], expected [Ravi, Karan]. If the sorting is right, check the ORDER of the nodes: what does Top 2 receive?`);\n"
        "}\n"
        "if (bugs.length) throw new Error(`🐞 ${bugs.length} bug(s) left: ` + bugs.map((b, i) => `(${i + 1}) ${b}`).join('  '));\n"
        "return [{ json: { result: '🎉 All fixed! Top 2 leads: Ravi (1200), Karan (450).', leads: items } }];"}, (1320, 0))
    w.link("When clicking 'Execute workflow'", "Leads"); w.link("When clicking 'Execute workflow'", "Companies")
    w.link("Leads", "Join on Company", 0, 0); w.link("Companies", "Join on Company", 0, 1)
    w.chain("Join on Company", "Size", *(("Biggest First", "Top 2") if fixed else ("Top 2", "Biggest First")), "✅ Check")
    return w


def X02(root):
    w = _x02(False)
    write(root, w, readme("X02", "Debug me: the top-2 leads list", X, "Sales / any", "25 min",
        "Joining two lists, ranking them and keeping the top few is one of the most common workflow shapes (leads + CRM, orders + customers, tickets + SLAs). It's also where silent bugs hide: a join that matches nothing, numbers that sort as text, and nodes in the wrong order. This workflow has all three.",
        ["**Merge → Combine by matching fields**, and what happens when keys differ", "Why **types** matter: text sorts differently from numbers",
         "Node order: Limit before Sort is not the same as Sort before Limit", "Reading a Merge node's two INPUT panels"],
        "Manual → Leads + Companies → Merge (match on company) → Size (Set) → Top 2 (Limit) → Biggest First (Sort) → ✅ Check",
        [],
        ["Import `workflow.json` (not `solution.json`) and click **Execute workflow**.",
         "Open **✅ Check** and read the error. It changes as you fix bugs, because a later bug can hide behind an earlier one.",
         "Open **Join on Company** and look at both INPUT tabs side by side.",
         "Fix, re-run, repeat until ✅ Check says *All fixed*.",
         "Stuck? Hints and solutions are under **Practice**. The fixed workflow is [`solution.json`](solution.json)."],
        ["✅ Check outputs `🎉 All fixed!` with Ravi (Kiranmart, 1200) then Karan (Zenlogix, 450)."],
        [("To fix the node order I have to delete connections", "Drag from the output dot of one node to the input of another. To remove a connection, hover over it and click the 🗑 icon.")],
        ["Change it to top 3 per size band (hint: Switch + Limit per branch).", "Replace Companies with a Google Sheets read (L07)."]))
    _write_solution(root, _x02(True))


ALL = [X01, X02]
