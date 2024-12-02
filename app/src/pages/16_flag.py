import logging
import requests

logger = logging.getLogger(__name__)

import streamlit as st
from modules.menubar import SideBarLinks

st.set_page_config(layout="wide")

SideBarLinks()

# Page title
st.title("Content Flags Management")

# Create tabs
tabs = st.tabs(["View Flags", "Update Flag Status"])

# Tab 1: View Flags
with tabs[0]:
    st.header("View Flags")
    try:
        # Fetch flag data from the API
        data = requests.get('http://api:4000/ad/flags').json()
    except:
        st.write("**Important**: Could not connect to sample API, so using dummy data.")
        data = {"a": {"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}
    
    # Display the data in a table
    st.dataframe(data)

# Tab 2: Update Flag Status
with tabs[1]:
    st.header("Update Flag Status")

    # Form to update flag status
    with st.form("update_flag_form"):
        # Input for flag ID
        flag_id = st.number_input("Flag ID", min_value=1, step=1)

        # Dropdown for selecting the new status
        new_status = st.selectbox("New Status", options=["active", "resolved", "closed"], index=0)

        # Submit button
        submit_button = st.form_submit_button("Update Status")

        # Handle form submission
        if submit_button:
            if not flag_id:
                st.error("Please enter a valid Flag ID.")
            elif not new_status:
                st.error("Please select a status.")
            else:
                # Prepare the data for the PUT request
                update_data = {"status": new_status}
                try:
                    # Send the PUT request to the backend
                    response = requests.put(
                        f"http://api:4000/flags/{flag_id}",
                        json=update_data
                    )
                    if response.status_code == 200:
                        st.success(f"Flag ID {flag_id} updated to '{new_status}' successfully!")
                    else:
                        st.error(f"Failed to update flag: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the server: {str(e)}")
