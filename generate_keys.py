import pickle
from pathlib import Path

import streamlit_authenticator as stauth
staff_names = [
    "محمدرضا مرادی", "رحمت ایمانی پور", "حمید خانی", "محمد محمدی", "وحید طالقانی", "رسول محمدخانی",
    "ابراهیم کریمی", "بهزاد مهدی زاده", "فرشاد بیگلری", "بیت الله امامی", "جواد کلهر", "رسول نصیری",
    "محسن آریایی", "رضا قاسمی", "علی زمانی", "محمد رحمانی", "حسن حیدری", "رضا رشوند", "رضا حسینی",
    "فرهاد هاشم خانی", "داریوش درخشانی", "حمید قربانی", "رحیم محمدخانی", "جواد مقدادی", "حسن احمدی",
    "داود حیدری", "مهدی داوودی", "جواد حسین علیزاده", "شهریار ابرام پور", "پرستو دمرچی", "علی سهرابی"
]

usernames = [
    "moradi", "rahmat_imanipour", "hamid_khani", "mohammad_mohammadi", "vahid_taleghani",
    "rasool_mohammadkhani", "ebrahim_karimi", "behzad_mehdizadeh", "farshad_biglari", "beytolah_emami", "javad_kalhor",
    "rasool_nasiri", "mohsen_ariayi", "reza_ghasemi", "ali_zamani", "mohammad_rahmani", "hasan_heydari",
    "reza_rashvand", "reza_hosseini", "farhad_hashemkhani", "dariush_derakhshani","hamid_ghorbani", "rahim_mohammadkhani",
    "javad_meghdadi", "hasan_ahmadi", "davood_heydari", "mehdi_davoodi", "javad_hosseinalizadeh", "ebrampour",
    "damerchi", "sohrabi"
]

passwords = ["123"] * len(staff_names)  # All passwords set to "123" for simplicity

user_pass = {
    "moradi": ["محمدرضا مرادی", "123"],
    "rahmat_imanipour": ["رحمت ایمانی پور", "123"],
    "hamid_khani": ["حمید خانی", "123"],
    "mohammad_mohammadi": ["محمد محمدی", "123"],
    "vahid_taleghani": ["وحید طالقانی", "123"],
    "rasool_mohammadkhani": ["رسول محمدخانی", "123"],
    "ebrahim_karimi": ["ابراهیم کریمی", "123"],
    "behzad_mehdizadeh": ["بهزاد مهدی زاده", "123"],
    "farshad_biglari": ["فرشاد بیگلری", "123"],
    "beytolah_emami": ["بیت الله امامی", "123"],
    "javad_kalhor": ["جواد کلهر", "123"],
    "rasool_nasiri": ["رسول نصیری", "123"],
    "mohsen_ariayi": ["محسن آریایی", "123"],
    "reza_ghasemi": ["رضا قاسمی", "123"],
    "ali_zamani": ["علی زمانی", "123"],
    "mohammad_rahmani": ["محمد رحمانی", "123"],
    "hasan_heydari": ["حسن حیدری", "123"],
    "reza_rashvand": ["رضا رشوند", "123"],
    "reza_hosseini": ["رضا حسینی", "123"],
    "farhad_hashemkhani": ["فرهاد هاشم خانی", "123"],
    "dariush_derakhshani": ["داریوش درخشانی", "123"],
    "hamid_ghorbani": ["حمید قربانی", "123"],
    "rahim_mohammadkhani": ["رحیم محمدخانی", "123"],
    "javad_meghdadi": ["جواد مقدادی", "123"],
    "hasan_ahmadi": ["حسن احمدی", "123"],
    "davood_heydari": ["داود حیدری", "123"],
    "mehdi_davoodi": ["مهدی داوودی", "123"],
    "javad_hosseinalizadeh": ["جواد حسین علیزاده", "123"],
    "ebrampour": ["شهریار ابرام پور", "123"],
    "damerchi": ["پرستو دمرچی", "123"],
    "sohrabi": ["علی سهرابی", "123"]
}


hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path("data/hashed_pw.pkl")
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
