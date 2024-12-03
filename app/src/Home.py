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
        st.session_state['profile_pic'] = "assets/employer_p1.jpg"
        st.switch_page('pages/01_employer_home.py')

    if st.button('# Admin Login', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'admin'
        st.session_state['user id'] = 43
        st.session_state['first_name'] = 'Bob'
        st.session_state['profile_pic'] = "assets/admin_p1.png"
        st.switch_page('pages/02_admin_home.py')

    if st.button('# Data Analyst', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'analyst'
        st.session_state['user id'] = 121
        st.session_state['first_name'] = 'Lisa'
        st.session_state['profile_pic'] = "assets/analyst_p1.jpg"
        st.switch_page('pages/03_analyst_home.py')
