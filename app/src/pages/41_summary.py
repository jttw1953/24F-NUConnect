import logging
logger = logging.getLogger(__name__)
import requests
import pandas as pd 
import matplotlib.pyplot as plt

import streamlit as st
from modules.menubar import SideBarLinks
SideBarLinks()
st.title("Summaries")

results = requests.get('http://api:4000/analyst/DailySummary').json()
df = pd.DataFrame(results)

if results:
    apps_sent = df['apps_sent']
    jobs_posted = df['jobs_posted']
    new_discussions = df['new_discussions']
    new_comments = df['new_comments']

    st.subheader("Daily Summary Stats")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Applications Sent", apps_sent)
        st.metric("Jobs Posted", jobs_posted)

    with col2:
        st.metric("New Discussions", new_discussions)
        st.metric("New Comments", new_comments)


activity = requests.get('http://api:4000/analyst/ActivityLog').json()
# Prepare the data for the bar chart
act_df = pd.DataFrame(activity)
types = {'login': act_df[act_df['activityType'] == 'login'].shape[0], 
         'logout': act_df[act_df['activityType'] == 'logout'].shape[0], 
         'delete': act_df[act_df['activityType'] == 'delete'].shape[0], 
         'update': act_df[act_df['activityType'] == 'update'].shape[0]}
activity_df = pd.DataFrame(list(types.items()), columns=["Activity Type", "Count"])


# Display the bar chart
st.subheader("All Activity")
st.bar_chart(activity_df.set_index('Activity Type')['Count'])