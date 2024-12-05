import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.menubar import SideBarLinks
import pandas as pd
SideBarLinks()

user_id = st.session_state['user id']
job_options = []
company_options = []

try:
    response = requests.get(f"http://api:4000/stu/Jobs")
    if response.status_code == 200:
        data = pd.DataFrame(response.json())
        job_data = response.json()
        titles = list(data['title'])
        ids = list(data['jobID'])
        description = list(data['description'])
        company_ids = list(data['companyID'])

        for i in range(len(titles)):
            job_options.append((titles[i], ids[i], description[i], company_ids[i]))
    else:
        st.error("Failed to fetch job information.")
except Exception as e:
    st.error(f"Error connecting to the server: {e}")

try:
    response = requests.get(f"http://api:4000/stu/Employers")
    if response.status_code == 200:
        company_data = pd.DataFrame(response.json())

        compid = list(company_data['companyID'])
        compname = list(company_data['name'])

        for i in range(len(compid)):
            company_options.append((compid[i], compname[i]))    
    else:
        st.error("Failed to fetch company information.")
except Exception as e:
    st.error(f"Error connecting to the server: {e}")

if job_options:
    title, job_id, description, company_id = st.selectbox(
        "Select Job",
        options=job_options,
        format_func=lambda x: x[0] if isinstance(x, tuple) else "No Jobs Available",
        index=0
    )
else:
    st.error("No Jobs available")
    st.stop()

company_name = [v[1] for _, v in enumerate(company_options) if v[0] == company_id][0]

st.header("Job Title: " +title)
st.subheader("Company: " + str(company_name))
st.write("Description:")
st.write(description)


if st.button("Apply"):
    if job_id:
        app_data = {
            "studentID": user_id,
            "jobID": job_id,
            "status": "pending"
        }
        try:
            response = requests.post("http://api:4000/stu/Apply", json=app_data)
            if response.status_code == 201:
                st.success("Successful Application!")
            else:
                st.error(f"Failed to apply. Error: {response.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error connecting to the server: {e}")

