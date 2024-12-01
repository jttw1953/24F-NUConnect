import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.menubar import SideBarLinks
SideBarLinks()

# Page title
st.title("Security Logs")

try:
  data = requests.get('http://api:4000/ad/securityLogs').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)
