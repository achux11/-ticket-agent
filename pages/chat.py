import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.llm import analyze_code
from utils.faiss_store import search_similar, add_ticket
from utils.db import save_ticket, init_db
from utils.github_api import create_github_issue, format_issue_body

init_db()

SAMPLE_CODE = '''def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    average = total / len(numbers)
    return average

result = calculate_average([])
print(result)'''

def render():
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);
    padding:2rem;border-radius:12px;margin-bottom:1.5rem;color:white;text-align:center'>
        <h1 style='margin:0;font-size:2rem'>🐛 Bug Ticket Agent</h1>
        <p style='margin:0.3rem 0 0;opacity:0.8'>
        Paste your code — AI will detect bugs and raise GitHub tickets automatically
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Code input
    st.subheader("📋 Paste your code")
    code = st.text_area(
        "Code to analyze",
        height=250,
        placeholder="Paste your Python, JavaScript, or any code here...",
        label_visibility="collapsed"
    )

    # Sample code button
    if st.button("💡 Load sample buggy code"):
        st.session_state.sample = True
        st.rerun()

    if st.session_state.get("sample"):
        code = SAMPLE_CODE
        st.code(SAMPLE_CODE, language="python")
        st.session_state.sample = False

    st.markdown("---")

    # Analyze button
    if st.button("🔍 Analyze & Raise Tickets", type="primary", use_container_width=True):
        if not code.strip():
            st.warning("Please paste some code first!")
            return

        # Step 1 — Analyze code
        with st.spinner("🤖 AI is analyzing your code for bugs..."):
            result = analyze_code(code)

        # Handle errors
        if "error" in result:
            st.error(f"❌ {result['error']}")
            return

        # No bugs found
        if not result.get("bugs_found"):
            st.success("✅ No bugs found! Your code looks good.")
            st.info(result.get("overall_summary", ""))
            return

        # Bugs found!
        bugs = result.get("bugs", [])
        st.warning(f"🐛 Found {len(bugs)} bug(s) in your code!")
        st.info(result.get("overall_summary", ""))

        st.markdown("---")

        # Process each bug
        for i, bug in enumerate(bugs):
            st.markdown(f"### Bug {i+1}: {bug['title']}")

            col1, col2 = st.columns(2)
            col1.markdown(f"**Severity:** {bug['severity']}")
            col2.markdown(f"**Category:** {bug['category']}")

            st.markdown(f"**Description:** {bug['description']}")
            st.markdown(f"**Suggested Fix:** {bug['suggested_fix']}")

            if bug.get("code_snippet"):
                st.code(bug["code_snippet"], language="python")

            # Step 2 — Check for duplicates in FAISS
            with st.spinner("🔍 Checking for duplicate tickets..."):
                similar = search_similar(f"{bug['title']} {bug['description']}")

            if similar:
                st.warning(f"⚠️ Similar ticket already exists: **{similar[0]['title']}** (Ticket #{similar[0]['ticket_id']})")
                st.caption("Skipping duplicate ticket creation.")
            else:
                # Step 3 — Create GitHub issue
                with st.spinner("📤 Creating GitHub issue..."):
                    issue_body = format_issue_body(bug, code)
                    github_result = create_github_issue(
                        title=bug["title"],
                        body=issue_body,
                        severity=bug["severity"]
                    )

                if github_result["success"]:
                    # Step 4 — Save to SQLite
                    ticket_id = save_ticket(
                        title=bug["title"],
                        description=bug["description"],
                        severity=bug["severity"],
                        category=bug["category"],
                        code_snippet=bug.get("code_snippet", ""),
                        suggested_fix=bug["suggested_fix"],
                        github_url=github_result["issue_url"],
                        github_number=github_result["issue_number"]
                    )

                    # Step 5 — Add to FAISS
                    add_ticket(ticket_id, bug["title"], bug["description"])

                    st.success(f"✅ Ticket #{ticket_id} created!")
                    st.markdown(f"🔗 [View on GitHub]({github_result['issue_url']})")
                else:
                    st.error(f"❌ GitHub error: {github_result['error']}")

            st.markdown("---")