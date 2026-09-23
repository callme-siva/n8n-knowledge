# How to test n8n workflows

Testing happens at three levels. Beginners only need the first; contributors should use all three.

## Level 1: in the editor (everyone)
- **Run node by node.** Click ▶ on a single node to run the workflow up to that node. Check the OUTPUT panel before adding the next node.
- **Pin data.** In any node's output, click 📌 *Pin*. The next runs reuse that output and don't call the API or AI again, which saves quota and time. *Unpin before exporting* (CI rejects pinned data because it often contains real emails).
- **Mock a trigger.** For Gmail/Form/Webhook triggers, click *Fetch test event* / *Listen*, send one real event, then pin it.
- **Test the unhappy path.** Bad input, empty API result, expired credential. Every README has a *Test it* list that includes these.
- **Executions tab.** Every production run is logged there. Open a failed one and click *Debug in editor* to load its data into the canvas.

## Level 2: structural validation (contributors, no n8n needed)
```bash
python3 tools/validate.py
```
Checks every `workflow.json` for: valid JSON, unique node names, connections pointing to real nodes, no credentials, no pinned data, no personal emails, has a trigger, has a README. This runs automatically on every push and PR (`.github/workflows/validate.yml`).

## Level 3: check against real n8n
Installs a real n8n and checks every node **type**, **typeVersion**, **parameter** and **option** against n8n's own node definitions. This catches typos that the n8n UI would silently drop.
```bash
mkdir -p /tmp/n8n-check && cd /tmp/n8n-check && npm init -y && npm i n8n
```
```bash
cd /tmp/n8n-check && node /path/to/n8n-knowledge/tools/check-nodes.js /path/to/n8n-knowledge/workflows/*/workflow.json
```
Import test (proves n8n accepts every file):
```bash
mkdir -p /tmp/imp && for f in workflows/*/workflow.json; do cp "$f" "/tmp/imp/$(basename $(dirname $f)).json"; done
```
```bash
N8N_USER_FOLDER=/tmp/n8n-test npx n8n import:workflow --separate --input=/tmp/imp
```

**Last full run:** n8n 2.40.5 → 23/23 imported, 0 node/parameter issues.

## Level 4: end-to-end (optional)
Run each workflow once with real credentials and the inputs from [sample-data.md](sample-data.md). Record the result in your PR description.
