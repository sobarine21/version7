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
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            insights = response.json()

            if "error" in insights:
                st.error(f"API Error: {insights['error']}")
            else:
                st.subheader("Insights:")
                st.write(f"**Summary:** {insights.get('summary', 'N/A')}")
                st.write(f"**Response:** {insights.get('response', 'N/A')}")
                st.write(f"**Highlights:** {insights.get('highlights', 'N/A')}")
                st.write(f"**Tasks:** {insights.get('tasks', 'N/A')}")
                st.write(f"**Sentiment:** {insights.get('sentiment', 'N/A')}")
                st.write(f"**Clarity Score:** {insights.get('clarity_score', 'N/A')}")
                st.write(f"**Scenario Response:** {insights.get('scenario_response', 'N/A')}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to API: {e}")
        except json.JSONDecodeError:
            st.error("Invalid JSON response from API.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
