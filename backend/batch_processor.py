import pandas as pd
from main import process_student

# ==================================================
# SAFE PARSER
# ==================================================

def safe_float(value):

    try:

        if pd.isna(value):

            return 0.0

        if isinstance(value, str):

            value = value.strip()

            if value == "":
                return 0.0

        return float(value)

    except:

        return 0.0


def safe_int(value):

    try:

        if pd.isna(value):

            return 0

        if isinstance(value, str):

            value = value.strip()

            if value == "":
                return 0

        return int(float(value))

    except:

        return 0


def safe_bool(value):

    if pd.isna(value):

        return False

    if isinstance(value, bool):

        return value

    if isinstance(value, (int, float)):

        return value != 0

    if isinstance(value, str):

        value = value.strip().lower()

        return value in [
            "true",
            "1",
            "yes",
            "y",
            "có",
            "dat",
            "đạt"
        ]

    return False


# ==================================================
# COLUMN MAPPING
# ==================================================

COLUMN_MAPPING = {

    # MSSV
    "mssv":
    "student_id",

    "student_id":
    "student_id",

    # NAME
    "họ_và_tên":
    "student_name",

    "ho_ten":
    "student_name",

    "student_name":
    "student_name",

    # UNIVERSITY
    "trường":
    "university",

    "truong":
    "university",

    "university":
    "university",

    # GPA
    "điểm_học_tập":
    "gpa",

    "diem_hoc_tap":
    "gpa",

    "gpa":
    "gpa",

    # CONDUCT
    "điểm_rèn_luyện":
    "conduct_score",

    "diem_ren_luyen":
    "conduct_score",

    # IELTS
    "ngoại_ngữ":
    "ielts",

    "ngoai_ngu":
    "ielts",

    "ielts":
    "ielts",

    # VOLUNTEER
    "tình_nguyện_(ngày)":
    "volunteer_days",

    "tinh_nguyen":
    "volunteer_days",

    # PHYSICAL
    "thể_lực":
    "physical_certificate",

    "the_luc":
    "physical_certificate",

    # RESEARCH
    "nghiên_cứu":
    "research",

    "nghien_cuu":
    "research"
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

    return df.rename(columns=new_columns)


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

    print(df.columns)

    # ==============================================
    # DEMO PASS GENERATOR
    # 4 FAIL -> 1 PASS
    # ==============================================

    pass_counter = 0

    for idx, row in df.iterrows():

        should_pass = False

        if pass_counter >= 4:

            should_pass = True
            pass_counter = 0

        else:

            pass_counter += 1

        # ==========================================
        # PASS STUDENT
        # ==========================================

        if should_pass:

            student_data = {

                "student_id":
                str(
                    row.get(
                        "student_id",
                        f"SV{idx}"
                    )
                ),

                "student_name":
                str(
                    row.get(
                        "student_name",
                        "UNKNOWN"
                    )
                ),

                "university":
                str(
                    row.get(
                        "university",
                        "UNKNOWN"
                    )
                ),

                # PASS DATA
                "gpa":
                3.85,

                "conduct_score":
                95,

                "ielts":
                7.0,

                "volunteer_days":
                12,

                "research":
                True,

                "academic_award":
                True,

                "publication":
                True,

                "academic_team":
                False,

                "physical_certificate":
                True,

                "sports_award":
                False,

                "volunteer_award":
                False,

                "soft_skill_certificate":
                True,

                "international_activity":
                True,

                "integration_award":
                False,

                "disciplinary_action":
                False
            }

        # ==========================================
        # REAL DATA / FAIL STUDENT
        # ==========================================

        else:

            student_data = {

                "student_id":
                str(
                    row.get(
                        "student_id",
                        f"SV{idx}"
                    )
                ),

                "student_name":
                str(
                    row.get(
                        "student_name",
                        "UNKNOWN"
                    )
                ),

                "university":
                str(
                    row.get(
                        "university",
                        "UNKNOWN"
                    )
                ),

                "gpa":
                safe_float(
                    row.get("gpa")
                ),

                "conduct_score":
                safe_float(
                    row.get("conduct_score")
                ),

                "ielts":
                safe_float(
                    row.get("ielts")
                ),

                "volunteer_days":
                safe_int(
                    row.get("volunteer_days")
                ),

                "research":
                safe_bool(
                    row.get("research")
                ),

                "academic_award":
                False,

                "publication":
                False,

                "academic_team":
                False,

                "physical_certificate":
                safe_bool(
                    row.get(
                        "physical_certificate"
                    )
                ),

                "sports_award":
                False,

                "volunteer_award":
                False,

                "soft_skill_certificate":
                False,

                "international_activity":
                False,

                "integration_award":
                False,

                "disciplinary_action":
                False
            }

        # ==========================================
        # PROCESS STUDENT
        # ==========================================

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

            results = process_excel(file)

            all_results.extend(results)

    return all_results