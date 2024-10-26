def stoppage_page(username):
    import streamlit as st
    from cons import operator_machine_group, user_pass, stoppage_list, categories
    import jdatetime
    from Database import insert_stoppage, fetch_stoppages, update_stoppages
    import pandas as pd
    from datetime import datetime
    toady_milady = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    def miladi_to_shamsi(date):
        return jdatetime.date.fromgregorian(date=date)

    today_shamsi = miladi_to_shamsi(jdatetime.datetime.now().togregorian())

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

    # staff = employee_names.get(username)
    staff = user_pass.get(username)[0]
    if username in operator_machine_group:
        # Get all machines for the operator
        machine_groups_for_operator = operator_machine_group[username]
        machines = []
        # Combine all machines from different groups
        for group in machine_groups_for_operator:
            machines.extend(categories[group])
        df_key = f"df_stoppage_{username}"
        # *** Dataframe Setting *** #
        if df_key not in st.session_state:
            # Fetch data from the database

            df = fetch_stoppages(username)

            if df.empty:
                df = pd.DataFrame(columns=[
                    'stpg_id',
                    'person_name',
                    'machine',
                    'reason',
                    'date',
                    'stoppage_duration',
                    'stpg_date',
                    'stpg_description'
                ])

            # df['task_name'] = df['task_name'].astype(pd.CategoricalDtype(cons.task_name.values()))
            st.session_state[df_key] = df
        with st.form(key="stoppage_form", clear_on_submit=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                # Display all machines for the operator
                selected_machine = st.selectbox("دستگاه مورد نظر را انتخاب کنید:", machines)
            with col2:
                # Select stoppage type
                stoppage_reason = st.selectbox("علت توقف را وارد کنید:", stoppage_list)
            with col3:
                stpg_description = st.text_area('توضیحات',
                                                max_chars=100,
                                                height=25)

            with st.container(border=True):
                st.write("تاریخ توقف")
                col3, col4, col5 = st.columns(3)
                with col3:
                    day = st.number_input('روز', min_value=1, max_value=31, value=today_shamsi.day)
                    day = f'{int(day):02}'
                with col4:
                    month = st.number_input('ماه', min_value=1, max_value=12, value=today_shamsi.month, disabled=False)
                    month = f'{int(month):02}'
                with col5:
                    year = st.number_input('سال', min_value=1300, max_value=1500, value=today_shamsi.year,
                                           disabled=True)
                # تبدیل تاریخ شمسی به رشته با فرمت 1403-6-31
                task_date = f"{year}-{month}-{day}"

            st.write("مدت زمان توقف")
            stp_hour = st.number_input('ساعت', min_value=0, max_value=24, key="stop_du_h")
            stp_minute = st.number_input('دقیقه', min_value=1, max_value=60, key="stop_du_m")
            stp_duration = f"{stp_hour:02d}:{stp_minute:02d}"
            submitted_stoppage = st.form_submit_button("ثبت")

            # بررسی اینکه هیچ یک از فیلدها خالی نباشد
            if submitted_stoppage:
                new_stoppage = {
                    'person_name': staff,
                    'machine': selected_machine,
                    'reason': stoppage_reason,
                    'date': task_date,
                    'stoppage_duration': stp_duration,
                    'stpg_date': toady_milady,
                    'stpg_description': stpg_description
                }
                insert_stoppage(new_stoppage)
                # Update session state
                st.session_state[df_key] = fetch_stoppages(username)
                st.success("توقف اضافه شد.")

        stoppage_df = st.data_editor(st.session_state[df_key],
                                     disabled=['person_name',
                                               'machine',
                                               'reason',
                                               'date',
                                               'stoppage_duration',
                                               'stpg_description'],

                                     column_order=['person_name',
                                                   'machine',
                                                   'reason',
                                                   'date',
                                                   'stoppage_duration',
                                                   'stpg_description'],

                                     key="stoppage_df",
                                     use_container_width=True,
                                     num_rows="dynamic",
                                     hide_index=True,
                                     )

        # # فیلتر کردن سطرهای خالی اضافه شده
        stoppage_filtered_df = stoppage_df.dropna(how='all')

        # ذخیره تغییرات در دیتابیس
        if stoppage_df is not None:
            update_stoppages(stoppage_filtered_df,
                             st.session_state[df_key])  # دیتافریم اصلی را در session state ویرایش کنید
            st.session_state[df_key] = stoppage_filtered_df  # به‌روزرسانی session state با داده‌های جدید
