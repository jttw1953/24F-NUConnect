import logging
import requests
import streamlit as st
from modules.menubar import SideBarLinks

logger = logging.getLogger(__name__)

SideBarLinks()

role_response = requests.get(f"http://api:4000/emp/role/{st.session_state['user id']}").json()
if role_response and isinstance(role_response, list):
    role = role_response[0].get("role", "").lower()
else:
    role = None

if role == "student":
    profile = requests.get(f"http://api:4000/stu/students/{st.session_state['user id']}").json()
    if profile:
        st.subheader("Student Profile")
        st.image(st.session_state['profile_pic'], width=150)
        st.write(f"**Name**: {profile.get('firstName', 'N/A')} {profile.get('lastName', 'N/A')}")
        st.write(f"**Email**: {profile.get('email', 'N/A')}")
        st.write(f"**Phone Number**: {profile.get('phoneNum', 'N/A')}")
        st.write(f"**Major**: {profile.get('major', 'N/A')}")
        st.write(f"**Admit Year**: {profile.get('admitYear', 'N/A')}")
        st.write(f"**Skills**: {profile.get('skills', 'N/A')}")
    else:
        st.error("Student profile not found.")

elif role == "employer":
    profile = requests.get(f"http://api:4000/emp/employers/{st.session_state['user id']}").json()
    if profile:
        st.subheader("Employer Profile")
        st.image(st.session_state['profile_pic'], width=150)
        st.write(f"**Name**: {profile.get('firstName', 'N/A')} {profile.get('lastName', 'N/A')}")
        st.write(f"**Email**: {profile.get('email', 'N/A')}")
        st.write(f"**Phone Number**: {profile.get('phoneNum', 'N/A')}")
        st.write(f"**Company Name**: {profile.get('companyName', 'N/A')}")
        st.write(f"**Industry**: {profile.get('industry', 'N/A')}")
        st.write(f"**Location**: {profile.get('location', 'N/A')}")
    else:
        st.error("Employer profile not found.")

elif role == "analyst":
    profile = requests.get(f"http://api:4000/analyst/analysts/{st.session_state['user id']}").json()
    if profile:
        st.subheader("Analyst Profile")
        st.image(st.session_state['profile_pic'], width=150)
        st.write(f"**Name**: {profile.get('firstName', 'N/A')} {profile.get('lastName', 'N/A')}")
        st.write(f"**Email**: {profile.get('email', 'N/A')}")
        st.write(f"**Phone Number**: {profile.get('phoneNum', 'N/A')}")
        st.write(f"**Role Description**: Responsible for analyzing and reporting platform data.")
        st.write(f"**Date Registered**: {profile.get('registrationDate', 'N/A')}")
    else:
        st.error("Analyst profile not found.")

# Admin Profile
elif role == "admin":
    profile = requests.get(f"http://api:4000/ad/admins/{st.session_state['user id']}").json()
    if profile:
        st.subheader("Admin Profile")
        st.image(st.session_state['profile_pic'], width=150)
        st.write(f"**Name**: {profile.get('firstName', 'N/A')} {profile.get('lastName', 'N/A')}")
        st.write(f"**Email**: {profile.get('email', 'N/A')}")
        st.write(f"**Phone Number**: {profile.get('phoneNum', 'N/A')}")
        st.write(f"**Role Description**: Platform administrator responsible for system maintenance and user management.")
        st.write(f"**Date Registered**: {profile.get('registrationDate', 'N/A')}")
    else:
        st.error("Admin profile not found.")

else:
    st.error("Invalid user role or user not found.")
