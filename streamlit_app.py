import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://escalytics7version.onrender.com/api/insights"

# Load the authentication API key from environment variables
AUTH_API_KEY = os.getenv('AUTH_API_KEY')

if AUTH_API_KEY is None:
    st.error("Authentication API key not found. Please set the AUTH_API_KEY environment variable.")
    st.stop()  # Stop the app if the key is missing

st.title("Email Insights Generator")

email_content = st.text_area("Enter Email Content:", height=300)
scenario = st.selectbox("Select Scenario (for response generation):", ["General", "Urgent", "Formal", "Informal"])

if st.button("Generate Insights"):
    if not email_content:
        st.error("Please enter email content.")
    else:
        try:
            headers = {"X-API-KEY": AUTH_API_KEY}
            payload = {"email_content": email_content, "scenario": scenario}
            response = requests.post(API_URL, json=payload, headers=headers)

            if response.status_code == 401:
                st.error("Unauthorized access. Please check your API key.")
                #No return statement is needed here. st.stop() will stop execution.
                st.stop()

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

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to API: {e}")
        except json.JSONDecodeError:
            st.error("Invalid JSON response from API.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
