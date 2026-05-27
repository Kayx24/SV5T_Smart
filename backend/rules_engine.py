import json
import os

# =========================
# GET CURRENT FILE PATH
# =========================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

RULES_PATH = os.path.join(
    CURRENT_DIR,
    "config_rules.json"
)

# =========================
# LOAD RULES
# =========================

with open(
    RULES_PATH,
    "r",
    encoding="utf-8"
) as f:

    RULES = json.load(f)

# =========================
# RULE ENGINE
# =========================

def evaluate_student(student_data):

    reasons = []

    passed = True

    # =========================
    # GPA
    # =========================

    if student_data["gpa"] < RULES["gpa_min"]:

        passed = False

        reasons.append(
            f"GPA dưới yêu cầu "
            f"({student_data['gpa']} < "
            f"{RULES['gpa_min']})"
        )

    # =========================
    # IELTS
    # =========================

    if student_data["ielts"] < RULES["ielts_min"]:

        passed = False

        reasons.append(
            f"IELTS dưới yêu cầu "
            f"({student_data['ielts']} < "
            f"{RULES['ielts_min']})"
        )

    # =========================
    # Volunteer
    # =========================

    if (
        student_data["volunteer_hours"]
        < RULES["volunteer_hours_min"]
    ):

        passed = False

        reasons.append(
            "Không đủ giờ tình nguyện"
        )

    # =========================
    # Research
    # =========================

    if (
        RULES["research_required"]
        and not student_data["research"]
    ):

        passed = False

        reasons.append(
            "Thiếu nghiên cứu khoa học"
        )

    # =========================
    # Discipline
    # =========================

    if (
        RULES[
            "disciplinary_action_must_be_false"
        ]
        and student_data["disciplinary_action"]
    ):

        passed = False

        reasons.append(
            "Có vi phạm kỷ luật"
        )

    return {
        "passed": passed,
        "reasons": reasons
    }