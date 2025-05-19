
import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Change when deployed

st.title("🧠 Sentiment Analyzer (RoBERTa)")

option = st.radio("Choose analysis type:", ["Single", "Batch"])

if option == "Single":
    text = st.text_area("Enter your text")
    if st.button("Analyze"):
        if text:
            with st.spinner("Analyzing..."):
                resp = requests.post(f"{API_URL}/analyze_single", json={"text": text})
                st.json(resp.json())
        else:
            st.warning("Please enter some text.")

else:
    batch_input = st.text_area("Enter texts (one per line)")
    if st.button("Analyze Batch"):
        lines = [line.strip() for line in batch_input.strip().split("\n") if line.strip()]
        if lines:
            with st.spinner("Analyzing..."):
                resp = requests.post(f"{API_URL}/analyze_batch", json={"texts": lines})
                results = resp.json()
                for i, r in enumerate(results):
                    st.write(f"**Text {i+1}:**")
                    st.json(r)
        else:
            st.warning("Please enter at least one line.")
