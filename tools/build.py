"""Regenerate every workflow, canvas snapshot and README:  python3 tools/build.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import level1_2, level3_4, quickwins, projects

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for fn in level1_2.ALL + level3_4.ALL + quickwins.ALL + projects.ALL:
    fn(ROOT)
    print("built", fn.__name__)

# previous / next navigation (L20a is a helper, not a lesson)
HELPERS = ("L20a", "P10a")
all_dirs = sorted(d for d in os.listdir(os.path.join(ROOT, "workflows")) if not d.startswith(HELPERS))
title = lambda d: json.load(open(os.path.join(ROOT, "workflows", d, "workflow.json")))["name"].split(" (")[0]
TRACK = {"L": "the core path", "Q": "Quick wins", "P": "Real-world projects"}
for d in all_dirs:
    dirs = [x for x in all_dirs if x[0] == d[0]]
    i = dirs.index(d)
    p = os.path.join(ROOT, "workflows", d, "README.md")
    prev = f'<a href="../{dirs[i-1]}/README.md">← {title(dirs[i-1])}</a>' if i else ""
    nxt = f'<a href="../{dirs[i+1]}/README.md">{title(dirs[i+1])} →</a>' if i + 1 < len(dirs) else f"🏁 End of {TRACK[d[0]]}"
    nav = f'<p align="center">{prev} &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; {nxt}</p>'
    s = open(p).read().replace("{{NAV}}", nav)
    open(p, "w").write(s)

for helper, parent, label in [("L20a-subworkflow-send-branded-email", "L20-subworkflows-caller", "L20 · Sub-workflows"), ("P10a-tool-lookup-customer", "P10-mcp-server-business-tools", "P10 · MCP server")]:
    p = os.path.join(ROOT, "workflows", helper, "README.md")
    txt = open(p).read()
    open(p, "w").write(txt.replace("{{NAV}}", f'<p align="center"><a href="../{parent}/README.md">← Used by {label}</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a></p>'))

# ---- main README: lesson tables + gallery
import re
from lib import REGISTRY, LEVELS
strip = lambda t: re.sub(r"\*\*|`|\*", "", t)
blocks = []
for key, head in [("🟢", "🟢 Level 1 · Basics"), ("🟡", "🟡 Level 2 · Integrations"), ("🟠", "🟠 Level 3 · AI"), ("🔴", "🔴 Level 4 · Multi-agent & production"),
                  ("⚡", "⚡ Quick wins: useful in 15 minutes"), ("🏭", "🏭 Real-world projects: production-grade systems")]:
    rows = [r for r in REGISTRY if r["level"].startswith(key) and not r["num"].endswith("a")]
    blocks += [f"### {head}", "", "| # | Lesson | Domain | Key concepts | Time |", "|:-:|---|---|---|:-:|"]
    for r in rows:
        concepts = " · ".join(strip(x).split(":")[0].split(" (")[0] for x in r["learn"][:2])
        extra = {"L20": " <sub>+ [L20a](workflows/L20a-subworkflow-send-branded-email/README.md)</sub>", "P10": " <sub>+ [P10a](workflows/P10a-tool-lookup-customer/README.md)</sub>"}.get(r["num"], "")
        blocks.append(f"| **{r['num']}** | [{r['title']}](workflows/{r['slug']}/README.md){extra} | {r['domain']} | {concepts} | {r['time']} |")
    blocks.append("")
gal = ["<table>"]
rs = [r for r in REGISTRY if not r["num"].endswith("a")]
for i in range(0, len(rs), 2):
    gal.append("<tr>")
    for r in rs[i:i + 2]:
        gal.append(f'<td width="50%" align="center" valign="top"><a href="workflows/{r["slug"]}/README.md"><img src="workflows/{r["slug"]}/canvas.svg" alt="{r["num"]} canvas"></a><br/><b>{r["num"]}</b> · {r["title"]}</td>')
    gal.append("</tr>")
gal.append("</table>")
p = os.path.join(ROOT, "README.md"); s = open(p).read()
s = re.sub(r"<!-- LESSONS:START -->.*<!-- LESSONS:END -->", lambda m: "<!-- LESSONS:START -->\n" + "\n".join(blocks) + "\n<!-- LESSONS:END -->", s, flags=re.S)
s = re.sub(r"<!-- GALLERY:START -->.*<!-- GALLERY:END -->", lambda m: "<!-- GALLERY:START -->\n" + "\n".join(gal) + "\n<!-- GALLERY:END -->", s, flags=re.S)
open(p, "w").write(s)
print("README tables + gallery updated")

import roadmap
roadmap.build(os.path.join(ROOT, "assets", "learning-path.svg"))
print("roadmap drawn")
