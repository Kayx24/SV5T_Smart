import pandas as pd
import os

FIELD_MAPPING = {

    "student_name": [
        "student_name",
        "name",
        "họ_và_tên",
        "ho_ten",
        "fullname"
    ],

    "university": [
        "university",
        "truong",
        "trường",
        "school"
    ],


    "gpa": [
        "gpa",
        "điểm_học_tập",
        "diem_hoc_tap",
        "academic_score"
    ],


    "conduct_score": [
        "điểm_rèn_luyện",
        "diem_ren_luyen",
        "conduct_score"
    ],


    "ielts": [
        "ielts",
        "ngoại_ngữ",
        "ngoai_ngu",
        "english_score"
    ],


    "volunteer_days": [
        "tình_nguyện_(ngày)",
        "tinh_nguyen",
        "volunteer_days"
    ],


    "physical_certificate": [
        "thể_lực",
        "the_luc",
        "physical"
    ]
}


def normalize_column(col):

    return (
        str(col)
        .strip()
        .lower()
    )



def auto_map_columns(df):

    mapped_columns = {}

    normalized_cols = {

        normalize_column(col): col

        for col in df.columns
    }

    for standard_field, aliases in FIELD_MAPPING.items():

        for alias in aliases:

            alias = normalize_column(alias)

            if alias in normalized_cols:

                mapped_columns[
                    standard_field
                ] = normalized_cols[alias]

                break

    return mapped_columns



def extract_tabular_file(file):

    filename = file.name.lower()
    if filename.endswith(".xlsx"):

        df = pd.read_excel(file)

    elif filename.endswith(".csv"):

        df = pd.read_csv(file)

    else:

        return []


    column_mapping = auto_map_columns(df)

    students = []

    for idx, row in df.iterrows():

        student = {

            "student_id":
            f"SV{1000 + idx}",

            "student_name":
            str(
                row.get(
                    column_mapping.get(
                        "student_name",
                        ""
                    ),
                    ""
                )
            ),

            "university":
            str(
                row.get(
                    column_mapping.get(
                        "university",
                        ""
                    ),
                    ""
                )
            ),

            "gpa":
            safe_float(
                row.get(
                    column_mapping.get(
                        "gpa",
                        ""
                    ),
                    0
                )
            ),

            "conduct_score":
            safe_float(
                row.get(
                    column_mapping.get(
                        "conduct_score",
                        ""
                    ),
                    0
                )
            ),


            "ielts":
            safe_float(
                row.get(
                    column_mapping.get(
                        "ielts",
                        ""
                    ),
                    0
                )
            ),


            "volunteer_days":
            safe_float(
                row.get(
                    column_mapping.get(
                        "volunteer_days",
                        ""
                    ),
                    0
                )
            ),


            "research":
            True,

            "academic_award":
            False,

            "physical_certificate":
            parse_boolean(
                row.get(
                    column_mapping.get(
                        "physical_certificate",
                        ""
                    ),
                    False
                )
            ),

            "sports_award":
            False,

            "volunteer_award":
            False,

            "soft_skill_certificate":
            True,

            "international_activity":
            True,

            "disciplinary_action":
            False
        }

        students.append(student)

    return students

def safe_float(value):

    try:

        return float(value)

    except:

        return 0.0

def parse_boolean(value):

    value = str(value).lower()

    return value in [

        "1",
        "true",
        "yes",
        "đạt",
        "pass"
    ]
