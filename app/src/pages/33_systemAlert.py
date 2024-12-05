import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.menubar import SideBarLinks

st.set_page_config(layout="wide")

SideBarLinks()

# Initialize session state to track active tab and data
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "View System Alerts"

if "alerts_data" not in st.session_state:
    st.session_state["alerts_data"] = None

# Tabs
tabs = ["View System Alerts", "Post a New System Alert", "Update System Alert"]
active_tab = st.radio("Select Tab", tabs, horizontal=True)

# Check if the tab has changed
if active_tab != st.session_state["active_tab"]:
    st.session_state["active_tab"] = active_tab  # Update session state
    if active_tab == "View System Alerts":
        # Refresh alerts data when switching to the "View" tab
        try:
            st.session_state["alerts_data"] = requests.get("http://api:4000/ad/alerts").json()
        except requests.exceptions.RequestException as e:
            st.session_state["alerts_data"] = None
            st.error(f"Failed to fetch alerts: {str(e)}")

# Tab 1: View System Alerts
if active_tab == "View System Alerts":
    st.header("View System Alerts")
    alerts_data = st.session_state.get("alerts_data")
    if alerts_data:
        st.dataframe(alerts_data)
    else:
        st.error("No alerts to display or failed to fetch data.")

# Tab 2: Post a New System Alert
elif active_tab == "Post a New System Alert":
    st.header("Post a New System Alert")
    with st.form("post_alert_form"):
        alert_description = st.text_area("Alert Description")
        alert_status = st.selectbox("Alert Status", options=["", "active", "resolved", "dismissed"])
        alert_notify_admin = st.number_input("Notify Admin ID", min_value=1, step=1)
        alert_triggered_by = st.number_input("Triggered By User ID", min_value=1, step=1)
        submit_button = st.form_submit_button("Post Alert")

        if submit_button:
            if not alert_description.strip():
                st.error("Please enter an alert description")
            elif not alert_status:
                st.error("Please select an alert status")
            else:
                alert_data = {
                    "description": alert_description,
                    "status": alert_status,
                    "notify_admin": alert_notify_admin,
                    "triggered_by": alert_triggered_by,
                }
                try:
                    response = requests.post("http://api:4000/ad/alerts", json=alert_data)
                    if response.status_code == 201:
                        st.success("System alert posted successfully!")
                        # Refresh the alerts data after posting
                        st.session_state["alerts_data"] = requests.get("http://api:4000/ad/alerts").json()
                    else:
                        st.error(f"Error posting alert: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")

# Tab 3: Update System Alert
elif active_tab == "Update System Alert":
    st.header("Update System Alert")
    alert_id = st.text_input("System Alert ID", help="Enter the ID of the alert you want to update")
    with st.form("update_alert_form"):
        status = st.selectbox(
            "Status",
            options=["", "active", "resolved", "dismissed"],
            help="Select the new status for the alert",
        )
        description = st.text_area("Description (optional)")
        submit_button = st.form_submit_button("Update Alert")

        if submit_button:
            if not alert_id:
                st.error("Please provide a System Alert ID")
            elif not status and not description:
                st.error("Please provide at least one field to update")
            else:
                update_data = {}
                if status:
                    update_data["status"] = status
                if description:
                    update_data["description"] = description
                try:
                    response = requests.put(f"http://api:4000/ad/alerts/{alert_id}", json=update_data)
                    if response.status_code == 200:
                        st.success(f"System alert with ID {alert_id} updated successfully!")
                        # Refresh the alerts data after update
                        st.session_state["alerts_data"] = requests.get("http://api:4000/ad/alerts").json()
                    elif response.status_code == 404:
                        st.error(f"System alert with ID {alert_id} not found.")
                    else:
                        st.error(f"Failed to update alert: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the server: {str(e)}")
