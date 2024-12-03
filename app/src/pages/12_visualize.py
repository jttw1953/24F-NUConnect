import logging
logger = logging.getLogger(__name__)
import requests 
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import streamlit as st
from modules.menubar import SideBarLinks

st.set_page_config(layout = 'wide')
SideBarLinks()

st.title("Visualization")

tables = ["Select", "Forum Discussions", "Comments", "Applications", "Jobs"]
forum = pd.DataFrame(requests.get('http://api:4000/analyst/ForumDiscussion').json())

students = pd.DataFrame(requests.get('http://api:4000/analyst/Students').json())
employers = pd.DataFrame(requests.get('http://api:4000/analyst/Employers').json())
comments = pd.DataFrame(requests.get('http://api:4000/analyst/Comments').json())
apps = pd.DataFrame(requests.get('http://api:4000/analyst/Apps').json())
jobs= pd.DataFrame(requests.get('http://api:4000/analyst/Jobs').json())



selected_table = st.selectbox("Select a table to display visualizations:", list(tables))
if selected_table == "Select":
    col1, col2 = st.columns(2)
    with col1:
        st.write("No Table Selected")

if selected_table == 'Forum Discussions':
    st.write("Forum Discussions")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Discussions", forum.shape[0])

    with col2:
        st.write("Top Contributors")
        writers = list(forum['createdBy'])

        counts = Counter(writers) # O(n)
        largest = max(counts.values()) # O(n)
        largest_with_ties = [k for k, v in counts.items() if v == largest] # O(n)
        result = sorted(largest_with_ties)

        labels = result[0:5]
        sizes = [writers.count(x) for x in labels]
        labels = ["User ID " + str(res) + "" for res in labels]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)
if selected_table == 'Comments':
    st.write("Comments")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Comments", comments.shape[0])

    with col2:
        st.write("Top Contributors")
        writers = list(comments['createdBy'])

        counts = Counter(writers) # O(n)
        largest = max(counts.values()) # O(n)
        largest_with_ties = [k for k, v in counts.items() if v == largest] # O(n)
        result = sorted(largest_with_ties)

        labels = result[0:5]
        sizes = [writers.count(x) for x in labels]
        labels = ["User ID " + str(res) + "" for res in labels]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)
if selected_table == 'Applications':
    st.write("Applications")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Applications", apps.shape[0])

    with col2:
        st.write("Job Statuses")
        writers = list(apps['status'])

        counts = Counter(writers) # O(n)
        largest = max(counts.values()) # O(n)
        largest_with_ties = [k for k, v in counts.items()] # O(n)
        result = sorted(largest_with_ties)
        labels = result
        sizes = [writers.count(x) for x in labels]
        labels = ["Job ID " + str(res) + "" for res in labels]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)
if selected_table == 'Jobs':
    st.write("Jobs")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Jobs", jobs.shape[0])

    with col2:
        st.write("Job Industries")
        industry = jobs.merge(employers, on='companyID')
        writers = list(industry['industry'])

        counts = Counter(writers) # O(n)
        largest = max(counts.values()) # O(n)
        largest_with_ties = [k for k, v in counts.items()] # O(n)
        result = sorted(largest_with_ties)
        labels = result
        sizes = [writers.count(x) for x in labels]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)

