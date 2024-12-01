import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.menubar import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title("Welcome " +  st.session_state['first_name'] + "!")