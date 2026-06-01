import json
import os

# def load_rules():
#     """Đọc file cấu hình tiêu chuẩn SV5T"""
#     config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'sv5t_rules.json')
#     with open(config_path, 'r', encoding='utf-8') as f:
#         return json.load(f)

def analyze_gap(student_data, rules):
    """
    Phân tích khoảng cách (Gap Analysis) giữa hồ sơ sinh viên và tiêu chuẩn.
    Trả về Dictionary chứa trạng thái đạt, các tiêu chí thiếu và khoảng cách chi tiết.
    """
    # rules = load_rules()
    gaps = {}
    missing_criteria = []
    qualified = True

    # Phân tích GPA
    if student_data['gpa'] < rules['gpa']:
        gaps['gpa'] = round(rules['gpa'] - student_data['gpa'], 2)
        missing_criteria.append("Học tập (GPA)")
        qualified = False

    # Phân tích Điểm rèn luyện
    if student_data['conduct_score'] < rules['conduct_score']:
        gaps['conduct_score'] = rules['conduct_score'] - student_data['conduct_score']
        missing_criteria.append("Đạo đức (Điểm rèn luyện)")
        qualified = False

    # Phân tích IELTS
    if student_data['ielts'] < rules['ielts']:
        gaps['ielts'] = round(rules['ielts'] - student_data['ielts'], 1)
        missing_criteria.append("Hội nhập (IELTS)")
        qualified = False

    # Phân tích Tình nguyện
    if student_data['volunteer_days'] < rules['volunteer_days']:
        gaps['volunteer_days'] = rules['volunteer_days'] - student_data['volunteer_days']
        missing_criteria.append("Tình nguyện (Ngày)")
        qualified = False

    # Phân tích NCKH
    if student_data['research_projects'] < rules['research_projects']:
        gaps['research_projects'] = rules['research_projects'] - student_data['research_projects']
        missing_criteria.append("Nghiên cứu khoa học")
        qualified = False

    # Phân tích Thể lực
    if not student_data['fitness_passed']:
        gaps['fitness_passed'] = True
        missing_criteria.append("Thể lực")
        qualified = False

    return {
        "qualified": qualified,
        "missing_criteria": missing_criteria,
        "gaps": gaps
    }