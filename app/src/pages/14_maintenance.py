import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.menubar import SideBarLinks

st.set_page_config(layout="wide")

SideBarLinks()

# Page title
st.title("Maintenance Schedules")

try:
  data = requests.get('http://api:4000/ad/maintenance').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)

st.title('Create New Maintenance Schedule')

# Form for adding a new maintenance schedule
with st.form("new_maintenance_schedule_form"):
    # Input fields
    description = st.text_area("Description", help="Provide a brief description of the maintenance.")
    start_time = st.text_input(
        "Start Time",
        placeholder="YYYY-MM-DD HH:MM:SS",
        help="Enter the start time in the format YYYY-MM-DD HH:MM:SS"
    )
    end_time = st.text_input(
        "End Time",
        placeholder="YYYY-MM-DD HH:MM:SS",
        help="Enter the end time in the format YYYY-MM-DD HH:MM:SS"
    )
    performed_by = st.number_input("Performed By (Admin ID)", min_value=1, help="Enter the Admin ID responsible for this maintenance.")

    # Submit button
    submit_button = st.form_submit_button("Create Maintenance Schedule")

    # Handle form submission
    if submit_button:
        # Validate input fields
        if not description:
            st.error("Please provide a description for the maintenance.")
        elif not start_time:
            st.error("Please provide a valid start time.")
        elif not end_time:
            st.error("Please provide a valid end time.")
        elif performed_by <= 0:
            st.error("Please provide a valid Admin ID.")
        else:
            # Package data for the API
            maintenance_data = {
                "description": description,
                "start_time": start_time,
                "end_time": end_time,
                "performed_by": int(performed_by),
            }

            # Log the data
            logger.info(f"Submitting maintenance schedule: {maintenance_data}")

            # Make the API call
            try:
                # Replace with your API endpoint
                response = requests.post("http://api:4000/ad/maintenance", json=maintenance_data)

                # Handle the response
                if response.status_code == 201:
                    st.success("Maintenance schedule created successfully!")
                else:
                    st.error(f"Error creating maintenance schedule: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the server: {str(e)}")