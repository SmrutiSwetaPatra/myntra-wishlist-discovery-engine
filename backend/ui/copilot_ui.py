import streamlit as st
import asyncio
from app.engine.copilot import DiscoveryCopilot
from ui.db_utils import run_async
import json

def render_copilot():
    st.title("💬 Discovery Copilot")
    st.markdown("Ask natural language questions about wishlist behaviors and purchase barriers.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "copilot" not in st.session_state:
        copilot = DiscoveryCopilot()
        
        async def init_copilot():
            from app.db.session import AsyncSessionLocal
            async with AsyncSessionLocal() as session:
                await copilot.initialize(session)
                
        with st.spinner("Initializing AI Copilot..."):
            run_async(init_copilot())
            
        st.session_state.copilot = copilot
        
    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("evidence"):
                count = len(msg['evidence'])
                noun = "record" if count == 1 else "records"
                st.caption(f"Retrieved {count} relevant evidence {noun}.")
                for i, ev in enumerate(msg["evidence"], 1):
                    if isinstance(ev, dict):
                        ev_tier = ev.get('validation_status', 'Unknown')
                        ev_text = ev.get('raw_text', ev.get('text', ''))
                        ev_source = ev.get('source', 'Unknown')
                    else:
                        ev_tier = getattr(ev, 'validation_status', 'Unknown')
                        ev_text = getattr(ev, 'raw_text', '')
                        ev_source = getattr(ev, 'source', 'Unknown')
                        
                    with st.expander(f"[Evidence {i}] | Tier: {ev_tier}"):
                        st.markdown(
                            f"""
                            <div style="
                                font-size: 16px;
                                font-weight: 500;
                                line-height: 1.6;
                                color: #111827;
                                padding: 12px 16px;
                                border-left: 4px solid #9ca3af;
                                background-color: #f9fafb;
                                border-radius: 4px;
                                margin-bottom: 12px;
                            ">
                                {ev_text}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.caption(f"Source: {ev_source}")
            if msg.get("metrics"):
                st.markdown("**Deterministic Metrics:**")
                for m in msg["metrics"]:
                    st.text(m)

    # Chat input
    if prompt := st.chat_input("What are the biggest pre-purchase barriers?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Analyzing dataset..."):
                try:
                    result = run_async(st.session_state.copilot.query(prompt, session_id="streamlit_session"))
                    
                    st.markdown(result.answer)
                    
                    if result.metrics:
                        st.markdown("**Deterministic Metrics:**")
                        for m in result.metrics:
                            st.text(m)
                            
                    if result.evidence_cards:
                        count = len(result.evidence_cards)
                        noun = "record" if count == 1 else "records"
                        st.caption(f"Retrieved {count} relevant evidence {noun}.")
                        for i, ev in enumerate(result.evidence_cards, 1):
                            if isinstance(ev, dict):
                                ev_tier = ev.get('validation_status', 'Unknown')
                                ev_text = ev.get('raw_text', ev.get('text', ''))
                                ev_source = ev.get('source', 'Unknown')
                            else:
                                ev_tier = getattr(ev, 'validation_status', 'Unknown')
                                ev_text = getattr(ev, 'raw_text', '')
                                ev_source = getattr(ev, 'source', 'Unknown')
                                
                            with st.expander(f"[Evidence {i}] | Tier: {ev_tier}"):
                                st.markdown(
                                    f"""
                                    <div style="
                                        font-size: 16px;
                                        font-weight: 500;
                                        line-height: 1.6;
                                        color: #111827;
                                        padding: 12px 16px;
                                        border-left: 4px solid #9ca3af;
                                        background-color: #f9fafb;
                                        border-radius: 4px;
                                        margin-bottom: 12px;
                                    ">
                                        {ev_text}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                                st.caption(f"Source: {ev_source}")
                                
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": result.answer,
                        "evidence": result.evidence_cards,
                        "metrics": result.metrics
                    })
                except Exception as e:
                    st.error(f"Error executing query: {str(e)}")
