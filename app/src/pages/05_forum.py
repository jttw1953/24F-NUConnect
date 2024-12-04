import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.menubar import SideBarLinks
SideBarLinks()

import requests

st.title("Forum Discussions")

# Create a new discussion
st.subheader("Create a New Discussion")
title = st.text_input("Title")
content = st.text_area("Content")
tags = st.text_input("Tags (comma-separated)")
if st.button("Post Discussion"):
    try:
        payload = {"createdBy": 1, "title": title, "content": content, "tags": tags}  # Replace 1 with dynamic student ID
        response = requests.post("http://api:4000/stu/ForumDiscussion", json=payload)
        if response.status_code == 201:
            st.success("Discussion posted successfully")
        else:
            st.error("Failed to post discussion")
    except Exception as e:
        st.error(f"An error occurred: {e}")


# Fetch discussions from the backend
st.subheader("Discussion Posts")

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

# Search forum discussions
st.subheader("Search Discussions")
tags = st.text_input("Enter tags to filter discussions (e.g., 'co-op', 'interview')")
if st.button("Search Discussions"):
    try:
        response = requests.get(f"http://api:4000/emp/forumdiscussion/tags/{tags}")
        if response.status_code == 200:
            discussions = response.json()
            for discussion in discussions:
                st.write(f"**{discussion['title']}**: {discussion['content']}")
        else:
            st.error("Unable to fetch forum discussions. Please try again later.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

