import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.menubar import SideBarLinks
SideBarLinks()

st.title("Find Employees")

# Fetch student data from the backend API
@st.cache_data
def fetch_students():
    api_url = "http://localhost:4000/employers/students"  # Adjust URL as needed
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch students")
        return []

students = fetch_students()

# Check if any students are returned
if students:
    # Dropdown to select a student
    student_names = [f"{student['name']} ({student['student_id']})" for student in students]
    selected_student = st.selectbox("Select a student to view their skills:", student_names)

    # Get the selected student's details
    selected_student_data = next(
        (student for student in students if f"{student['name']} ({student['student_id']})" == selected_student), None
    )

    if selected_student_data:
        st.subheader(f"Details for {selected_student_data['name']}")
        st.write(f"**Skills:** {selected_student_data['skills']}")
else:
    st.warning("No students found.")