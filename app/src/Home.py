# ##################################################
# # This is the main/entry-point file for the 
# # sample application for your project
# ##################################################

# # Set up basic logging infrastructure
# import logging
# logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
# logger = logging.getLogger(__name__)

# # import the main streamlit library as well
# # as SideBarLinks function from src/modules folder
# import streamlit as st
# from modules.nav import SideBarLinks

# # streamlit supports reguarl and wide layout (how the controls
# # are organized/displayed on the screen).
# st.set_page_config(layout = 'wide')

# # If a user is at this page, we assume they are not 
# # authenticated.  So we change the 'authenticated' value
# # in the streamlit session_state to false. 
# st.session_state['authenticated'] = False

# # Use the SideBarLinks function from src/modules/nav.py to control
# # the links displayed on the left-side panel. 
# # IMPORTANT: ensure src/.streamlit/config.toml sets
# # showSidebarNavigation = false in the [client] section
# SideBarLinks(show_home=True)

# # ***************************************************
# #    The major content of this page
# # ***************************************************

# # set the title of the page and provide a simple prompt. 
# logger.info("Loading the Home page of the app")
# st.title('NUConnect')
# st.write('\n\n')
# st.write('### HI! As which user would you like to log in?')

# # For each of the user personas for which we are implementing
# # functionality, we put a button on the screen that the user 
# # can click to MIMIC logging in as that mock user. 

# if st.button("Act as John, a Political Strategy Advisor", 
#             type = 'primary', 
#             use_container_width=True):
#     # when user clicks the button, they are now considered authenticated
#     st.session_state['authenticated'] = True
#     # we set the role of the current user
#     st.session_state['role'] = 'pol_strat_advisor'
#     # we add the first name of the user (so it can be displayed on 
#     # subsequent pages). 
#     st.session_state['first_name'] = 'John'
#     # finally, we ask streamlit to switch to another page, in this case, the 
#     # landing page for this particular user type
#     logger.info("Logging in as Political Strategy Advisor Persona")
#     st.switch_page('pages/00_Pol_Strat_Home.py')

# if st.button('Act as Mohammad, an USAID worker', 
#             type = 'primary', 
#             use_container_width=True):
#     st.session_state['authenticated'] = True
#     st.session_state['role'] = 'usaid_worker'
#     st.session_state['first_name'] = 'Mohammad'
#     st.switch_page('pages/10_USAID_Worker_Home.py')

# if st.button('Act as System Administrator', 
#             type = 'primary', 
#             use_container_width=True):
#     st.session_state['authenticated'] = True
#     st.session_state['role'] = 'administrator'
#     st.session_state['first_name'] = 'SysAdmin'
#     st.switch_page('pages/20_Admin_Home.py')


import logging
import streamlit as st

# Logging setup
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Streamlit page configuration
st.set_page_config(layout='wide')
st.session_state['authenticated'] = False

logger.info("Loading the Home page of the app")

# Layout: Center column
col1, col2, col3, col4, col5, col6= st.columns([1, 1, 2, 2, 1, 1]) 

with col3: 
    st.write('\n\n')
    st.write('\n\n')
    st.write("###  Welcome To")
    st.write("# NUCONNECT")
    st.image("assets/logo.png", width=100)

with col4:
    # Header
    st.write('\n\n')
    st.write('\n\n')
    st.markdown("<div style='text-align: center;'> LOGIN</div>", unsafe_allow_html=True)

    st.write('\n\n')
    st.write('\n\n')

    if st.button('Student Login', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'student'
        st.session_state['user id'] = 1
        st.session_state['first_name'] = 'Lebron'
        st.session_state['profile_pic'] = "assets/student_p1.jpg"
        st.switch_page('pages/00_student_home.py')

    if st.button('# Employer Login', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'employer'
        st.session_state['user id'] = 81
        st.session_state['first_name'] = 'Sarah'
        st.session_state['profile_pic'] = "assets/student_p1.jpg"
        st.switch_page('pages/01_employer_home.py')

    if st.button('# Admin Login', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'admin'
        st.session_state['user id'] = 43
        st.session_state['first_name'] = 'Bob'
        st.session_state['profile_pic'] = "assets/student_p1.jpg"
        st.switch_page('pages/02_admin_home.py')

    if st.button('# Data Analyst', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'analyst'
        st.session_state['user id'] = 121
        st.session_state['first_name'] = 'Lisa'
        st.session_state['profile_pic'] = "assets/student_p1.jpg"
        st.switch_page('pages/03_analyst_home.py')
