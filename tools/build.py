"""Regenerate every workflow, canvas snapshot and README:  python3 tools/build.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(__file__))
import level1_2, level3_4, quickwins, projects, debug

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

import lib, templates
lib.SHEET_TEMPLATES = templates.sheet_templates(ROOT)   # columns come from the last e2e run (tests/results.json)
templates.sample_files(ROOT)
for fn in level1_2.ALL + level3_4.ALL + quickwins.ALL + projects.ALL + debug.ALL:
    fn(ROOT)
    print("built", fn.__name__)

# previous / next navigation (L20a is a helper, not a lesson)
HELPERS = ("L20a", "P10a")
all_dirs = sorted(d for d in os.listdir(os.path.join(ROOT, "workflows")) if not d.startswith(HELPERS))
title = lambda d: json.load(open(os.path.join(ROOT, "workflows", d, "workflow.json")))["name"].split(" (")[0]
TRACK = {"L": "the core path", "Q": "Quick wins", "P": "Real-world projects", "X": "the debug challenges"}
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
                  ("⚡", "⚡ Quick wins: useful in 15 minutes"), ("🏭", "🏭 Projects: real business processes"), ("🐞", "🐞 Debug challenges: fix a broken workflow")]:
    rows = [r for r in REGISTRY if r["level"].startswith(key) and not r["num"].endswith("a")]
    blocks += [f"### {head}", "", "| # | Lesson | Domain | Key concepts | Time |", "|:-:|---|---|---|:-:|"]
    for r in rows:
        concepts = " · ".join(strip(x).split(":")[0].split(" (")[0] for x in r["learn"][:2])
        extra = {"L20": " <sub>+ [L20a](workflows/L20a-subworkflow-send-branded-email/README.md)</sub>", "P10": " <sub>+ [P10a](workflows/P10a-tool-lookup-customer/README.md)</sub>"}.get(r["num"], "")
        blocks.append(f"| **{r['num']}** | [{r['title']}](workflows/{r['slug']}/README.md){extra} | {r['domain']} | {concepts} | {r['time']} |")
    blocks.append("")
def gallery(rows, prefix=""):
    g = ["<table>"]
    for i in range(0, len(rows), 2):
        g.append("<tr>")
        for r in rows[i:i + 2]:
            g.append(f'<td width="50%" align="center" valign="top"><a href="{prefix}workflows/{r["slug"]}/README.md"><img src="{prefix}workflows/{r["slug"]}/canvas.svg" alt="{r["num"]} canvas"></a><br/><b>{r["num"]}</b> · {r["title"]}</td>')
        g.append("</tr>")
    return g + ["</table>"]
rs = [r for r in REGISTRY if not r["num"].endswith("a")]
HIGHLIGHTS = ("L01", "L15", "Q02", "P01", "P06", "X01")
gal = gallery([r for r in rs if r["num"] in HIGHLIGHTS]) + ["", f"**[See all {len(rs)} canvases →](GALLERY.md)**"]
open(os.path.join(ROOT, "GALLERY.md"), "w").write("\n".join(['<div align="center">', "", "# 🖼️ Gallery", "",
    f"**Every workflow's canvas, {len(rs)} in total.** Click one to open its lesson.", "", "</div>", "", *gallery(rs), "",
    '<p align="center"><a href="README.md">← Back to the learning path</a></p>']) + "\n")
p = os.path.join(ROOT, "README.md"); s = open(p).read()
s = re.sub(r"<!-- LESSONS:START -->.*<!-- LESSONS:END -->", lambda m: "<!-- LESSONS:START -->\n" + "\n".join(blocks) + "\n<!-- LESSONS:END -->", s, flags=re.S)
s = re.sub(r"<!-- GALLERY:START -->.*<!-- GALLERY:END -->", lambda m: "<!-- GALLERY:START -->\n" + "\n".join(gal) + "\n<!-- GALLERY:END -->", s, flags=re.S)
open(p, "w").write(s)
print("README tables + gallery updated")

# ---- counts quoted in the docs come from the test fixtures and REGISTRY, never typed by hand
sys.path.insert(0, os.path.join(ROOT, "tests"))
from fixtures import EXPECT
n_checks = sum(map(len, EXPECT.values()))
n_wf = len(os.listdir(os.path.join(ROOT, "workflows")))
n_run = n_wf - 1   # P10 (MCP server) is structure-checked only
by_track = {}
for r in REGISTRY:
    if r["num"].endswith("a") or r["level"].startswith("🐞"):
        continue
    by_track.setdefault(r["num"][0], []).append(r["num"])
n_core, n_quick, n_proj = len(by_track.get("L", [])), len(by_track.get("Q", [])), len(by_track.get("P", []))
n_lessons = n_core + n_quick + n_proj
last_q = f"Q{n_quick:02d}"
from exercises import EX
n_ex = sum(len(v) for v in EX.values())
for f in ("README.md", "tests/README.md", "docs/testing.md", "docs/architecture.md", "docs/quiz.md", "docs/real-world-guide.md"):
    p = os.path.join(ROOT, f); t = open(p).read()
    t = re.sub(r"\d+ behaviour checks", f"{n_checks} behaviour checks", t)
    t = re.sub(r"imports all \d+ workflows", f"imports all {n_wf} workflows", t)
    t = re.sub(r"runs \d+ of them", f"runs {n_run} of them", t)
    t = re.sub(r"runs \d+ of the \d+ workflows", f"runs {n_run} of the {n_wf} workflows", t)
    t = re.sub(r"✅ \d+ run ·", f"✅ {n_run} run ·", t)
    t = re.sub(r"building \d+ workflows,", f"building {n_lessons} workflows,", t)
    t = re.sub(r"across all \d+ workflows", f"across all {n_lessons} workflows", t)   # "all N workflows" alone also matches "imports all N workflows" above — too broad
    t = re.sub(r"\d+ real workflows", f"{n_lessons} real workflows", t)
    t = re.sub(r"Q01[–-]Q\d+", f"Q01–{last_q}", t)
    t = re.sub(r"workflows-\d+-7C3AED", f"workflows-{n_lessons}-7C3AED", t)
    if f == "README.md":   # "N quick wins" appears elsewhere (e.g. a rollout plan's "ship 3 quick wins") with an unrelated meaning
        t = re.sub(r"\d+ quick wins", f"{n_quick} quick wins", t)
        t = re.sub(r"\d+ practice challenges", f"{n_ex} practice challenges", t)
        t = re.sub(r"✅ \d+ \+ 30-question quiz", f"✅ {n_ex} + 30-question quiz", t)
    open(p, "w").write(t)
banner = os.path.join(ROOT, "assets", "banner.svg")
if os.path.exists(banner):
    t = open(banner).read()
    t = re.sub(r"\d+ real workflows", f"{n_lessons} real workflows", t)
    open(banner, "w").write(t)
print(n_checks, "behaviour checks ·", n_lessons, "lessons ·", n_quick, "quick wins")

import roadmap
roadmap.build(os.path.join(ROOT, "assets", "learning-path.svg"))
print("roadmap drawn")
