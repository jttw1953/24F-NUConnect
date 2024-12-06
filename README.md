# NUConnect (CS3200 Final Project)

Northeastern’s NUWorks is a platform used by Northeastern students in their co-op search, but something it lacks is a sense of community and connection with their employers and peers. 

What we aim to do is create a platform that allows current co-op searchers to connect with others during their search and get advice and guidance from students who have completed co-ops in the past. We hope to make students feel less alone during their search for a co-op. Additionally, it will allow employers to engage with students more actively during the search, guiding them in the right direction. 

With NUConnect, we introduce a new interactive data-driven career platform that allows students and employers to communicate with each other to further improve their job/employee search experience. 

## Features 

NUConnect allows to you log in through 4 different user archetypes: 

1. __Students:__ Students are able to submit and view discussion posts posted by both peers and employers. They are also able to view and apply to jobs, as well as see their applications and their statuses. 
2. __Employers:__ Like students, employers are able to submit and view discussion posts. They are able to post new jobs under their company name, as well as view applications to jobs they've posted. 
3. __Admin:__ Admins are also able to view and post discussions. They can also view, post, delete, and update maintenance logs, security logs, system logs, and content flags. 
4. __Analyst:__ Analysts can view all tables in the database related to user activity and see summaries and visualizations of the data. They can also view and post to the forum discussions. 

## Current Project Components

Currently, there are three major components which will each run in their own Docker Containers:

- Streamlit App in the `./app` directory
- Flask REST api in the `./api` directory
- SQL files for your data model and data base in the `./database-files` directory


## Controlling the Containers

- `docker compose up -d` to start all the containers in the background
- `docker compose down` to shutdown and delete the containers

You can access the application at http://localhost:8501