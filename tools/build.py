"""Regenerate every workflow, canvas snapshot and README:  python3 tools/build.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import level1_2, level3_4

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for fn in level1_2.ALL + level3_4.ALL:
    fn(ROOT)
    print("built", fn.__name__)

# previous / next navigation (L20a is a helper, not a lesson)
dirs = sorted(d for d in os.listdir(os.path.join(ROOT, "workflows")) if not d.startswith("L20a"))
title = lambda d: json.load(open(os.path.join(ROOT, "workflows", d, "workflow.json")))["name"].split(" (")[0]
for i, d in enumerate(dirs):
    p = os.path.join(ROOT, "workflows", d, "README.md")
    prev = f'<a href="../{dirs[i-1]}/README.md">← {title(dirs[i-1])}</a>' if i else ""
    nxt = f'<a href="../{dirs[i+1]}/README.md">{title(dirs[i+1])} →</a>' if i + 1 < len(dirs) else "🏁 You finished the path!"
    nav = f'<p align="center">{prev} &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a> &nbsp;·&nbsp; {nxt}</p>'
    s = open(p).read().replace("{{NAV}}", nav)
    open(p, "w").write(s)

p = os.path.join(ROOT, "workflows", "L20a-subworkflow-send-branded-email", "README.md")
txt = open(p).read()
open(p, "w").write(txt.replace("{{NAV}}", '<p align="center"><a href="../L20-subworkflows-caller/README.md">← Used by L20 · Sub-workflows</a> &nbsp;·&nbsp; <a href="../../README.md#-the-learning-path">📚 All lessons</a></p>'))

# ---- main README: lesson tables + gallery
import re
from lib import REGISTRY, LEVELS
strip = lambda t: re.sub(r"\*\*|`|\*", "", t)
blocks = []
for key, head in [("🟢", "🟢 Level 1 · Basics"), ("🟡", "🟡 Level 2 · Integrations"), ("🟠", "🟠 Level 3 · AI"), ("🔴", "🔴 Level 4 · Multi-agent & production")]:
    rows = [r for r in REGISTRY if r["level"].startswith(key) and r["num"] != "L20a"]
    blocks += [f"### {head}", "", "| # | Lesson | Domain | Key concepts | Time |", "|:-:|---|---|---|:-:|"]
    for r in rows:
        concepts = " · ".join(strip(x).split(":")[0].split(" (")[0] for x in r["learn"][:2])
        extra = " <sub>+ [L20a](workflows/L20a-subworkflow-send-branded-email/README.md)</sub>" if r["num"] == "L20" else ""
        blocks.append(f"| **{r['num']}** | [{r['title']}](workflows/{r['slug']}/README.md){extra} | {r['domain']} | {concepts} | {r['time']} |")
    blocks.append("")
gal = ["<table>"]
rs = [r for r in REGISTRY if r["num"] != "L20a"]
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
