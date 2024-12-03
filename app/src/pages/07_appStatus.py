import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.menubar import SideBarLinks
SideBarLinks()

import requests

st.title("Application Status")

# Section: Fetch Application Status
try:
    # Get student ID from session state
    student_id = st.session_state.get("user_id", 1)  # Default to 1 for testing
    response = requests.get(f"http://localhost:4000/Application/{student_id}")
    
    if response.status_code == 200:
        applications = response.json()
        if applications:
            st.subheader("Your Applications")
            for app in applications:
                st.write(f"### {app['title']}")
                st.write(f"**Company:** {app['companyName']}")
                st.write(f"**Position:** {app['positionTitle']}")
                st.write(f"**Status:** {app['status']}")
                st.write(f"**Submission Date:** {app['submissionDate']}")
                st.write(f"**Last Updated:** {app['lastUpdated']}")
                st.write("---")
        else:
            st.write("No applications found.")
    else:
        st.error("Failed to fetch application statuses. Please try again later.")
except Exception as e:
    st.error(f"An error occurred while fetching applications: {e}")