import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.menubar import SideBarLinks
SideBarLinks()

st.title("Find Students")

results = requests.get('http://api:4000/emp/students').json()

if results:
    for student in results:
        user_id = student.get('userID', 'N/A')
        email = student.get('email', 'N/A')
        phone = student.get('phoneNum', 'N/A')
        first_name = student.get('firstName', 'N/A')
        last_name = student.get('lastName', 'N/A')
        major = student.get('major', 'N/A')
        admit_year = student.get('admitYear', 'N/A')
        skills = student.get('skills', 'N/A')  

        with st.container():
            st.subheader(f"{first_name} {last_name}")
            st.write(f"**Email**: {email}")
            st.write(f"**Phone**: {phone}")
            st.write(f"**Major**: {major}")
            st.write(f"**Admit Year**: {admit_year}")
            st.write(f"**Skills**: {', '.join(skills) if isinstance(skills, list) else skills}")
            st.markdown("---") 
else:
    st.write("No student profiles available.")