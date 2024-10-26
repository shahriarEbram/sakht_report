def forman_page_tasks(username):
    from cons import work_shift, unit_name, categories, managers
    from Database import fetch_tasks, update_tasks  # Use functions for stoppage
    import streamlit as st

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
    if "forman_df" not in st.session_state:
        st.session_state.forman_df = fetch_tasks(username, True)

    # Show the data editor with the fetched stoppage data
    edited_df_forman = st.data_editor(
        st.session_state.forman_df,
        hide_index=True,
        use_container_width=True,
        column_order=["person_name", "unit", "shift", "operation", "machine",
                  "product", "work_type", "project_code", "date",
                  "operation_duration", "announced_duration", "done_duration" ,"task_description"],
        disabled=["person_name", "unit", "shift", "operation", "machine",
                  "product", "work_type", "project_code", "date",
                  "operation_duration", "announced_duration", "done_duration" ]
    )
