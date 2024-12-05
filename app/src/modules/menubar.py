import streamlit as st

# Common menus
def Logout():
    st.sidebar.page_link("Home.py", label="Logout", icon="↩")

def UserProf():
    st.sidebar.page_link("pages/00_profile.py", label="Profile", icon="🫵🏼")

def ForumMenu(): 
    st.sidebar.page_link("pages/01_forum.py", label="Discussion", icon="📰")

# Student-specific menus
def ApplicationApply():
    st.sidebar.page_link("pages/02_appApply.py", label="Application Apply", icon="📝")

def ApplicationStatus():
    st.sidebar.page_link("pages/03_appStatus.py", label="Application Status", icon="📄")

# Employer-specific menus
def PostJobMenu():
    st.sidebar.page_link("pages/21_postJob.py", label="Post Job", icon="📋")

def FindEmployeeMenu():
    st.sidebar.page_link("pages/22_findStudent.py", label="Find Students", icon="🔍")

# Analyst-specific menus
def SummaryMenu():
    st.sidebar.page_link("pages/41_summary.py", label="Summary", icon="📊")

def DataMenu():
    st.sidebar.page_link("pages/42_data.py", label="Data", icon="📈")

def VisualizeMenu():
    st.sidebar.page_link("pages/43_visualize.py", label="Visualize", icon="🖼️")

# Admin-specific menus
def LogMenu():
    st.sidebar.page_link("pages/31_log.py", label="Logs", icon="📜")

def MaintenanceMenu():
    st.sidebar.page_link("pages/32_maintenance.py", label="Maintenance", icon="🛠️")

def SystemAlertMenu():
    st.sidebar.page_link("pages/33_systemAlert.py", label="System Alerts", icon="🚨")

def MetricMenu():
    st.sidebar.page_link("pages/35_metric.py", label="Metrics", icon="📊")

def FlagMenu():
    st.sidebar.page_link("pages/34_flag.py", label="Flags", icon="🚩")


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
