# AI Interview Prep Hub — Streamlit study app

An interactive interview-prep companion covering **two** cheat sheets in one
app: **The RAG Stack** (13 sections) and **Prompt Engineering** (24
sections) — each with its own rapid-fire Q&A round and numbers-to-memorize
table, navigable from a left-hand sidebar with the content on the right.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

## What's inside

- `app.py` — the Streamlit application.
- `data_rag.py` — all RAG Stack content (definitions, reference tables,
  facts, quirks, Q&A), extracted from the same source used to build
  `The_RAG_Stack_Cheat_Sheet.xlsx`.
- `data_pe.py` — all Prompt Engineering content, extracted from the same
  source used to build `Prompt_Engineering_Cheat_Sheet.xlsx`.
- `The_RAG_Stack_Cheat_Sheet.xlsx` / `Prompt_Engineering_Cheat_Sheet.xlsx` —
  the original workbooks, offered as sidebar downloads inside the app.

## Using it

- **Choose your subject** — at the top of the sidebar, switch between
  "🧩 The RAG Stack" and "🗣️ Prompt Engineering." Switching resets you to
  that subject's first section and clears any active search.
- **Left sidebar** — click any core section, or jump to that subject's
  Rapid-fire Q&A / Numbers-to-memorize study tools.
- **Search box** — searches definitions, facts, quirks, and Q&A *within the
  currently selected subject*; click "Open full section" on a result to
  jump there. Switch subjects first if you're not sure which one a term
  belongs to.
- **Reveal Q&A answers by default** — toggle in the sidebar. Off by default
  so you can test yourself (click a question to reveal its answer); turn it
  on to read straight through. Applies to whichever subject is active.
- **Tabs on each section page** — Know cold / Reference tables / Facts &
  gotchas / Interview Q&A — plus Previous/Next buttons at the bottom to read
  straight through in order.
- **Download as Excel** — downloads whichever subject's workbook is
  currently selected.

## Editing content

All text lives in `data_rag.py` and `data_pe.py` as plain Python lists
(`SECTIONS`, `RAPID_FIRE`, `NUMBERS`) — edit them directly and Streamlit
will pick up the change on refresh. Each entry in `SECTIONS` needs a unique
`id` (used for sidebar navigation and the Previous/Next order) — if you add
a new section, give it a slug that isn't already used within that subject.

## Adding a third subject

1. Create `data_<subject>.py` with the same `SECTIONS` / `RAPID_FIRE` /
   `NUMBERS` shape as the existing modules (each section needs: `num`,
   `eyebrow`, `title`, `core`, `defs`, `tables`, `facts`, `quirks`, `qa`,
   `id`).
2. `import data_<subject>` at the top of `app.py` and add an entry to the
   `COURSES` dict with a `label`, `short_label`, `subtitle`, `icon`, the
   three data lists, and an `xlsx_file` name (optional — the download
   button only appears if that file exists next to `app.py`).
3. That's it — the sidebar switcher, search, and all page renderers already
   loop over `COURSES`, so a third subject needs no other code changes.
