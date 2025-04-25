# app.py

import streamlit as st
from agents import policy_rag_with_mcp, security_analysis_with_mcp

st.set_page_config(page_title="NeoEdge Autonomous Ops", layout="wide")

st.title("🧠 NeoEdge Autonomous Ops Assistant")
st.markdown("Interact with your company policies and security logs using AI-powered agents.")

tabs = st.tabs(["📘 HR PolicyBot", "🛡️ System MonitorBot"])

# --- HR PolicyBot ---
with tabs[0]:
    st.subheader("Ask a question about company policies")
    policy_query = st.text_area("Type your policy-related question below", height=100)
    if st.button("Ask PolicyBot", key="policy_button"):
        if policy_query.strip():
            with st.spinner("Thinking..."):
                policy_response = policy_rag_with_mcp(policy_query)
            st.success("✅ PolicyBot Response:")
            st.write(policy_response)
        else:
            st.warning("Please enter a valid question.")

# --- MonitorBot ---
with tabs[1]:
    st.subheader("Submit system logs for analysis")
    logs_input = st.text_area("Paste your logs below", height=200, placeholder="[ERROR] 2025-04-23 ...")
    if st.button("Analyze Logs", key="monitor_button"):
        if logs_input.strip():
            with st.spinner("Analyzing..."):
                analysis_response = security_analysis_with_mcp(logs_input)
            st.success("✅ MonitorBot Analysis:")
            st.write(analysis_response)
        else:
            st.warning("Please provide valid log content.")

st.markdown("---")
st.caption("Powered by CrewAI, LangChain, Cohere, and Streamlit | Built by Girish")
