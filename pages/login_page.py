import streamlit as st
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from generate_keys import staff_names, usernames
import streamlit_authenticator as stauth
from pathlib import Path
import pickle
from employee import user_page
from stoppage import stoppage_page
from main import show_page_for_user

st.set_page_config(layout="wide", page_title="login")

# اعمال تنظیمات راست به چپ برای بدنه و فونت فارسی
st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    body {
        direction: rtl;
        font-family: 'Vazir', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# توابع برای صفحات مختلف


# Load hashed passwords
file_path = Path(__file__).parent / "../data/hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(staff_names, usernames, hashed_passwords,
                                    "sakht_dash", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("ورود", "main")

if authentication_status == False:
    st.error("نام کاربری یا پسورد اشتباه است.")

if authentication_status == None:
    st.warning("لطفاً نام کاربری و رمز عبور را وارد کنید.")

if authentication_status:
    # If the session state has changed, reset it
    if 'username' not in st.session_state or st.session_state['username'] != username:
        st.session_state.clear()

    # Set the username in session state
    st.session_state['username'] = username
    # Add rerun to refresh the page

    # Navigate based on the username
    show_page_for_user(username,authenticator)
