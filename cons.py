unit_name = ["BT1", "BT2", "BT3", "BT4", "BT5", "BT6", "دفتر مرکز"]
work_shift = ["شیفت اول", "شیفت دوم"]

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
    "damerchi": ["خانم پرستو دمرچی", "123"],
    "sohrabi": ["علی سهرابی", "123"]
}

work_type = ["پروژه", "یدکی اصلاحی", "هفتگی", "متفرقه"]

categories = {
    "CNC": [
        "سنگ محور", "1000", "FIL", "720", "هرمله1", "هرمله2", "NEWAY"
    ],
    "برشکاری": [
        "هوابرش CNC", "اره نواري"
    ],
    "جوشکاری": [
        "ترانس جوش"
    ],
    "تراشکاری": [
        "تراش1", "تراش2", "تراش3", "تراش4"
    ],
    "کار دستی": [
        "پلیسه گیری", "سنگ زنی", "مونتاژ"
    ],
    "فرزکاری": [
        "فرز1", "فرز2", "فرز3", "فرز4", "فرز5", "فرز6", "اسپارک"
    ],
    "سوراخ کاری و قلاویزکاری": [
        "رادیال 1", "رادیال 2"
    ]
}

column_names_fa = {
    'id': 'شناسه',
    'person_name': 'نام کاربر',
    'unit': 'واحد',
    'shift': 'شیفت',
    'operation': 'عملیات',
    'machine': 'ماشین',
    'product': 'محصول',
    'work_type': 'نوع کار',
    'project_code': 'کد پروژه',
    'date': 'تاریخ',
    'operation_duration': 'مدت زمان کارکرد',
    'announced_duration': 'مدت زمان اعلام شده',
    'done_duration': 'مدت زمان انجام شده'
}

stoppage_list = [
    "عدم برنامه",
    "نبود مواد",
    "نبود ابزار",
    "آماده نبودن نقشه",
    "تعمیر و اصلاح دستگاه",
    "خرابی دستگاه",
    "توقف برقی",
    "مرخصی اپراتور",
    "کمبود اپراتور",
    "متفرقه"
]

# Mapping operators to machine groups
operator_machine_group = {
    "behzad_mehdizadeh": ["CNC"],
    "ebrahim_karimi": ["CNC"],
    "farhad_hashemkhani": ["CNC"],
    "hasan_heydari": ["فرزکاری", "تراشکاری"],
    "mehdi_davoodi": ["فرزکاری", "تراشکاری"],
    "mohammad_mohammadi": ["سوراخ کاری و قلاویزکاری"],
    "moradi": ["برشکاری", "جوشکاری"]
}

# Mapping operators to their workers
operator_workers = {
    "behzad_mehdizadeh": ["حمید قربانی",
                          "رسول نصیری",
                          "محسن آریایی",
                          "جواد کلهر",
                          "فرشاد بیگلری",
                          "بیت الله امامی",
                          ],

    "ebrahim_karimi": ["حمید قربانی",
                       "رسول نصیری",
                       "محسن آریایی",
                       "جواد کلهر",
                       "فرشاد بیگلری",
                       "بیت الله امامی",
                       ],

    "hasan_heydari": ["علی زمانی",
                      "رضا رشوند",
                      "رضا قاسمی",
                      "سید رضا حسینی",
                      "جواد حسین علیزاده",
                      "محمد رحمانی",
                      "حسن احمدی",
                      "داریوش درخشان",
                      ],
    "mehdi_davoodi": ["علی زمانی",
                      "رضا رشوند",
                      "رضا قاسمی",
                      "سید رضا حسینی",
                      "جواد حسین علیزاده",
                      "محمد رحمانی",
                      "حسن احمدی",
                      "داریوش درخشان",
                      ],

    "mohammad_mohammadi": ["وحید طالقانی",
                           "داود حیدری",
                           "رسول محمدخانی"
                           ],

    "moradi": ["حمید خانی",
               "رحمت ایمانی پور",
               "جواد مقدادی",
               ],

}

managers = ["ebrampour", "sohrabi", "damerchi"]

foremen = ["behzad_mehdizadeh", "ebrahim_karimi",
           "hasan_heydari", "mehdi_davoodi",
           "farhad_hashemkhani", "mohammad_mohammadi", "moradi"]

workers = ['rahmat_imanipour', 'hamid_khani', 'vahid_taleghani', 'rasool_mohammadkhani', 'farshad_biglari',
           'beytolah_emami', 'javad_kalhor', 'rasool_nasiri', 'mohsen_ariayi', 'reza_ghasemi', 'ali_zamani',
           'mohammad_rahmani', 'reza_rashvand', 'reza_hosseini', 'dariush_derakhshani', 'hamid_ghorbani',
           'rahim_mohammadkhani', 'javad_meghdadi', 'hasan_ahmadi', 'davood_heydari',
           'javad_hosseinalizadeh']

months = {
    0: "همه",
    1: "فروردین",
    2: "اردیبهشت",
    3: "خرداد",
    4: "تیر",
    5: "مرداد",
    6: "شهریور",
    7: "مهر",
    8: "آبان",
    9: "آذر",
    10: "دی",
    11: "بهمن",
    12: "اسفند",
}
