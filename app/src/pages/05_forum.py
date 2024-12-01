import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.menubar import SideBarLinks
SideBarLinks()

import requests

st.title("Forum Discussions")

# Fetch discussions from the backend
results = requests.get('http://api:4000/ad/forumdiscussions').json()

if results:
    for discussion in results:
        discussion_id = discussion.get('discussionID', 'N/A')
        title = discussion.get('title', 'No Title')
        content = discussion.get('content', 'No Content Available')
        tags = discussion.get('tags', 'No Tags')
        created_at = discussion.get('createdAt', 'Unknown Date')
        created_by = discussion.get('createdBy', 'Anonymous')
        comment_count = discussion.get('commentCount', 0)

        # Discussion Block
        with st.container():
            st.subheader(title)
            st.write(f"**Content:** {content}")
            st.write(f"**Tags:** {tags}")
            st.write(f"**Posted By:** {created_by} on {created_at}")
            st.write(f"**Comments:** {comment_count} {'comment' if comment_count == 1 else 'comments'}")
            st.markdown("---") 
else:
    st.write("No discussions available.")
