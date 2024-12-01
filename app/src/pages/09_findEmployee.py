import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.menubar import SideBarLinks
SideBarLinks()

st.title("Find Students")

#test table
results = requests.get('http://api:4000/c/customers').json()
st.dataframe(results)
  