def generate_recommendations(gaps):
    """
    Sinh lộ trình đề xuất dựa trên các tiêu chí còn thiếu.
    Chia thành các mức độ ưu tiên.
    """
    recommendations = []
    
    # High Priority (Các tiêu chí bắt buộc, không cần tốn thời gian dài)
    if 'fitness_passed' in gaps:
        recommendations.append({"priority": "High Priority", "action": "Đăng ký tham gia kiểm tra Thể lực thanh niên khỏe ngay kỳ tới."})
    if 'conduct_score' in gaps:
        recommendations.append({"priority": "High Priority", "action": f"Tham gia thêm các hoạt động Đoàn/Hội để bù {gaps['conduct_score']} điểm rèn luyện."})

    # Medium Priority (Cần lên kế hoạch thực hiện)
    if 'volunteer_days' in gaps:
        recommendations.append({"priority": "Medium Priority", "action": f"Đăng ký tham gia Mùa hè xanh hoặc Xuân tình nguyện để tích lũy thêm {gaps['volunteer_days']} ngày tình nguyện."})
    if 'research_projects' in gaps:
        recommendations.append({"priority": "Medium Priority", "action": "Tìm giảng viên hướng dẫn và đăng ký ngay 1 đề tài Nghiên cứu khoa học cấp Khoa."})

    # Low Priority (Cần thời gian dài để cải thiện)
    if 'ielts' in gaps:
        recommendations.append({"priority": "Low Priority", "action": f"Ôn thi để tăng điểm IELTS thêm {gaps['ielts']} (Mục tiêu 6.0+)."})
    if 'gpa' in gaps:
        recommendations.append({"priority": "Low Priority", "action": f"Tập trung cải thiện GPA. Cần nâng thêm {gaps['gpa']} điểm (Mục tiêu 3.2+). Lên kế hoạch học nhóm."})

    return recommendations