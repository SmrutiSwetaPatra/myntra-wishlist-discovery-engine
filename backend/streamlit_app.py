import streamlit as st
from ui.dashboard import render_dashboard
from ui.explorer import render_explorer
from ui.copilot_ui import render_copilot
from ui.radar import render_radar
import asyncio

st.set_page_config(
    page_title="Myntra Discovery Copilot",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.sidebar.title("🛍️ Discovery Copilot")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Evidence Explorer", "Discovery Copilot", "Opportunity Radar"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Evidence-Backed Product Discovery")
    
    if page == "Dashboard":
        render_dashboard()
    elif page == "Evidence Explorer":
        render_explorer()
    elif page == "Discovery Copilot":
        render_copilot()
    elif page == "Opportunity Radar":
        render_radar()

if __name__ == "__main__":
    main()
