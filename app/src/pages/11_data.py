import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.menubar import SideBarLinks
SideBarLinks()

st.title("Viewing Data")
tables = ["Forum Discussions", "Employers", "Students", "Comments", "Applications", "Jobs"]


selected_table = st.selectbox("Select a table to display:", list(tables))
if selected_table == 'Forum Discussions':
    results = requests.get('http://api:4000/analyst/ForumDiscussion').json()
if selected_table == 'Employers':
    results = requests.get('http://api:4000/analyst/Employers').json()
if selected_table == 'Students':
    results = requests.get('http://api:4000/analyst/Students').json()
if selected_table == 'Comments':
    results = requests.get('http://api:4000/analyst/Comments').json()
if selected_table == 'Applications':
    results = requests.get('http://api:4000/analyst/Apps').json()
if selected_table == 'Jobs':
    results = requests.get('http://api:4000/analyst/Jobs').json()

st.dataframe(results, use_container_width=True)

