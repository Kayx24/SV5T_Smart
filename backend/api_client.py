import random


def call_mock_sv5tot_api():

    first_names = [

        "Nguyen",
        "Tran",
        "Le",
        "Pham",
        "Hoang"

    ]

    middle_names = [

        "Thanh",
        "Minh",
        "Gia",
        "Quoc",
        "Duc"

    ]

    last_names = [

        "An",
        "Huy",
        "Linh",
        "Phuong",
        "Vy"

    ]

    universities = [

        "ĐH KHTN",
        "ĐH Bách Khoa",
        "ĐH CNTT",
        "ĐH Kinh tế",
        "ĐH Sư phạm"

    ]

    student_name = f"""

{random.choice(first_names)}

{random.choice(middle_names)}

{random.choice(last_names)}

""".replace("\n", " ").strip()

    return {

        "student_id":
        f"SV{random.randint(1000,9999)}",

        "student_name":
        student_name,

        "university":
        random.choice(universities),

        "gpa":
        round(
            random.uniform(2.0, 4.0),
            2
        ),

        "ielts":
        round(
            random.uniform(4.5, 8.0),
            1
        ),

        "research":
        random.choice(
            [True, False]
        ),

        "volunteer_hours":
        random.randint(10, 200),

        "disciplinary_action":
        random.choice(
            [True, False]
        ),

        "confidence":
        round(
            random.uniform(0.7, 0.99),
            2
        )
    }