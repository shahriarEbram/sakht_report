def manager_page_tasks(username):
    from cons import work_shift, unit_name, categories, managers, months
    from Database import fetch_tasks, update_tasks, fetch_stoppages_by_month  # Use functions for stoppage
    import streamlit as st
    from code_validator import product_name
    from Database import fetch_tasks_by_month
    import pandas as pd
    from io import BytesIO
    if username in managers:
        task_approve_column = st.column_config.CheckboxColumn(
            required=True
        )
    else:
        task_approve_column = None
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
    machines = []
    for category in categories.values():
        for machine in category:
            machines.append(machine)
    # Fetch Task data from the database
    if "manager_df" not in st.session_state:
        st.session_state.manager_df = fetch_tasks(username)

    # Show the data editor with the fetched stoppage data
    edited_df_manager = st.data_editor(
        st.session_state.manager_df,
        hide_index=True,
        use_container_width=True,
        disabled=["person_name"],
        column_order=["task_approve","person_name", "unit", "shift", "operation", "machine",
                      "product", "work_type", "project_code", "date",
                      "operation_duration", "announced_duration", "done_duration", "task_description"
                      ],
        column_config={
            "unit": st.column_config.SelectboxColumn(
                options=unit_name,
                required=True,
            ),
            "shift": st.column_config.SelectboxColumn(
                options=work_shift,
                required=True,
            ),
            "operation": st.column_config.SelectboxColumn(
                options=list(categories.keys()),
                required=True,
            ),
            "machine": st.column_config.SelectboxColumn(
                options=machines,
                required=True,
            ),
            "product": st.column_config.SelectboxColumn(
                options=list(product_name.values()),
                required=True,
            ),
            "task_approve": task_approve_column,
        }
    )
    st.session_state.edited_df = edited_df_manager
    # Add a button to save changes
    if st.button("ذخیره تغییرات", key="manager_tasks_sub"):
        if st.session_state.edited_df is not None:
            if not edited_df_manager.equals(st.session_state.manager_df):
                try:
                    # Update the stoppage data in the database
                    update_tasks(st.session_state.edited_df, st.session_state.manager_df)
                    # Update the session state
                    st.session_state.manager_df = edited_df_manager
                    st.success("تغییرات با موفقیت اعمال شد.")
                except Exception as e:
                    st.error(f"خطای: {e}")
            else:
                st.warning("تغییری اعمال نشد.")

    # total_report =fetch_tasks(username)
    # with st.expander(f"گزارشات تایید شده"):
    #     st.dataframe(total_report,hide_index =True)

    with st.container(border=True):
        st.header("دانلود گزارش کارکرد واحد ساخت")
        col1, col2 = st.columns(2)
        with col1:
            month = st.selectbox(" ",
                                 options=months.values(),
                                 index=0,
                                 placeholder="ماه مورد نظر را انتخاب کنید:",
                                 key="month_select")
            month_zip = dict(zip(months.values(), months.keys()))
            month_number = month_zip[str(month)]
            df_temp_task = fetch_tasks_by_month(month_number)
            df_temp_stpgs = fetch_stoppages_by_month(month_number)
            # تبدیل DataFrame به فرمت Excel
            if not df_temp_task.empty:
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_temp_task.to_excel(writer, index=False, sheet_name=f"{month} کارکرد ")
                    df_temp_stpgs.to_excel(writer, index=False, sheet_name=f'{month} توقفات ')
                output.seek(0)  # بازگشت به ابتدای بافر

                st.download_button("دانلود گزارش کارکرد",
                                   file_name=f"گزارش کاکرد واحد ساخت - {month}.xlsx",
                                   data=output.getvalue(),
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.warning("هیچ داده‌ای برای دانلود وجود ندارد.")
