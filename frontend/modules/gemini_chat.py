import os

from dotenv import load_dotenv
from google import genai

# =====================================================
# LOAD ENV
# =====================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# =====================================================
# GEMINI CLIENT
# =====================================================

client = None

if API_KEY:
    try:
        client = genai.Client(
            api_key=API_KEY
        )
    except Exception as e:
        print(f"Gemini init error: {e}")

# =====================================================
# STUDENT AI ASSISTANT
# =====================================================

def get_ai_advice(
    student_profile,
    user_question
):

    if client is None:
        return "❌ Chưa cấu hình GEMINI_API_KEY"

    prompt = f"""
Bạn là Student AI Assistant hỗ trợ sinh viên đạt danh hiệu Sinh viên 5 tốt.

THÔNG TIN SINH VIÊN:
{student_profile}

CÂU HỎI:
{user_question}

Yêu cầu:
- Trả lời bằng tiếng Việt.
- Ngắn gọn, dễ hiểu.
- Đưa ra lời khuyên thực tế.
- Nếu sinh viên còn thiếu tiêu chí nào thì nêu rõ.
- Khuyến khích sinh viên tiếp tục hoàn thiện hồ sơ.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"❌ Gemini Error: {str(e)}"