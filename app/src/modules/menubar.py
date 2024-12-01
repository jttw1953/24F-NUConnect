import streamlit as st

# Common menus
def Logout():
    st.sidebar.page_link("Home.py", label="Logout", icon="↩")

def UserProf():
    st.sidebar.page_link("pages/04_profile.py", label="Profile", icon="🫵🏼")

def ForumMenu(): 
    st.sidebar.page_link("pages/05_forum.py", label="Discussion", icon="📰")

# Student-specific menus
def ApplicationApply():
    st.sidebar.page_link("pages/06_appApply.py", label="Application Apply", icon="📝")

def ApplicationStatus():
    st.sidebar.page_link("pages/07_appStatus.py", label="Application Status", icon="📄")

# Employer-specific menus
def PostJobMenu():
    st.sidebar.page_link("pages/08_postJob.py", label="Post Job", icon="📋")

def FindEmployeeMenu():
    st.sidebar.page_link("pages/09_findStudent.py", label="Find Students", icon="🔍")

# Analyst-specific menus
def SummaryMenu():
    st.sidebar.page_link("pages/10_summary.py", label="Summary", icon="📊")

def DataMenu():
    st.sidebar.page_link("pages/11_data.py", label="Data", icon="📈")

def VisualizeMenu():
    st.sidebar.page_link("pages/12_visualize.py", label="Visualize", icon="🖼️")

# Admin-specific menus
def LogMenu():
    st.sidebar.page_link("pages/13_log.py", label="Logs", icon="📜")

def MaintenanceMenu():
    st.sidebar.page_link("pages/14_maintenance.py", label="Maintenance", icon="🛠️")

def SystemAlertMenu():
    st.sidebar.page_link("pages/15_systemAlert.py", label="System Alerts", icon="🚨")

def MetricMenu():
    st.sidebar.page_link("pages/17_metric.py", label="Metrics", icon="📊")

def FlagMenu():
    st.sidebar.page_link("pages/16_flag.py", label="Flags", icon="🚩")


def SideBarLinks():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if st.session_state["authenticated"]:
        st.sidebar.title("NUCONNECT")
        st.sidebar.markdown("<br>", unsafe_allow_html=True)

        if 'profile_pic' in st.session_state:
            st.sidebar.image(st.session_state['profile_pic'], width=100)
            
        if 'first_name' in st.session_state:
            st.sidebar.text(st.session_state['first_name'])
        

        if st.session_state["role"] == "student":
            UserProf()
        elif st.session_state["role"] == "employer":
            UserProf()

        ForumMenu()

        if st.session_state["role"] == "student":
            ApplicationApply()
            ApplicationStatus()
        
        elif st.session_state["role"] == "employer":
            ApplicationStatus()  
            PostJobMenu()
            FindEmployeeMenu()
        
        elif st.session_state["role"] == "analyst":
            SummaryMenu()
            DataMenu()
            VisualizeMenu()
        
        elif st.session_state["role"] == "admin":
            LogMenu()
            MaintenanceMenu()
            SystemAlertMenu()
            MetricMenu()
            FlagMenu()

        Logout()
