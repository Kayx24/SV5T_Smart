import os
import json
import random

# =========================
# CONFIG
# =========================

BASE_DIR = "mock_documents"

os.makedirs(BASE_DIR, exist_ok=True)

# =========================
# SAMPLE DATA
# =========================

first_names = [
    "Nguyen",
    "Tran",
    "Le",
    "Pham",
    "Hoang"
]

middle_names = [
    "Van",
    "Thi",
    "Minh",
    "Gia",
    "Thanh"
]

last_names = [
    "An",
    "Binh",
    "Chau",
    "Duy",
    "Huy"
]

universities = [
    "ĐH CNTT",
    "ĐH Bách Khoa",
    "ĐH KHTN",
    "ĐH FPT"
]

# =========================
# GENERATE STUDENTS
# =========================

for i in range(1, 201):

    student_id = f"SV{i:04d}"

    student_folder = os.path.join(
        BASE_DIR,
        student_id
    )

    os.makedirs(student_folder, exist_ok=True)

    # =========================
    # RANDOM DATA
    # =========================

    full_name = (
        f"{random.choice(first_names)} "
        f"{random.choice(middle_names)} "
        f"{random.choice(last_names)}"
    )

    university = random.choice(universities)

    gpa = round(
        random.uniform(2.0, 4.0),
        2
    )

    ielts = random.choice([
        4.5,
        5.0,
        5.5,
        6.0,
        6.5,
        7.0
    ])

    volunteer_hours = random.randint(0, 150)

    research = random.choice([
        True,
        False
    ])

    disciplinary_action = random.choice([
        False,
        False,
        False,
        True
    ])

    # =========================
    # TRANSCRIPT
    # =========================

    transcript_text = f'''
    STUDENT TRANSCRIPT

    Student ID: {student_id}

    Full Name: {full_name}

    University: {university}

    GPA: {gpa}
    '''

    with open(
        os.path.join(student_folder, "transcript.txt"),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(transcript_text)

    # =========================
    # IELTS
    # =========================

    ielts_text = f'''
    IELTS CERTIFICATE

    Candidate: {full_name}

    Overall Band Score: {ielts}
    '''

    with open(
        os.path.join(student_folder, "ielts.txt"),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(ielts_text)

    # =========================
    # VOLUNTEER
    # =========================

    volunteer_text = f'''
    VOLUNTEER ACTIVITIES

    Student: {full_name}

    Total Volunteer Hours:
    {volunteer_hours}
    '''

    with open(
        os.path.join(student_folder, "volunteer.txt"),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(volunteer_text)

    # =========================
    # RESEARCH
    # =========================

    research_text = f'''
    SCIENTIFIC RESEARCH

    Student: {full_name}

    Research Participation:
    {research}
    '''

    with open(
        os.path.join(student_folder, "research.txt"),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(research_text)

    # =========================
    # DISCIPLINE
    # =========================

    discipline_text = f'''
    DISCIPLINARY REPORT

    Student: {full_name}

    Disciplinary Action:
    {disciplinary_action}
    '''

    with open(
        os.path.join(student_folder, "discipline.txt"),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(discipline_text)

    # =========================
    # PROFILE JSON
    # =========================

    profile = {
        "student_id": student_id,
        "student_name": full_name,
        "university": university,
        "gpa": gpa,
        "ielts": ielts,
        "volunteer_hours": volunteer_hours,
        "research": research,
        "disciplinary_action": disciplinary_action
    }

    with open(
        os.path.join(student_folder, "profile.json"),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            profile,
            f,
            indent=4,
            ensure_ascii=False
        )

print("Mock document dataset generated!")