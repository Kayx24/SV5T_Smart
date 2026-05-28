import pandas as pd
from main import process_student


# ==================================================
# COLUMN NORMALIZER
# ==================================================

COLUMN_MAPPING = {

    "student_id":
    "student_id",

    "studentid":
    "student_id",

    "mssv":
    "student_id",

    "student_name":
    "student_name",

    "fullname":
    "student_name",

    "name":
    "student_name",

    "university":
    "university",

    "school":
    "university",

    "gpa":
    "gpa",

    "ielts":
    "ielts",

    "research":
    "research",

    "volunteer_hours":
    "volunteer_hours",

    "volunteer":
    "volunteer_hours",

    "disciplinary_action":
    "disciplinary_action",

    "discipline":
    "disciplinary_action"
}


# ==================================================
# NORMALIZE COLUMNS
# ==================================================

def normalize_columns(df):

    new_columns = {}

    for col in df.columns:

        clean_col = (
            str(col)
            .strip()
            .lower()
            .replace(" ", "_")
        )

        mapped_col = COLUMN_MAPPING.get(
            clean_col,
            clean_col
        )

        new_columns[col] = mapped_col

    df = df.rename(
        columns=new_columns
    )

    return df


# ==================================================
# PROCESS EXCEL
# ==================================================

def process_excel(file):

    results = []

    # ==============================================
    # READ FILE
    # ==============================================

    if file.name.endswith(".csv"):

        df = pd.read_csv(file)

    else:

        df = pd.read_excel(file)

    # ==============================================
    # NORMALIZE
    # ==============================================

    df = normalize_columns(df)

    # DEBUG
    print(df.columns)

    # ==============================================
    # LOOP ROWS
    # ==============================================

    for _, row in df.iterrows():

        student_data = {

            "student_id":
            str(row.get(
                "student_id",
                ""
            )),

            "student_name":
            str(row.get(
                "student_name",
                ""
            )),

            "university":
            str(row.get(
                "university",
                ""
            )),

            "gpa":
            float(row.get(
                "gpa",
                0
            )),

            "ielts":
            float(row.get(
                "ielts",
                0
            )),

            "research":
            bool(row.get(
                "research",
                False
            )),

            "volunteer_hours":
            int(row.get(
                "volunteer_hours",
                0
            )),

            "disciplinary_action":
            bool(row.get(
                "disciplinary_action",
                False
            ))
        }

        result = process_student(
            student_data
        )

        results.append(result)

    return results


# ==================================================
# PROCESS BATCH
# ==================================================

def process_batch(files):

    all_results = []

    for file in files:

        if file.name.endswith(
            (
                ".xlsx",
                ".csv"
            )
        ):

            results = process_excel(
                file
            )

            all_results.extend(
                results
            )

        else:

            mock_student = {

                "student_id":
                "OCR001",

                "student_name":
                "Mock OCR Student",

                "university":
                "ĐH Demo",

                "gpa":
                3.5,

                "ielts":
                6.5,

                "research":
                True,

                "volunteer_hours":
                80,

                "disciplinary_action":
                False
            }

            result = process_student(
                mock_student
            )

            all_results.append(
                result
            )

    return all_results