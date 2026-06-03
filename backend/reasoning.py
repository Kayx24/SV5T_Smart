import os
import warnings
from dotenv import load_dotenv
from google import genai

warnings.filterwarnings(
    "ignore",
    category=UserWarning
)

# =====================================================
# LOAD ENV
# =====================================================

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

# =====================================================
# CONFIG GEMINI
# =====================================================

client = None

if GEMINI_API_KEY:

    try:

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    except Exception as e:

        print(
            f"Gemini init error: {e}"
        )

# =====================================================
# AI REVIEWER
# =====================================================

def generate_ai_reasoning(
    student_data,
    evaluation_result
):

    if client is None:

        return """
❌ Chưa cấu hình GEMINI_API_KEY
"""

    criteria = evaluation_result.get(
        "criteria",
        {}
    )

    prompt = f"""
Bạn là AI Reviewer Assistant hỗ trợ xét duyệt Sinh viên 5 tốt cấp Trung ương.

LUẬT QUAN TRỌNG:
- KHÔNG được thay đổi PASS/FAIL
- PASS/FAIL do Rule Engine quyết định
- Chỉ hỗ trợ reviewer phân tích hồ sơ

==================================================
THÔNG TIN SINH VIÊN
==================================================

MSSV:
{student_data.get("student_id")}

Họ tên:
{student_data.get("student_name")}

Trường:
{student_data.get("university")}

==================================================
KẾT QUẢ TỪ RULE ENGINE
==================================================

KẾT QUẢ:
{"PASS" if evaluation_result.get("passed") else "FAIL"}

CHI TIẾT:

{criteria}

==================================================
YÊU CẦU AI
==================================================

Hãy phân tích:

1. Tổng quan hồ sơ
2. Điểm mạnh
3. Điểm yếu
4. Tiêu chí nào đạt
5. Tiêu chí nào chưa đạt
6. Risk analysis
7. Recommendation cho reviewer
8. Hồ sơ có cần hậu kiểm không

Viết rõ ràng theo markdown.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"""
❌ Gemini Error:

{str(e)}
"""