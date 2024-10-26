def user_page(username, authenticator):
    from cons import work_shift, unit_name, work_type, categories, user_pass
    from Database import update_tasks, insert_task
    from code_validator import product_name
    import pandas as pd
    from Database import fetch_tasks
    import streamlit as st
    import cons
    import jdatetime
    from datetime import datetime
    toady_milady = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    # staff = cons.employee_names.get(username)
    staff = user_pass.get(username)[0]

    def miladi_to_shamsi(date):
        return jdatetime.date.fromgregorian(date=date)

    today_shamsi = miladi_to_shamsi(jdatetime.datetime.now().togregorian())

    # with st.expander(f"{staff} خوش آمدید!"):
    #     authenticator.logout("خروج از حساب کاربری", "main")

    df_key = f"df_task_{username}"
    # *** Dataframe Setting *** #
    if df_key not in st.session_state:
        # Fetch data from the database
        df = fetch_tasks(username)

        if df.empty:
            df = pd.DataFrame(columns=[
                'id',
                'person_name',
                'unit',
                'shift',
                'operation',
                'machine',
                'product',
                'work_type',
                'project_code',
                'date',
                'operation_duration',
                'announced_duration',
                'done_duration',
                'task_date',
                'task_description',
            ])

        # df['task_name'] = df['task_name'].astype(pd.CategoricalDtype(cons.task_name.values()))
        st.session_state[df_key] = df
    # ساخت فرم
    with st.container(border=True):

        # ردیف اول: اسم واحد و شیفت
        col1, col2 = st.columns(2)
        with col1:
            unit = st.selectbox("نام واحد درخواست دهنده",
                                options=unit_name,
                                index=None,
                                placeholder="واحد را انتخاب کنید:",
                                key="unit_select")
        with col2:
            shift = st.selectbox("شیفت",
                                 options=work_shift,
                                 index=None,
                                 placeholder="شیفت را انتخاب کنید:",
                                 key="shift_select")

        # ردیف دوم: نوع کار و اسم محصول
        col3, col4 = st.columns(2)
        with col3:
            selected_category = st.selectbox("عملیات",
                                             index=None,
                                             placeholder="عملیات مورد نظر را انتخاب کنید:",
                                             options=list(categories.keys()))
        with col4:
            if selected_category:
                selected_item = st.selectbox("ماشین",
                                             options=categories[selected_category])
            else:
                selected_item = st.selectbox("ماشین",
                                             options=[""])

        # ردیف سوم: اسم دستگاه و نوع کار
        col5, col6 = st.columns(2)
        with col5:
            product_name_input = st.selectbox("اسم محصول",
                                              index=None,
                                              options=product_name.values(),
                                              placeholder="نام محصول را انتخاب کنید:")
        with col6:
            work_type_input = st.selectbox("نوع کار",
                                           index=None,
                                           options=work_type,
                                           placeholder="نوع کار انتخاب کنید:")

        # کد پروژه
        col13, col14 = st.columns(2)
        with col13:
            pcode = st.text_input("کد پروژه:",
                                  max_chars=9,
                                  key=0,
                                  disabled=False)
        with col14:
            task_description = st.text_area('توضیحات',
                                            max_chars=100,
                                            height=25)

        # انتخاب تاریخ انجام کار
        with st.container(border=True):
            st.write("تاریخ انجام کار")
            col7, col8, col9 = st.columns(3)
            with col7:
                day = st.number_input('روز', min_value=1, max_value=31, value=today_shamsi.day)
                day = f'{int(day):02}'
            with col8:
                month = st.number_input('ماه', min_value=1, max_value=12, value=today_shamsi.month, disabled=False)
                month = f'{int(month):02}'
            with col9:
                year = st.number_input('سال', min_value=1300, max_value=1500, value=today_shamsi.year, disabled=True)
            # task_date = jdatetime.date(year, month, day)
            # تبدیل تاریخ شمسی به رشته با فرمت 1403-6-31
            task_date = f"{year}-{month}-{day}"

        # مدت زمان‌ها
        col10, col11, col12 = st.columns(3)
        with col10:
            st.write("مدت زمان کارکرد")
            operation_dur_hour = st.number_input('ساعت', min_value=0, max_value=24, key="op_du_h")
            operation_dur_minute = st.number_input('دقیقه', min_value=1, max_value=60, key="op_du_m")
        with col11:
            st.write("مدت زمان اعلام شده")
            announced_dur_hour = st.number_input('ساعت', min_value=0, max_value=500, key="an_du_h")
            announced_dur_minute = st.number_input('دقیقه', min_value=0, max_value=60, key="an_du_m")
        with col12:
            st.write("مدت زمان انجام شده")
            done_dur_hour = st.number_input('ساعت', min_value=0, max_value=500, key="do_du_h")
            done_dur_minute = st.number_input('دقیقه', min_value=0, max_value=60, key="do_du_m")

        # فرمت کردن زمان‌ها به صورت HH:MM
        operation_duration = f"{operation_dur_hour:02d}:{operation_dur_minute:02d}"
        announced_duration = f"{announced_dur_hour:02d}:{announced_dur_minute:02d}"
        done_duration = f"{done_dur_hour:02d}:{done_dur_minute:02d}"
        # دکمه ثبت فرم
        submitted_task = st.button("ثبت", key="task_submit_button")

    if submitted_task:
        new_task = {
            "person_name": staff,
            "unit": unit,
            "shift": shift,
            "operation": selected_category,
            "machine": selected_item,
            "product": product_name_input,
            "work_type": work_type_input,
            "project_code": pcode,
            "date": task_date,
            "operation_duration": operation_duration,
            "announced_duration": announced_duration,
            "done_duration": done_duration,
            "task_date": toady_milady,
            "task_description":task_description
        }
        if not unit:
            st.warning("نام واحد را انتخاب کنید.")
        elif not shift:
            st.warning("شیفت را انتخاب کنید.")
        elif not selected_category:
            st.warning("عملیات را انتخاب کنید.")
        elif not work_type_input:
            st.warning("نوع کار را انتخاب کنید.")
        else:
            insert_task(new_task)
            # Update session state
            st.session_state[df_key] = fetch_tasks(username)
            st.success("کارکرد اضافه شد.")

    task_df = st.data_editor(st.session_state[df_key],
                             disabled=['id', 'person_name', 'unit', 'shift', 'operation',
                                       'machine', 'product', 'work_type', 'project_code',
                                       'date', 'operation_duration', 'announced_duration', 'done_duration',"task_description"],
                             column_order=["person_name", "unit", "shift", "operation", "machine",
                                           "product", "work_type", "project_code", "date",
                                           "operation_duration", "task_description", "announced_duration",
                                           "done_duration"
                                           ],
                             key="task_df",
                             use_container_width=True,
                             num_rows="dynamic",
                             hide_index=True,
                             )

    # فیلتر کردن سطرهای خالی اضافه شده
    task_filtered_df = task_df.dropna(how='all')

    # ذخیره تغییرات در دیتابیس
    if task_df is not None:
        update_tasks(task_filtered_df, st.session_state[df_key])  # دیتافریم اصلی را در session state ویرایش کنید
        st.session_state[df_key] = task_filtered_df  # به‌روزرسانی session state با داده‌های جدید
