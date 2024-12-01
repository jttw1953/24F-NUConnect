import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.menubar import SideBarLinks
SideBarLinks()

col1, col2= st.columns([10, 1])  # Adjust column widths as needed

with col2:
    st.image("assets/student_p1.jpg", width=100)
    if st.button("Edit", use_container_width=True):
        st.switch_page("Home.py")  