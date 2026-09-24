# Contributing a workflow

Thanks for helping others learn! A good lesson solves **one real problem** and teaches **one or two new concepts**.

## Checklist
- [ ] A **Concept first** entry in `tools/concepts.py` (key idea, mental model, when not to use it).
- [ ] Two **practice challenges** (⭐ and ⭐⭐) with hint + solution in `tools/exercises.py`.
- [ ] Projects: 3–5 **design decisions** in `tools/decisions.py`.
- [ ] A sample event / fixtures and at least one **behaviour check** in `tests/fixtures.py`; `tests/harness.py` passes.
- [ ] Folder `workflows/Lxx-short-name/` with `workflow.json` + `README.md` (copy an existing README's sections: problem, what you'll learn, flow, credentials, build steps, test, common errors, level up).
- [ ] A sticky note on the canvas saying what to configure.
- [ ] If a node's output is gated by a **computed, non-obvious condition** (a threshold, a diff against remembered state, a dedupe check) and nothing else on the canvas explains it, add a second sticky note right at that node: what it takes for the gate to pass, and how to force a pass while testing. Use `w.note(content, (x, y), width, height, color=4)` positioned at the *node's own x/y* — `tools/render.py`'s `canvas_svg` folds it into the right spot automatically, even on a wide, two-row canvas. See Q02 and L21 for the pattern.
- [ ] Settings live in a `⚙️ Config` Set node, not scattered across nodes.
- [ ] No credentials, no pinned data, no real emails or sheet IDs (`you@example.com`, `PASTE_YOUR_…`, `REPLACE_…`).
- [ ] Gemini as the default model unless the lesson is about another provider.
- [ ] Retry on Fail for external APIs (the builder adds it; `validate.py` fails without it), and a guard for empty results.
- [ ] `python3 tools/validate.py` passes (CI runs it).
- [ ] Run it once for real in n8n with the data in `docs/sample-data.md` (or your own): the harness mocks AI and credentialed nodes, so it can't catch a bad prompt.

## Export cleanly from n8n
1. Unpin all data.
2. *⋯ → Download*. Credentials are not exported, only their names; the validator removes nothing, so check.
3. Rename emails, sheet URLs and folder IDs to placeholders.

## Generated workflows
Every workflow, README, canvas snapshot and the lesson tables are generated from Python specs by `python3 tools/build.py`. Editing a `workflow.json` or README by hand gets overwritten on the next build, and CI fails if the committed files differ from a fresh build.

**Adding a lesson (e.g. L23):**
1. Build and test it in n8n first, then *Download* the JSON.
2. Add a spec function to the right file (`tools/level3_4.py`, `quickwins.py` or `projects.py`) and to its `ALL` list. Either write it with `w.add(...)` like its neighbours, or drop your exported JSON into `workflows/L23-slug/workflow.json` and load it with `convert(...)` (see L12–L18 in `level3_4.py`).
3. Add entries to `tools/concepts.py`, `tools/exercises.py` and, for projects, `tools/decisions.py`.
4. In `tests/fixtures.py`: a sample event in `TRIGGERS` (if it isn't a schedule/manual trigger), mocks in `FIXTURES` for Sheets reads and anything else credentialed, and at least one `EXPECT` check.
5. Install n8n 2.40.5 once (`mkdir ~/n8n && cd ~/n8n && npm i n8n@2.40.5`), then run `python3 tools/build.py && N8N_DIR=~/n8n python3 tests/harness.py L23 && python3 tools/build.py` (the second build picks up the test results for badges and sheet templates).
6. `python3 tools/validate.py` must pass.
