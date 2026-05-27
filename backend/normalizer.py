def normalize_api_response(api_response):

    data = api_response["extracted_data"]

    return {
        "student_id": data.get("student_id"),
        "student_name": data.get("student_name"),
        "university": data.get("university"),
        "gpa": float(data.get("gpa", 0)),
        "ielts": float(data.get("ielts", 0)),
        "research": bool(data.get("research", False)),
        "volunteer_hours": int(
            data.get("volunteer_hours", 0)
        ),
        "disciplinary_action": bool(
            data.get("disciplinary_action", False)
        ),
        "confidence": api_response.get(
            "confidence",
            0.0
        )
    }