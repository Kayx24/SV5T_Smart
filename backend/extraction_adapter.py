import random


def mock_extract_documents(files):

    return {

        "student_id":
        f"SV{random.randint(1000,9999)}",

        "student_name":
        random.choice([
            "Nguyen Van A",
            "Tran Thi B",
            "Le Minh C"
        ]),

        "university":
        random.choice([
            "ĐH Bách Khoa",
            "ĐH CNTT",
            "ĐH KHTN"
        ]),

        "gpa":
        round(
            random.uniform(2.5, 4.0),
            2
        ),

        "ielts":
        round(
            random.uniform(5.0, 8.0),
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
        )
    }