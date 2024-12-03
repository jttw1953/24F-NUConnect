import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.menubar import SideBarLinks
import datetime
SideBarLinks()

st.title("Post a Job")

user_id = 81
company_options = []

try:
    response = requests.get(f"http://api:4000/emp/company/{user_id}")
    if response.status_code == 200:
        company_data = response.json()
        company_options.append((company_data["companyID"], company_data["companyName"]))
    else:
        st.error("Failed to fetch company information.")
except Exception as e:
    st.error(f"Error connecting to the server: {e}")


if company_options:
    company_id, company_name = st.selectbox(
        "Select Company",
        options=company_options,
        format_func=lambda x: x[1] if isinstance(x, tuple) else "No Company Available",
        index=0
    )
else:
    st.error("No companies available for this employer.")
    st.stop()

job_title = st.text_input("Job Title", placeholder="Enter the job title")
job_description = st.text_area("Job Description", placeholder="Enter a detailed description of the job")
deadline = st.date_input("Application Deadline", min_value=datetime.date.today(), help="Select the deadline for applications")
salary = st.text_input("Salary", placeholder="Enter the salary range or amount (optional)")

if st.button("Post Job"):
    if company_id and job_title and job_description and deadline:
        st.info(f"Deadline: {deadline.strftime('%Y-%m-%d')}")

        job_data = {
            "companyID": company_id,
            "title": job_title,
            "description": job_description
        }
        try:
            response = requests.post("http://api:4000/emp/job", json=job_data)
            if response.status_code == 201:
                st.success("Job posted successfully!")
            else:
                st.error(f"Failed to post job. Error: {response.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error connecting to the server: {e}")
    else:
        st.warning("Please fill in all fields before posting the job.")
