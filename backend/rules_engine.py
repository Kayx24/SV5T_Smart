# =====================================================
# SV5T CENTRAL RULE ENGINE
# =====================================================

def evaluate_student(student):

    criteria = {}

    global_fail_reasons = []

    # =================================================
    # 1. ĐẠO ĐỨC TỐT
    # =================================================

    dao_duc_details = []

    conduct_score = student.get(
        "conduct_score",
        0
    )

    disciplinary_action = student.get(
        "disciplinary_action",
        False
    )

    dao_duc_pass = True

    # Điểm rèn luyện

    if conduct_score >= 90:

        dao_duc_details.append(
            f"Điểm rèn luyện đạt ({conduct_score} >= 90)"
        )

    else:

        dao_duc_pass = False

        dao_duc_details.append(
            f"Điểm rèn luyện không đạt ({conduct_score} < 90)"
        )

    # Kỷ luật

    if disciplinary_action is False:

        dao_duc_details.append(
            "Không vi phạm kỷ luật"
        )

    else:

        dao_duc_pass = False

        dao_duc_details.append(
            "Có vi phạm kỷ luật"
        )

    criteria["dao_duc_tot"] = {

        "status":
        "PASS" if dao_duc_pass else "FAIL",

        "details":
        dao_duc_details
    }

    if not dao_duc_pass:

        global_fail_reasons.append(
            "Không đạt Đạo đức tốt"
        )

    # =================================================
    # 2. HỌC TẬP TỐT
    # =================================================

    hoc_tap_details = []

    gpa = student.get(
        "gpa",
        0
    )

    research = student.get(
        "research",
        False
    )

    academic_award = student.get(
        "academic_award",
        False
    )

    publication = student.get(
        "publication",
        False
    )

    academic_team = student.get(
        "academic_team",
        False
    )

    hoc_tap_pass = True

    # GPA

    if gpa >= 3.6:

        hoc_tap_details.append(
            f"GPA đạt ({gpa} >= 3.6)"
        )

    else:

        hoc_tap_pass = False

        hoc_tap_details.append(
            f"GPA không đạt ({gpa} < 3.6)"
        )

    # Điều kiện học thuật phụ

    if (
        research
        or academic_award
        or publication
        or academic_team
    ):

        hoc_tap_details.append(
            "Đạt tiêu chí nghiên cứu / học thuật"
        )

    else:

        hoc_tap_pass = False

        hoc_tap_details.append(
            "Thiếu tiêu chí nghiên cứu / học thuật"
        )

    criteria["hoc_tap_tot"] = {

        "status":
        "PASS" if hoc_tap_pass else "FAIL",

        "details":
        hoc_tap_details
    }

    if not hoc_tap_pass:

        global_fail_reasons.append(
            "Không đạt Học tập tốt"
        )

    # =================================================
    # 3. THỂ LỰC TỐT
    # =================================================

    the_luc_details = []

    physical_certificate = student.get(
        "physical_certificate",
        False
    )

    sports_award = student.get(
        "sports_award",
        False
    )

    the_luc_pass = True

    if (
        physical_certificate
        or sports_award
    ):

        the_luc_details.append(
            "Đạt tiêu chí thể lực"
        )

    else:

        the_luc_pass = False

        the_luc_details.append(
            "Không đạt tiêu chí thể lực"
        )

    criteria["the_luc_tot"] = {

        "status":
        "PASS" if the_luc_pass else "FAIL",

        "details":
        the_luc_details
    }

    if not the_luc_pass:

        global_fail_reasons.append(
            "Không đạt Thể lực tốt"
        )

    # =================================================
    # 4. TÌNH NGUYỆN TỐT
    # =================================================

    tinh_nguyen_details = []

    volunteer_days = student.get(
        "volunteer_days",
        0
    )

    volunteer_award = student.get(
        "volunteer_award",
        False
    )

    tinh_nguyen_pass = True

    if volunteer_days >= 5:

        tinh_nguyen_details.append(
            f"Đủ ngày tình nguyện ({volunteer_days} >= 5)"
        )

    elif volunteer_award:

        tinh_nguyen_details.append(
            "Có thành tích tình nguyện"
        )

    else:

        tinh_nguyen_pass = False

        tinh_nguyen_details.append(
            f"Không đủ ngày tình nguyện ({volunteer_days} < 5)"
        )

    criteria["tinh_nguyen_tot"] = {

        "status":
        "PASS" if tinh_nguyen_pass else "FAIL",

        "details":
        tinh_nguyen_details
    }

    if not tinh_nguyen_pass:

        global_fail_reasons.append(
            "Không đạt Tình nguyện tốt"
        )

    # =================================================
    # 5. HỘI NHẬP TỐT
    # =================================================

    hoi_nhap_details = []

    ielts = student.get(
        "ielts",
        0
    )

    soft_skill_certificate = student.get(
        "soft_skill_certificate",
        False
    )

    international_activity = student.get(
        "international_activity",
        False
    )

    integration_award = student.get(
        "integration_award",
        False
    )

    hoi_nhap_pass = True

    # Ngoại ngữ

    if ielts >= 6.0:

        hoi_nhap_details.append(
            f"IELTS đạt ({ielts} >= 6.0)"
        )

    else:

        hoi_nhap_pass = False

        hoi_nhap_details.append(
            f"IELTS không đạt ({ielts} < 6.0)"
        )

    # Hội nhập

    if (
        soft_skill_certificate
        or international_activity
        or integration_award
    ):

        hoi_nhap_details.append(
            "Đạt tiêu chí hội nhập"
        )

    else:

        hoi_nhap_pass = False

        hoi_nhap_details.append(
            "Thiếu hoạt động/kỹ năng hội nhập"
        )

    criteria["hoi_nhap_tot"] = {

        "status":
        "PASS" if hoi_nhap_pass else "FAIL",

        "details":
        hoi_nhap_details
    }

    if not hoi_nhap_pass:

        global_fail_reasons.append(
            "Không đạt Hội nhập tốt"
        )

    # =================================================
    # FINAL RESULT
    # =================================================

    final_pass = all([

        dao_duc_pass,
        hoc_tap_pass,
        the_luc_pass,
        tinh_nguyen_pass,
        hoi_nhap_pass
    ])

    return {

        "passed":
        final_pass,

        "criteria":
        criteria,

        "reasons":
        global_fail_reasons
    }