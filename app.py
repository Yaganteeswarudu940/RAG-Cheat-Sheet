# -*- coding: utf-8 -*-
"""
AI Interview Prep Hub — Streamlit study app
Covers two interview-prep cheat sheets in one app: The RAG Stack, and
Prompt Engineering. Pick a subject in the sidebar; everything below it
(navigation, search, study tools) scopes to that subject.

Run with:
    pip install -r requirements.txt
    streamlit run app.py
"""

import os
import pandas as pd
import streamlit as st

import data_rag
import data_pe

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AI Interview Prep Hub",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

COURSES = {
    "rag": {
        "key": "rag",
        "label": "🧩 The RAG Stack",
        "short_label": "RAG Stack",
        "subtitle": "Interview-prep reference — tokenization → generation",
        "icon": "⚛️",
        "sections": data_rag.SECTIONS,
        "rapid_fire": data_rag.RAPID_FIRE,
        "numbers": data_rag.NUMBERS,
        "xlsx_file": "The_RAG_Stack_Cheat_Sheet.xlsx",
    },
    "pe": {
        "key": "pe",
        "label": "🗣️ Prompt Engineering",
        "short_label": "Prompt Engineering",
        "subtitle": "Interview-prep reference — instructions → reasoning → guardrails",
        "icon": "🗣️",
        "sections": data_pe.SECTIONS,
        "rapid_fire": data_pe.RAPID_FIRE,
        "numbers": data_pe.NUMBERS,
        "xlsx_file": "Prompt_Engineering_Cheat_Sheet.xlsx",
    },
}

AUTHOR_LINE = (
    "Dr. Akkem Yaganteeswarudu, Ph.D. NIT Silchar &nbsp;·&nbsp; "
    "Senior Data Scientist &nbsp;·&nbsp; Mobile: 8296655882"
)

