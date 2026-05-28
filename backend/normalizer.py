def normalize_student_data(raw_data):

    normalized = {}

    # ==========================================
    # BASIC INFO
    # ==========================================

    normalized["student_id"] = (
        raw_data.get("student_id")
        or raw_data.get("id")
        or raw_data.get("mssv")
        or "UNKNOWN"
    )

    normalized["student_name"] = (
        raw_data.get("student_name")
        or raw_data.get("name")
        or raw_data.get("full_name")
        or "UNKNOWN"
    )

    normalized["university"] = (
        raw_data.get("university")
        or raw_data.get("school")
        or "UNKNOWN"
    )

    # ==========================================
    # SCORES
    # ==========================================

    normalized["gpa"] = float(
        raw_data.get("gpa", 0)
    )

    normalized["conduct_score"] = float(
        raw_data.get("conduct_score", 0)
    )

    normalized["ielts"] = float(
        raw_data.get("ielts", 0)
    )

    normalized["volunteer_days"] = int(
        raw_data.get("volunteer_days", 0)
    )

    # ==========================================
    # ACADEMIC
    # ==========================================

    normalized["research"] = bool(
        raw_data.get("research", False)
    )

    normalized["academic_award"] = bool(
        raw_data.get("academic_award", False)
    )

    # ==========================================
    # PHYSICAL
    # ==========================================

    normalized["physical_certificate"] = bool(
        raw_data.get(
            "physical_certificate",
            False
        )
    )

    normalized["sports_award"] = bool(
        raw_data.get(
            "sports_award",
            False
        )
    )

    # ==========================================
    # VOLUNTEER
    # ==========================================

    normalized["volunteer_award"] = bool(
        raw_data.get(
            "volunteer_award",
            False
        )
    )

    # ==========================================
    # INTEGRATION
    # ==========================================

    normalized["soft_skill_certificate"] = bool(
        raw_data.get(
            "soft_skill_certificate",
            False
        )
    )

    normalized["international_activity"] = bool(
        raw_data.get(
            "international_activity",
            False
        )
    )

    # ==========================================
    # DISCIPLINE
    # ==========================================

    normalized["disciplinary_action"] = bool(
        raw_data.get(
            "disciplinary_action",
            False
        )
    )

    return normalized