import logging
import requests
import streamlit as st
from modules.menubar import SideBarLinks

# Set up logging
logger = logging.getLogger(__name__)

# Configure Streamlit app
st.set_page_config(layout="wide")
SideBarLinks()

# Initialize session state for active tab and maintenance data
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "View Maintenance"
if "maintenance_data" not in st.session_state:
    st.session_state["maintenance_data"] = None

# Define the tabs
tabs = ["View Maintenance", "Create Maintenance", "Update Maintenance", "Delete Maintenance"]
active_tab = st.radio("Select Tab", tabs, horizontal=True)

# Check if the active tab has changed
if active_tab != st.session_state["active_tab"]:
    st.session_state["active_tab"] = active_tab
    if active_tab == "View Maintenance":
        # Fetch maintenance data dynamically
        try:
            st.session_state["maintenance_data"] = requests.get("http://api:4000/ad/maintenance").json()
        except requests.exceptions.RequestException as e:
            st.session_state["maintenance_data"] = None
            st.error(f"Failed to fetch maintenance schedules: {str(e)}")

# Tab 1: View Maintenance
if st.session_state["active_tab"] == "View Maintenance":
    st.header("View Maintenance Schedules")
    maintenance_data = st.session_state["maintenance_data"]
    if maintenance_data:
        st.dataframe(maintenance_data)
    else:
        st.error("No maintenance schedules to display or failed to fetch data.")

# Tab 2: Create Maintenance
elif st.session_state["active_tab"] == "Create Maintenance":
    st.header("Create New Maintenance Schedule")
    with st.form("new_maintenance_form"):
        description = st.text_area("Description", help="Provide a brief description of the maintenance.")
        start_time = st.text_input("Start Time", placeholder="YYYY-MM-DD HH:MM:SS")
        end_time = st.text_input("End Time", placeholder="YYYY-MM-DD HH:MM:SS")
        performed_by = st.number_input("Performed By (Admin ID)", min_value=1, step=1)

        submit_button = st.form_submit_button("Create Maintenance Schedule")
        if submit_button:
            if not description or not start_time or not end_time or performed_by <= 0:
                st.error("All fields are required!")
            else:
                data = {
                    "description": description,
                    "startTime": start_time,
                    "endTime": end_time,
                    "performedBy": int(performed_by),
                }
                try:
                    response = requests.post("http://api:4000/ad/maintenance", json=data)
                    if response.status_code == 201:
                        st.success("Maintenance schedule created successfully!")
                        st.session_state["maintenance_data"] = requests.get("http://api:4000/ad/maintenance").json()
                    else:
                        st.error(f"Failed to create maintenance schedule: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the server: {str(e)}")

# Tab 3: Update Maintenance
elif st.session_state["active_tab"] == "Update Maintenance":
    st.header("Update Maintenance Schedule")
    with st.form("update_maintenance_form"):
        maintenance_id = st.number_input("Maintenance ID", min_value=1, step=1)
        description = st.text_area("Description (Optional)")
        start_time = st.text_input("Start Time (Optional)", placeholder="YYYY-MM-DD HH:MM:SS")
        end_time = st.text_input("End Time (Optional)", placeholder="YYYY-MM-DD HH:MM:SS")
        performed_by = st.number_input("Performed By (Admin ID, Optional)", min_value=0, step=1)

        submit_button = st.form_submit_button("Update Maintenance")
        if submit_button:
            if maintenance_id <= 0:
                st.error("Please provide a valid Maintenance ID.")
            else:
                data = {}
                if description:
                    data["description"] = description
                if start_time:
                    data["startTime"] = start_time
                if end_time:
                    data["endTime"] = end_time
                if performed_by > 0:
                    data["performedBy"] = int(performed_by)

                if not data:
                    st.error("At least one field must be updated.")
                else:
                    try:
                        response = requests.put(f"http://api:4000/ad/maintenance/{maintenance_id}", json=data)
                        if response.status_code == 200:
                            st.success(f"Maintenance ID {maintenance_id} updated successfully!")
                            st.session_state["maintenance_data"] = requests.get("http://api:4000/ad/maintenance").json()
                        else:
                            st.error(f"Failed to update maintenance: {response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to the server: {str(e)}")

# Tab 4: Delete Maintenance
elif st.session_state["active_tab"] == "Delete Maintenance":
    st.header("Delete Maintenance Schedule")
    with st.form("delete_maintenance_form"):
        maintenance_id = st.number_input("Maintenance ID", min_value=1, step=1)
        submit_button = st.form_submit_button("Delete Maintenance")

        if submit_button:
            if maintenance_id <= 0:
                st.error("Please provide a valid Maintenance ID.")
            else:
                try:
                    response = requests.delete(f"http://api:4000/ad/maintenance/{maintenance_id}")
                    if response.status_code == 200:
                        st.success(f"Maintenance ID {maintenance_id} deleted successfully!")
                        st.session_state["maintenance_data"] = requests.get("http://api:4000/ad/maintenance").json()
                    elif response.status_code == 404:
                        st.error(f"Maintenance ID {maintenance_id} not found.")
                    else:
                        st.error(f"Failed to delete maintenance: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the server: {str(e)}")
