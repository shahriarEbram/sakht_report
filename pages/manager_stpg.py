def manager_page_stoppage(username):
    from cons import stoppage_list, categories
    from Database import fetch_stoppages  # Use functions for stoppage
    import streamlit as st
    import cons

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

    # Fetch stoppage data from the database
    stoppges_manager = fetch_stoppages(username)
    # df_manager = df_manager.drop(columns=['id'])
    # Show the data editor with the fetched stoppage data
    machines = []
    for category in categories.values():
        for machine in category:
            machines.append(machine)
    edited_df_manager = st.data_editor(
        stoppges_manager,
        hide_index=True,
        use_container_width=True,
        disabled=["stoppage_approve", "stpg_id", "person_name", "date", "stoppage_duration", "stpg_description"],
        column_order=["person_name", "machine", "reason", "date", "stoppage_duration", "stpg_description"],
        column_config={
            "machine": st.column_config.SelectboxColumn(
                options=machines,
                required=True,
            ),
            "reason": st.column_config.SelectboxColumn(
                options=stoppage_list,
                required=True,
            ),
            "task_approve": st.column_config.CheckboxColumn(

            ),
        }
    )

    # Add a button to save changes
    if st.button("ذخیره تغییرات", key="manager_stoppage_sub"):
        if not edited_df_manager.equals(stoppges_manager):
            try:
                # Update the stoppage data in the database
                # update_all_stoppage(edited_df_manager)
                st.success("تغییرات با موفقیت اعمال شد.")
            except Exception as e:
                st.error(f"خطای: {e}")
        else:
            st.warning("تغییری اعمال نشد.")
