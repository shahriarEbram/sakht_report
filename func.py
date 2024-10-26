from Database import insert_user

from datetime import datetime

toady_milady = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
new_row = {
    "date": toady_milady,
    "person_name": "احمد",
    "username": "ahmad",
        "password": "123546",
}
# insert_user(new_row)
