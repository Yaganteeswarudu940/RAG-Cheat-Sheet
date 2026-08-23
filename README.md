
# The RAG Stack — Streamlit study app

An interactive interview-prep companion for the RAG Stack cheat sheet: the same
13 topic sections, rapid-fire Q&A, and numbers-to-memorize table as the Excel
workbook, navigable from a left-hand sidebar with the content on the right.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

## What's inside

- `app.py` — the Streamlit application.
- `data.py` — all cheat-sheet content (definitions, reference tables, facts,
  quirks, and Q&A) as plain Python data, extracted from the same source used
  to build the Excel workbook.
- `The_RAG_Stack_Cheat_Sheet.xlsx` — the original workbook, offered as a
  sidebar download inside the app.

## Using it

- **Left sidebar** — click any of the 13 core sections, or jump to the
  Rapid-fire Q&A / Numbers-to-memorize study tools.
- **Search box** — searches definitions, facts, quirks, and Q&A across every
  section at once; click "Open full section" on a result to jump there.
- **Reveal Q&A answers by default** — toggle in the sidebar. Off by default so
  you can test yourself (click a question to reveal its answer); turn it on
  to read straight through.
- **Tabs on each section page** — Know cold / Reference tables / Facts &
  gotchas / Interview Q&A — plus Previous/Next buttons at the bottom to read
  straight through in order.

## Editing content

All text lives in `data.py` as three plain Python lists (`SECTIONS`,
`RAPID_FIRE`, `NUMBERS`) — edit them directly and Streamlit will pick up the
change on refresh (or automatically if you have `streamlit run` file-watching
enabled, which is the default).
