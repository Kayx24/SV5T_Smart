import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

genai.configure(
    api_key=API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def generate_ai_reasoning(

    student_data,

    evaluation_result

):

    prompt = f"""

Bạn là AI Reviewer hỗ trợ xét duyệt
danh hiệu Sinh viên 5 tốt cấp Trung ương.

Nhiệm vụ của bạn:
- phân tích hồ sơ sinh viên
- giải thích PASS / FAIL
- phát hiện điểm mạnh
- phát hiện điểm yếu
- đánh giá mức độ rủi ro
- hỗ trợ reviewer đưa quyết định

=====================================
THÔNG TIN SINH VIÊN
=====================================

Student ID:
{student_data["student_id"]}

Họ tên:
{student_data["student_name"]}

Trường:
{student_data["university"]}

GPA:
{student_data["gpa"]}

IELTS:
{student_data["ielts"]}

Volunteer Hours:
{student_data["volunteer_hours"]}

Research:
{student_data["research"]}

Disciplinary Action:
{student_data["disciplinary_action"]}

Confidence:
{student_data["confidence"]}

=====================================
KẾT QUẢ RULE ENGINE
=====================================

PASS:
{evaluation_result["passed"]}

REASONS:
{evaluation_result["reasons"]}

=====================================
YÊU CẦU PHÂN TÍCH
=====================================

Hãy trả lời theo format:

1. Tổng quan hồ sơ
2. Điểm mạnh
3. Điểm yếu
4. Risk Analysis
5. Recommendation cho reviewer
6. Kết luận cuối cùng

Viết bằng tiếng Việt.
Văn phong chuyên nghiệp.
Ngắn gọn nhưng rõ ràng.
"""
    # CALL GEMINI
    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"""
AI reasoning failed.

Error:
{str(e)}
"""