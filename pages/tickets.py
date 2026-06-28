import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.db import get_all_tickets, update_ticket_status, get_stats

SEVERITY_COLORS = {
    "Critical": "🔴",
    "High": "🟠",
    "Medium": "🟡",
    "Low": "🟢"
}

STATUS_OPTIONS = ["open", "in progress", "resolved", "closed"]

def render():
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);
    padding:2rem;border-radius:12px;margin-bottom:1.5rem;color:white;text-align:center'>
        <h1 style='margin:0;font-size:2rem'>🎫 Ticket Dashboard</h1>
        <p style='margin:0.3rem 0 0;opacity:0.8'>
        View and manage all raised bug tickets
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    stats = get_stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📨 Total Tickets", stats["total"])
    c2.metric("🔓 Open", stats["open"])
    c3.metric("🔴 Critical", stats["critical"])
    c4.metric("✅ Resolved", stats["resolved"])

    st.markdown("---")

    # Filter
    col1, col2 = st.columns(2)
    with col1:
        filter_severity = st.selectbox(
            "Filter by severity",
            ["All", "Critical", "High", "Medium", "Low"]
        )
    with col2:
        filter_status = st.selectbox(
            "Filter by status",
            ["All", "open", "in progress", "resolved", "closed"]
        )

    # Get tickets
    tickets = get_all_tickets()

    # Apply filters
    if filter_severity != "All":
        tickets = [t for t in tickets if t["severity"] == filter_severity]
    if filter_status != "All":
        tickets = [t for t in tickets if t["status"] == filter_status]

    if not tickets:
        st.info("No tickets found. Go to Bug Analyzer to create some!")
        return

    # Display tickets
    for ticket in tickets:
        severity_icon = SEVERITY_COLORS.get(ticket["severity"], "⚪")

        with st.expander(
            f"{severity_icon} #{ticket['id']} — {ticket['title']} | {ticket['status'].upper()}",
            expanded=False
        ):
            col_l, col_r = st.columns([2, 1])

            with col_l:
                st.markdown(f"**Severity:** {ticket['severity']}")
                st.markdown(f"**Category:** {ticket['category']}")
                st.markdown(f"**Description:** {ticket['description']}")
                st.markdown(f"**Suggested Fix:** {ticket['suggested_fix']}")
                st.markdown(f"**Created:** {ticket['created_at']}")

                if ticket["github_url"]:
                    st.markdown(f"🔗 [View on GitHub]({ticket['github_url']})")

                if ticket["code_snippet"]:
                    st.code(ticket["code_snippet"], language="python")

            with col_r:
                new_status = st.selectbox(
                    "Update status",
                    STATUS_OPTIONS,
                    index=STATUS_OPTIONS.index(ticket["status"])
                    if ticket["status"] in STATUS_OPTIONS else 0,
                    key=f"status_{ticket['id']}"
                )
                if st.button("💾 Save", key=f"save_{ticket['id']}", use_container_width=True):
                    update_ticket_status(ticket["id"], new_status)
                    st.success("Updated!")
                    st.rerun()