# ---------------------------------------------------------------------------
# STYLING
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
    /* Streamlit's fixed top toolbar is ~60px tall (position: absolute, z-index: 999990) and
       overlaps the first ~60px of page content — pad past it so nothing renders underneath. */
    .block-container { padding-top: 5rem; padding-bottom: 3rem; max-width: 1100px; }
    .rag-header { margin-bottom: 0.9rem; }
    .rag-eyebrow {
        display: block;
        font-family: "Source Code Pro", monospace;
        font-size: 0.78rem;
        line-height: 1.6;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #8a8a8a;
        margin: 0 0 0.35rem 0;
    }
    .rag-title {
        font-size: 2.25rem;
        font-weight: 800;
        line-height: 1.2;
        margin: 0;
        color: inherit;
    }
    .rag-core {
        font-size: 1.05rem;
        font-style: italic;
        border-left: 3px solid #b75e27;
        padding: 0.6rem 1rem;
        border-radius: 4px;
        background: rgba(183, 94, 39, 0.08);
        margin-bottom: 1.2rem;
    }
    .rag-fact {
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.4rem;
        border-radius: 6px;
        background: rgba(60, 110, 116, 0.08);
        font-size: 0.95rem;
    }
    .rag-quirk {
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.4rem;
        border-radius: 6px;
        background: rgba(183, 94, 39, 0.10);
        font-size: 0.95rem;
    }
    .rag-footer {
        margin-top: 1.4rem;
        padding-top: 0.9rem;
        border-top: 1px solid rgba(128, 128, 128, 0.25);
        font-size: 0.8rem;
        color: #8a8a8a;
        text-align: center;
        line-height: 1.6;
    }
    .subject-badge {
        display: inline-block;
        font-family: "Source Code Pro", monospace;
        font-size: 0.72rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 0.15rem 0.55rem;
        border-radius: 999px;
        background: rgba(60, 110, 116, 0.15);
        margin-bottom: 0.6rem;
    }
    div[data-testid="stSidebarNav"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------

if "course" not in st.session_state:
    st.session_state.course = "rag"
if "reveal_answers" not in st.session_state:
    st.session_state.reveal_answers = False

COURSE = COURSES[st.session_state.course]
SECTIONS = COURSE["sections"]
RAPID_FIRE = COURSE["rapid_fire"]
NUMBERS = COURSE["numbers"]
SECTION_BY_ID = {s["id"]: s for s in SECTIONS}

# Defensive fallback: if "page" is unset, or holds an id that doesn't belong to the
# current course (e.g. stale state from before a course switch), snap to that
# course's first section rather than raising a KeyError further down.
_page_is_valid = st.session_state.get("page") in SECTION_BY_ID or st.session_state.get("page") in (
    "__rapidfire__",
    "__numbers__",
)
if not _page_is_valid:
    st.session_state.page = SECTIONS[0]["id"]


def go_to(page_id: str):
    st.session_state.page = page_id


def go_to_and_clear_search(page_id: str):
    st.session_state.page = page_id
    st.session_state.search_query = ""


def switch_course(course_key: str):
    st.session_state.course = course_key
    st.session_state.page = COURSES[course_key]["sections"][0]["id"]
    st.session_state.search_query = ""


# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### 📚 AI Interview Prep Hub")
    st.caption("Two cheat sheets, one place to cram.")

    st.markdown("**Choose your subject**")
    for key, c in COURSES.items():
        st.button(
            c["label"],
            key=f"course_{key}",
            on_click=switch_course,
            args=(key,),
            use_container_width=True,
            type="primary" if st.session_state.course == key else "secondary",
        )

    st.markdown(f"<span class='subject-badge'>{COURSE['icon']} {COURSE['short_label']}</span>", unsafe_allow_html=True)
    st.caption(COURSE["subtitle"])

    query = st.text_input(
        f"🔎 Search {COURSE['short_label']}",
        placeholder="type a keyword…",
        key="search_query",
    )

    st.markdown("**Core sections**")
    for s in SECTIONS:
        label = f"{s['num']}  {s['title'].split(' — ')[0]}"
        is_active = (not query) and st.session_state.page == s["id"]
        st.button(
            label,
            key=f"nav_{COURSE['key']}_{s['id']}",
            on_click=go_to_and_clear_search,
            args=(s["id"],),
            use_container_width=True,
            type="primary" if is_active else "secondary",
        )

    st.markdown("**Study tools**")
    st.button(
        "🎯  Rapid-fire Q&A",
        key=f"nav_{COURSE['key']}_rapidfire",
        on_click=go_to_and_clear_search,
        args=("__rapidfire__",),
        use_container_width=True,
        type="primary" if (not query and st.session_state.page == "__rapidfire__") else "secondary",
    )
    st.button(
        "🔢  Numbers to memorize",
        key=f"nav_{COURSE['key']}_numbers",
        on_click=go_to_and_clear_search,
        args=("__numbers__",),
        use_container_width=True,
        type="primary" if (not query and st.session_state.page == "__numbers__") else "secondary",
    )

    st.markdown("---")
    st.toggle("Reveal Q&A answers by default", key="reveal_answers")

    xlsx_path = os.path.join(os.path.dirname(__file__), COURSE["xlsx_file"])
    if os.path.exists(xlsx_path):
        with open(xlsx_path, "rb") as f:
            st.download_button(
                f"⬇️  Download {COURSE['short_label']} (Excel)",
                data=f.read(),
                file_name=COURSE["xlsx_file"],
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key=f"dl_{COURSE['key']}",
            )

# ---------------------------------------------------------------------------
# CONTENT RENDERERS
# ---------------------------------------------------------------------------


def render_header(eyebrow, title_html):
    st.markdown(
        f"<div class='rag-header'>"
        f"<span class='rag-eyebrow'>{eyebrow}</span>"
        f"<div class='rag-title'>{title_html}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(f"<div class='rag-footer'>{AUTHOR_LINE}</div>", unsafe_allow_html=True)


def render_defs(defs):
    df = pd.DataFrame(defs, columns=["Term", "Definition"])
    st.dataframe(df, hide_index=True, use_container_width=True, height=min(38 * len(df) + 40, 560))


def render_table(table):
    st.caption(table["caption"])
    df = pd.DataFrame(table["rows"], columns=table["headers"])
    st.dataframe(df, hide_index=True, use_container_width=True)


def render_facts(facts):
    for f in facts:
        st.markdown(f"<div class='rag-fact'>📌 {f}</div>", unsafe_allow_html=True)


def render_quirks(quirks):
    for q in quirks:
        st.markdown(f"<div class='rag-quirk'>⚠️ {q}</div>", unsafe_allow_html=True)


def render_qa(qa_list, key_prefix):
    for i, (q, a) in enumerate(qa_list):
        with st.expander(f"Q. {q}", expanded=st.session_state.reveal_answers):
            st.write(a)


def render_section(section):
    render_header(section["eyebrow"], f"{section['num']}. {section['title']}")
    st.markdown(f"<div class='rag-core'>{section['core']}</div>", unsafe_allow_html=True)

    tabs_needed = []
    if section["defs"]:
        tabs_needed.append("📖 Know cold")
    if section["tables"]:
        tabs_needed.append("📊 Reference tables")
    if section["facts"] or section["quirks"]:
        tabs_needed.append("🔢 Facts & gotchas")
    if section["qa"]:
        tabs_needed.append("🎯 Interview Q&A")

    tabs = st.tabs(tabs_needed)
    idx = 0

    if section["defs"]:
        with tabs[idx]:
            render_defs(section["defs"])
        idx += 1

    if section["tables"]:
        with tabs[idx]:
            for t in section["tables"]:
                render_table(t)
                st.markdown("")
        idx += 1

    if section["facts"] or section["quirks"]:
        with tabs[idx]:
            if section["facts"]:
                st.markdown("**Numbers & facts**")
                render_facts(section["facts"])
            if section["quirks"]:
                st.markdown("**Quirks & gotchas**")
                render_quirks(section["quirks"])
        idx += 1

    if section["qa"]:
        with tabs[idx]:
            render_qa(section["qa"], key_prefix=section["id"])

    # prev / next navigation
    st.markdown("---")
    pos = [s["id"] for s in SECTIONS].index(section["id"])
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if pos > 0:
            st.button("← Previous", on_click=go_to, args=(SECTIONS[pos - 1]["id"],), use_container_width=True)
    with col3:
        if pos < len(SECTIONS) - 1:
            st.button("Next →", on_click=go_to, args=(SECTIONS[pos + 1]["id"],), use_container_width=True)
        else:
            st.button("Rapid-fire Q&A →", on_click=go_to, args=("__rapidfire__",), use_container_width=True)

    render_footer()


def render_rapid_fire():
    render_header("Speed round", f"🎯 {COURSE['short_label']} — Rapid-fire Q&A")
    st.markdown(
        "<div class='rag-core'>Read the question, say the answer out loud, then check.</div>",
        unsafe_allow_html=True,
    )
    filt = st.text_input("Filter rapid-fire questions", placeholder="type to filter…", key="rf_filter")
    items = RAPID_FIRE
    if filt:
        items = [(q, a) for q, a in RAPID_FIRE if filt.lower() in q.lower() or filt.lower() in a.lower()]
    st.caption(f"{len(items)} of {len(RAPID_FIRE)} questions shown")
    render_qa(items, key_prefix="rf")
    render_footer()


def render_numbers():
    render_header("Muscle memory", f"🔢 {COURSE['short_label']} — Numbers Worth Memorizing")
    df = pd.DataFrame(NUMBERS, columns=["Metric", "Value"])
    st.dataframe(df, hide_index=True, use_container_width=True, height=38 * len(df) + 40)
    render_footer()


def render_search(query):
    render_header("Search results", f"🔎 Results for “{query}” in {COURSE['short_label']}")
    q_lower = query.lower()
    found_any = False

    for s in SECTIONS:
        hits = []
        for term, definition in s["defs"]:
            if q_lower in term.lower() or q_lower in definition.lower():
                hits.append(("Definition", term, definition))
        for fact in s["facts"]:
            if q_lower in fact.lower():
                hits.append(("Fact", "", fact))
        for quirk in s["quirks"]:
            if q_lower in quirk.lower():
                hits.append(("Quirk", "", quirk))
        for question, answer in s["qa"]:
            if q_lower in question.lower() or q_lower in answer.lower():
                hits.append(("Q&A", question, answer))
        if q_lower in s["title"].lower() or q_lower in s["core"].lower():
            hits.append(("Overview", "", s["core"]))

        if hits:
            found_any = True
            st.subheader(f"{s['num']}. {s['title']}")
            for kind, label, text in hits:
                prefix = f"**{label}** — " if label else ""
                st.markdown(f"<div class='rag-fact'>[{kind}] {prefix}{text}</div>", unsafe_allow_html=True)
            st.button(
                "Open full section →",
                key=f"open_{COURSE['key']}_{s['id']}",
                on_click=go_to_and_clear_search,
                args=(s["id"],),
            )
            st.markdown("---")

    for q, a in RAPID_FIRE:
        if q_lower in q.lower() or q_lower in a.lower():
            found_any = True
            st.markdown(f"<div class='rag-fact'>[Rapid-fire] **{q}** — {a}</div>", unsafe_allow_html=True)

    if not found_any:
        st.info(f"No matches in {COURSE['short_label']}. Try a shorter keyword, or switch subjects in the sidebar.")

    render_footer()


# ---------------------------------------------------------------------------
# ROUTING
# ---------------------------------------------------------------------------

if query:
    render_search(query)
elif st.session_state.page == "__rapidfire__":
    render_rapid_fire()
elif st.session_state.page == "__numbers__":
    render_numbers()
else:
    render_section(SECTION_BY_ID[st.session_state.page])
