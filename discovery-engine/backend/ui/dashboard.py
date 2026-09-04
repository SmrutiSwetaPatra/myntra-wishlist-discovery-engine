import streamlit as st
import pandas as pd
import plotly.express as px
from ui.db_utils import get_dashboard_metrics

def render_dashboard():
    print("START RENDER DASHBOARD")
    st.title("📊 Discovery Dashboard")
    st.markdown("Overview of the Myntra Wishlist Discovery dataset.")
    
    with st.spinner("Loading metrics..."):
        print("CALLING GET_DASHBOARD_METRICS")
        metrics = get_dashboard_metrics()
        print("RETURNED GET_DASHBOARD_METRICS")
        
    # Top Row Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Collected Records", metrics["total_reviews"])
    with col2:
        st.metric("AI Analyzed/Embedded", metrics["analyzed"])
    with col3:
        st.metric("Google Play", metrics["sources"].get("Google Play", 0))
    with col4:
        st.metric("App Store / YouTube / Reddit", f"{metrics['sources'].get('Apple App Store', 0)} / {metrics['sources'].get('YouTube', 0)} / 0")
        
    st.markdown("---")
    
    # Evidence Validation Distribution
    st.subheader("Evidence Status")
    val_cols = st.columns(4)
    val_counts = metrics["validation_status"]
    with val_cols[0]:
        st.metric("✅ Direct Evidence", val_counts.get("Direct Evidence", 0))
    with val_cols[1]:
        st.metric("🟡 Indirect Pre-Purchase", val_counts.get("Indirect Pre-Purchase", 0))
    with val_cols[2]:
        st.metric("⏳ Needs Validation", val_counts.get("Needs Validation", 0))
    with val_cols[3]:
        st.metric("🚫 Excluded", val_counts.get("Excluded", 0))
        
    st.markdown("---")
    
    # Charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Top Barriers & Problems")
        barriers_df = pd.DataFrame(list(metrics["barriers"].items()), columns=["Barrier", "Count"])
        if not barriers_df.empty:
            barriers_df["Barrier"] = barriers_df["Barrier"].str.replace('_', ' ').str.title()
            fig1 = px.bar(barriers_df, x="Barrier", y="Count", color="Barrier", title="Primary Pre-Purchase Barriers")
            fig1.update_layout(font=dict(color="#1f2937"))
            st.plotly_chart(fig1, use_container_width=True)
            
    with chart_col2:
        st.subheader("Shopping Stage")
        stage_df = pd.DataFrame(list(metrics["stages"].items()), columns=["Stage", "Count"])
        if not stage_df.empty:
            stage_df["Stage"] = stage_df["Stage"].str.replace('_', ' ').str.title()
            fig2 = px.pie(stage_df, names="Stage", values="Count", title="Distribution by Shopping Stage", hole=0.4)
            fig2.update_layout(font=dict(color="#1f2937"))
            st.plotly_chart(fig2, use_container_width=True)
            
    chart_col3, chart_col4 = st.columns(2)
    with chart_col3:
        st.subheader("Purchase Intent")
        intent_df = pd.DataFrame(list(metrics["intents"].items()), columns=["Intent", "Count"])
        if not intent_df.empty:
            intent_df["Intent"] = intent_df["Intent"].str.replace('_', ' ').str.title()
            fig3 = px.bar(intent_df, x="Intent", y="Count", title="Purchase Intent Distribution")
            fig3.update_layout(font=dict(color="#1f2937"))
            st.plotly_chart(fig3, use_container_width=True)
            
    with chart_col4:
        st.subheader("Evidence Quality Tiers")
        quality_df = pd.DataFrame(list(metrics["quality"].items()), columns=["Quality", "Count"])
        if not quality_df.empty:
            quality_df["Quality"] = quality_df["Quality"].str.replace('_', ' ').str.title()
            fig4 = px.pie(quality_df, names="Quality", values="Count", title="AI Assigned Evidence Relevance", hole=0.4)
            fig4.update_layout(font=dict(color="#1f2937"))
            st.plotly_chart(fig4, use_container_width=True)
