def show_page_for_user(username, auth):
    import streamlit as st
    from pages.employee import user_page
    from pages.manager_tsk import manager_page_tasks
    from pages.manager_stpg import manager_page_stoppage
    from pages.stoppage import stoppage_page
    from forman_tsk import forman_page_tasks
    from cons import workers, foremen, managers, user_pass


    #staff = employee_names.get(username)
    staff = user_pass.get(username)[0]
    with st.expander(f"{staff} خوش آمدید!"):
        auth.logout("خروج از حساب کاربری", "main")

    # Operators
    if username in foremen:
        tab1, tab2, tab3 = st.tabs(["کارکرد", "توقفات", "گزارش کارکنان"])
        with tab1:
            user_page(username, auth)
        with tab2:
            stoppage_page(username)
        with tab3:
            forman_page_tasks(username)


    # Workers
    elif username in workers:
        user_page(username, auth)

    # Manager
    elif username in managers:
        tab1, tab2 = st.tabs(["گزارش کارکنان", "گزارش توقفات",])
        with tab1:
            manager_page_tasks(username)
        with tab2:
            manager_page_stoppage(username)


