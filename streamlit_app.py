import streamlit as st
import requests
import json

API_URL = "https://escalytics7version.onrender.com/api/insights"

st.title("Email Insights Generator")

email_content = st.text_area("Enter Email Content:", height=300)
scenario = st.selectbox("Select Scenario (for response generation):", ["General", "Urgent", "Formal", "Informal"])

if st.button("Generate Insights"):
    if not email_content:
        st.error("Please enter email content.")
    else:
        try:
            payload = {"email_content": email_content, "scenario": scenario}
            response = requests.post(API_URL, json=payload)
            insights = response.json()

            if "error" in insights:
                st.error(f"API Error: {insights['error']}")
            else:
                st.subheader("Insights:")
                st.write(f"**Summary:** {insights['summary']}")
                st.write(f"**Response:** {insights['response']}")
                st.write(f"**Highlights:** {insights['highlights']}")
                st.write(f"**Tasks:** {insights['tasks']}")
                st.write(f"**Sentiment:** {insights['sentiment']}")
                st.write(f"**Clarity Score:** {insights['clarity_score']}")
                st.write(f"**Scenario Response:** {insights['scenario_response']}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
