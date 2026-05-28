from api_client import call_mock_sv5tot_api
from rules_engine import evaluate_student
from database import save_to_database
from normalizer import normalize_student_data

# =====================================================
# PROCESS STUDENT
# =====================================================

def process_student(custom_student_data=None):

    # =================================================
    # INPUT DATA
    # =================================================

    if custom_student_data is not None:

        extracted_json = custom_student_data

    else:

        extracted_json = call_mock_sv5tot_api()

    # =================================================
    # NORMALIZE DATA
    # =================================================

    normalized_data = normalize_student_data(
        extracted_json
    )

    # =================================================
    # RULE ENGINE
    # =================================================

    evaluation_result = evaluate_student(
        normalized_data
    )

    # =================================================
    # CRITERIA RESULT
    # =================================================

    criteria_result = evaluation_result.get(
        "criteria",
        {}
    )

    # =================================================
    # BASIC VALUES
    # =================================================

    passed = evaluation_result.get(
        "passed",
        False
    )

    gpa = normalized_data.get(
        "gpa",
        0.0
    )

    conduct_score = normalized_data.get(
        "conduct_score",
        0
    )

    ielts = normalized_data.get(
        "ielts",
        0.0
    )

    volunteer_days = normalized_data.get(
        "volunteer_days",
        0
    )

    disciplinary_action = normalized_data.get(
        "disciplinary_action",
        False
    )

    # =================================================
    # RISK LEVEL
    # =================================================

    risk_level = "LOW"

    if not passed:

        risk_level = "HIGH"

    # Borderline cases
    elif (
        3.6 <= gpa <= 3.7
        or 90 <= conduct_score <= 92
        or 6.0 <= ielts <= 6.5
        or volunteer_days <= 5
    ):

        risk_level = "MEDIUM"

    # Disciplinary case = auto HIGH
    if disciplinary_action:

        risk_level = "HIGH"

    # =================================================
    # CONFIDENCE SCORE
    # =================================================

    confidence_score = 98

    suspicious_flags = "Không phát hiện"

    # GPA abnormal
    if gpa > 4.0:

        suspicious_flags = (
            "GPA vượt ngưỡng thực tế"
        )

        confidence_score = 70

    # IELTS abnormal
    if ielts > 9.0:

        suspicious_flags = (
            "IELTS vượt ngưỡng thực tế"
        )

        confidence_score = 65

    # Volunteer abnormal
    if volunteer_days > 365:

        suspicious_flags = (
            "Số ngày tình nguyện bất thường"
        )

        confidence_score = 60

    # =================================================
    # FINAL RESULT
    # =================================================

    final_result = {

        "student_data":
        normalized_data,

        "evaluation":
        evaluation_result,

        "criteria":
        criteria_result,

        "risk_level":
        risk_level,

        "confidence_score":
        confidence_score,

        "suspicious_flags":
        suspicious_flags
    }

    # =================================================
    # SAVE DATABASE
    # =================================================

    save_to_database(
        final_result
    )

    return final_result

# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    result = process_student()

    print(result)