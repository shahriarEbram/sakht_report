import streamlit as st
from datetime import datetime
from Database import fetch_all_tasks, insert_user, update_user
import re

toady_milady = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
# Apply RTL and Persian font
st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    body {
        direction: rtl;
        font-family: 'Vazir', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# حالت ویرایش را از session_state دریافت یا مقداردهی اولیه کنید
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# دریافت اطلاعات کاربران
users_df = fetch_all_tasks()

with st.container(border=True):
    st.subheader('تغییر پسورد و نام کاربری')
    names_list = users_df['person_name'].tolist()
    user_selectbox = st.selectbox("شخص مورد نظر را انتخاب کنید:", names_list)

    # دریافت اطلاعات کاربر انتخاب‌شده
    selected_user = users_df[users_df['person_name'] == user_selectbox].iloc[0]

    # بررسی حالت ویرایش
    if st.session_state.edit_mode:
        username = st.text_input("نام کاربری", selected_user['username'])
        password = st.text_input("پسورد", selected_user['password'], type='password')
    else:
        username = st.text_input("نام کاربری", selected_user['username'], disabled=True)
        password = st.text_input("پسورد", selected_user['password'], type='password', disabled=True)

    if st.button("ویرایش" if not st.session_state.edit_mode else "تایید"):
        if st.session_state.edit_mode:
            errors = []

            # اعتبارسنجی نام کاربری: باید حتماً انگلیسی باشد و عدد نداشته باشد
            if not re.match(r'^[a-zA-Z]+$', username):
                errors.append("نام کاربری باید شامل حروف انگلیسی باشد و نباید عدد داشته باشد.")

            # اعتبارسنجی پسورد: باید فقط عدد باشد
            if not re.match(r'^\d+$', password):
                errors.append("پسورد باید فقط شامل عدد باشد.")

            # نمایش خطاها
            if errors:
                for error in errors:
                    st.warning(error)
            else:
                changed_information = {
                    "date": toady_milady,
                    "person_name": selected_user['person_name'],
                    "username": username,
                    "password": password,
                }
                print(changed_information)
                if update_user(selected_user['user_id'], changed_information):
                    st.success("تغییرات اعمال شد.")
                    # بازخوانی اطلاعات کاربران بعد از بروزرسانی
                    users_df = fetch_all_tasks()  # دریافت داده‌های جدید
                else:
                    st.warning("نام کاربری از قبل موجود است. لطفاً نام کاربری دیگری انتخاب کنید.")
                st.session_state.edit_mode = False
        else:
            st.session_state.edit_mode = True


# ADD NEW USERNAME AND PASSWORD
with st.container(border=True):
    st.subheader('اضافه کردن کاربر جدید')
    new_person_name = st.text_input("نام شخص", placeholder="فارسی؛ مانند شهریار ابرام پور")
    new_username = st.text_input("نام کاربری", placeholder="مانند ebrampour")
    new_password = st.text_input("پسورد", placeholder="مانند 123456")
    add_btn = st.button("اضافه کردن")

    if add_btn:
        errors = []

        if not re.match(r'^[\u0600-\u06FF\s]+$', new_person_name):
            errors.append("نام شخص باید شامل حروف فارسی باشد و شامل نباید عدد باشد.")

        if not re.match(r'^[a-zA-Z]+$', new_username):
            errors.append("نام کاربری باید شامل حروف انگلیسی باشد و نباید شامل عدد باشد.")

        if not re.match(r'^\d+$', new_password):
            errors.append("پسورد باید فقط شامل عدد باشد.")

        if new_person_name == "" or new_username == "" or new_password == "":
            errors.append("اطلاعات را بطور کامل تکمیل کنید!")

        if errors:
            for error in errors:
                st.warning(error)
        else:
            new_person = {"date": toady_milady,
                          "person_name": new_person_name,
                          "username": new_username,
                          "password": new_password}
            if insert_user(new_person):
                st.success(f"کاربر {new_person_name} با نام کاربری {new_username} با موفقیت  اضافه شد!")
            else:
                st.warning("نام کاربری از قبل موجود است. لطفاً نام کاربری دیگری انتخاب کنید.")
