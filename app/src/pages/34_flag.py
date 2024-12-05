import logging
import requests
import streamlit as st
from modules.menubar import SideBarLinks

# Set up logging
logger = logging.getLogger(__name__)

# Configure Streamlit app
st.set_page_config(layout="wide")
SideBarLinks()

# Initialize session state for active tab and content flags data
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "View Content Flags"
if "flags_data" not in st.session_state:
    st.session_state["flags_data"] = None

# Define the tabs
tabs = ["View Content Flags", "Post Content Flag", "Update Content Flag", "Delete Content Flag"]
active_tab = st.radio("Select Tab", tabs, horizontal=True)

# Check if the active tab has changed
if active_tab != st.session_state["active_tab"]:
    st.session_state["active_tab"] = active_tab
    if active_tab == "View Content Flags":
        # Fetch content flags data dynamically
        try:
            st.session_state["flags_data"] = requests.get("http://api:4000/ad/flags").json()
        except requests.exceptions.RequestException as e:
            st.session_state["flags_data"] = None
            st.error(f"Failed to fetch content flags: {str(e)}")

# Tab 1: View Content Flags
if st.session_state["active_tab"] == "View Content Flags":
    st.header("View Content Flags")
    flags_data = st.session_state["flags_data"]
    if flags_data:
        st.dataframe(flags_data)
    else:
        st.error("No content flags to display or failed to fetch data.")

# Tab 2: Post Content Flag
elif st.session_state["active_tab"] == "Post Content Flag":
    st.header("Post Content Flag")
    with st.form("post_flag_form"):
        content_id = st.number_input("Content ID", min_value=1, step=1, help="Enter the ID of the content to flag")
        reason = st.text_area("Reason", help="Provide a reason for flagging this content")
        status = st.selectbox("Status", options=["", "active", "resolved", "closed"], help="Select the status of the flag")        
        submit_button = st.form_submit_button("Post Content Flag")

        if submit_button:
            if not content_id:
                st.error("Please enter a valid Content ID")
            elif not reason.strip():
                st.error("Please provide a reason for the flag")
            elif not status:
                st.error("Please select a status")
            else:
                # Prepare the data for the POST request
                post_data = {
                    "contentID": content_id,
                    "reason": reason.strip(),
                    "status": status,
                }
                try:
                    # Send the POST request to the backend
                    response = requests.post("http://api:4000/ad/flags", json=post_data)
                    if response.status_code == 201:
                        st.success(f"Content flag created successfully for Content ID {content_id}!")
                        st.session_state["flags_data"] = requests.get("http://api:4000/ad/flags").json()
                    else:
                        st.error(f"Failed to create content flag: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the server: {str(e)}")

# Tab 3: Update Content Flag
elif st.session_state["active_tab"] == "Update Content Flag":
    st.header("Update Content Flag")
    with st.form("update_flag_form"):
        flag_id = st.number_input("Flag ID", min_value=1, step=1, help="Enter the ID of the flag you want to update")
        new_status = st.selectbox(
            "New Status",
            options=["", "active", "resolved", "closed"],
            help="Select the new status for the flag",
        )
        submit_button = st.form_submit_button("Update Flag")

        if submit_button:
            if not flag_id:
                st.error("Please provide a valid Flag ID")
            elif not new_status:
                st.error("Please select a status")
            else:
                update_data = {"status": new_status}
                try:
                    response = requests.put(f"http://api:4000/ad/flags/{flag_id}", json=update_data)
                    if response.status_code == 200:
                        st.success(f"Flag ID {flag_id} updated to '{new_status}' successfully!")
                        st.session_state["flags_data"] = requests.get("http://api:4000/ad/flags").json()
                    elif response.status_code == 404:
                        st.error(f"Flag ID {flag_id} not found.")
                    else:
                        st.error(f"Failed to update flag: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the server: {str(e)}")

# Tab 4: Delete Content Flag
elif st.session_state["active_tab"] == "Delete Content Flag":
    st.header("Delete Content Flag")
    with st.form("delete_flag_form"):
        flag_id = st.number_input("Flag ID", min_value=1, step=1, help="Enter the ID of the flag to delete")
        submit_button = st.form_submit_button("Delete Flag")

        if submit_button:
            if not flag_id:
                st.error("Please provide a valid Flag ID")
            else:
                try:
                    response = requests.delete(f"http://api:4000/ad/flags/{flag_id}")
                    if response.status_code == 200:
                        st.success(f"Flag with ID {flag_id} deleted successfully!")
                        st.session_state["flags_data"] = requests.get("http://api:4000/ad/flags").json()
                    elif response.status_code == 404:
                        st.error(f"Flag with ID {flag_id} not found.")
                    elif response.status_code == 405:
                        st.error(f"Method Not Allowed. Check if the DELETE endpoint is correctly set up.")
                    else:
                        st.error(f"Failed to delete flag: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the server: {str(e)}")
