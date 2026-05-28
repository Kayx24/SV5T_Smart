def normalize_student_data(raw_data):

    normalized = {}

    # STUDENT ID

    normalized["student_id"] = (
        raw_data.get("student_id")
        or raw_data.get("id")
        or raw_data.get("mssv")
        or "UNKNOWN"
    )

    # NAME

    normalized["student_name"] = (
        raw_data.get("student_name")
        or raw_data.get("name")
        or raw_data.get("full_name")
        or "UNKNOWN"
    )

    # UNIVERSITY

    normalized["university"] = (
        raw_data.get("university")
        or raw_data.get("school")
        or raw_data.get("university_name")
        or "UNKNOWN"
    )

    # GPA

    normalized["gpa"] = float(

        raw_data.get("gpa")
        or raw_data.get("avg_score")
        or raw_data.get("grade_point")
        or 0
    )

    # IELTS

    normalized["ielts"] = float(

        raw_data.get("ielts")
        or raw_data.get("english_band")
        or raw_data.get("toeic_equivalent")
        or 0
    )


    # RESEARCH
    normalized["research"] = bool(

        raw_data.get("research")
        or raw_data.get("scientific_research")
        or raw_data.get("research_paper")
        or False
    )

    # VOLUNTEER
    normalized["volunteer_hours"] = int(

        raw_data.get("volunteer_hours")
        or raw_data.get("social_hours")
        or raw_data.get("volunteer")
        or 0
    )


    # DISCIPLINE
    normalized["disciplinary_action"] = bool(

        raw_data.get("disciplinary_action")
        or raw_data.get("discipline")
        or raw_data.get("violation")
        or False
    )

    return normalized