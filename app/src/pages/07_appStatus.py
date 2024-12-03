import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.menubar import SideBarLinks
SideBarLinks()

st.title("Application Status")

# Determine role from session state
role_response = requests.get(f"http://api:4000/emp/role/{st.session_state['user id']}").json()
if role_response and isinstance(role_response, list):
    role = role_response[0].get("role", "").lower()

user_id = st.session_state['user id']

if role == "student":
    st.subheader("Your Applications")
    response = requests.get(f"http://api:4000/stu//applications/student/{user_id}")
    applications = response.json()

    if isinstance(applications, list) and applications:
        for app in applications:
            job_title = app.get('jobTitle', 'N/A')
            company_name = app.get('companyName', 'N/A')
            employer_name = app.get('employerName', 'N/A')
            status = app.get('status', 'N/A')
            date_submitted = app.get('dateSubmitted', 'N/A')

            with st.container():
                st.write(f"**Job Title:** {job_title}")
                st.write(f"**Company:** {company_name}")
                st.write(f"**Employer:** {employer_name}")
                st.write(f"**Status:** {status}")
                st.write(f"**Date Submitted:** {date_submitted}")
                st.markdown("---")
    else:
        st.write("No applications found.")

# elif role == "employer":
#     st.subheader("Job Applications to Your Posts")
#     response = requests.get(f"http://api:4000/applications/employer/{user_id}")
#     applications = response.json()

#     if isinstance(applications, list) and applications:
#         for app in applications:
#             job_title = app.get('jobTitle', 'N/A')
#             company_name = app.get('companyName', 'N/A')
#             student_name = app.get('studentName', 'N/A')
#             status = app.get('status', 'N/A')
#             date_submitted = app.get('dateSubmitted', 'N/A')

#             with st.container():
#                 st.write(f"**Job Title:** {job_title}")
#                 st.write(f"**Company:** {company_name}")
#                 st.write(f"**Student:** {student_name}")
#                 st.write(f"**Status:** {status}")
#                 st.write(f"**Date Submitted:** {date_submitted}")
#                 st.markdown("---")
#     else:
#         st.write("No applications found.")
else:
    st.error("Invalid user role or user not found.")