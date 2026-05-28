import os
from dotenv import load_dotenv
import google.generativeai as genai

# LOAD ENV

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# CONFIG GEMINI

if API_KEY:

    genai.configure(
        api_key=API_KEY
    )

    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )

else:

    model = None


# AI REVIEWER ANALYSIS

def generate_ai_reasoning(
    student_data,
    evaluation_result
):

    # NO API KEY

    if model is None:

        return """
AI Assistant chưa được cấu hình.

Vui lòng kiểm tra:
- file .env
- GEMINI_API_KEY
"""

    # BUILD PROMPT

    prompt = f"""
Bạn là AI Reviewer Assistant hỗ trợ xét duyệt danh hiệu Sinh viên 5 tốt cấp Trung ương.

QUAN TRỌNG:
- KHÔNG tự quyết định PASS/FAIL
- PASS/FAIL đã được Rule Engine xử lý
- Bạn chỉ hỗ trợ reviewer phân tích hồ sơ

====================================
THÔNG TIN SINH VIÊN
====================================

Student ID:
{student_data.get("student_id")}

Họ tên:
{student_data.get("student_name")}

Trường:
{student_data.get("university")}

GPA:
{student_data.get("gpa")}

IELTS:
{student_data.get("ielts")}

Research:
{student_data.get("research")}

Volunteer Hours:
{student_data.get("volunteer_hours")}

Disciplinary Action:
{student_data.get("disciplinary_action")}

====================================
KẾT QUẢ RULE ENGINE
====================================

PASS:
{evaluation_result.get("passed")}

FAIL REASONS:
{evaluation_result.get("reasons")}

====================================
YÊU CẦU
====================================

Hãy hỗ trợ reviewer phân tích:

1. Tổng quan hồ sơ
2. Điểm mạnh
3. Điểm yếu
4. Risk Analysis
5. Recommendation cho reviewer
6. Các điểm cần hậu kiểm nếu có

KHÔNG được tự thay đổi kết quả Rule Engine.
"""

    # GENERATE

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"""
AI Assistant lỗi:

{str(e)}

Hệ thống vẫn hoạt động bình thường bằng Rule Engine.
"""