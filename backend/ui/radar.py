import streamlit as st
import pandas as pd
import plotly.express as px
from ui.radar_db import get_opportunities

def render_radar():
    st.title("🎯 Opportunity Radar")
    st.markdown("Identify and compare potential product opportunities. **Note: Evidence volume does not equal business impact.**")
    
    with st.spinner("Analyzing opportunities..."):
        opportunities = get_opportunities()
        
    if not opportunities:
        st.info("No validated opportunities found in the current dataset.")
        return
        
    st.subheader("Opportunity Landscape")
    
    # Create comparison dataframe
    df = pd.DataFrame(opportunities)
    df["Opportunity Name"] = df["barrier"] + " - " + df["unmet_need"]
    
    fig = px.scatter(
        df, 
        x="volume", 
        y="direct_count", 
        size="volume", 
        color="strength", 
        hover_name="Opportunity Name",
        title="Evidence Volume vs. Direct Evidence Strength",
        labels={"volume": "Total Evidence Volume", "direct_count": "Direct Evidence Count"}
    )
    fig.update_layout(font=dict(color="#1f2937"))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("Detailed Opportunities")
    for opp in opportunities:
        with st.container():
            st.markdown(f"### {opp['barrier'].title()}")
            st.markdown(f"**Unmet Need / Problem:** {opp['unmet_need']}")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Volume", opp['volume'])
            col2.metric("Direct Evidence", opp['direct_count'])
            col3.metric("Indirect Evidence", opp['indirect_count'])
            col4.metric("Evidence Strength", opp['strength'])
            
            st.markdown("💡 **Potential Product Opportunity (Hypothesis):**")
            st.info(f"Based on the evidence, exploring solutions around '{opp['barrier']}' could address the unmet need for '{opp['unmet_need']}'. **This is an evidence-backed hypothesis, not a guaranteed conversion driver.** Additional validation is required.")
            
            with st.expander("View Representative Evidence"):
                tier_map = {
                    "validated_relevant": "Direct Evidence",
                    "ai_direct_evidence": "Direct Evidence",
                    "indirect_pre_purchase": "Indirect Pre-Purchase",
                    "ai_indirect_evidence": "Indirect Pre-Purchase",
                    "ai_unvalidated": "Needs Validation"
                }
                for rev in opp['representative_reviews']:
                    display_tier = tier_map.get(rev['tier'], "Excluded")
                    st.markdown(f"**Evidence Type:** {display_tier}")
                    st.write(rev['text'])
                    
            st.markdown("---")
