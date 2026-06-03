import os
import google.genai as genai
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv(dotenv_path=r"Q:\anaconda\envs\sv5t")
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None

def get_ai_advice(student_profile, user_question):
    """
    Gửi prompt chứa ngữ cảnh hồ sơ sinh viên và câu hỏi tới Gemini.
    """
    if client is None:
        return "Lỗi: Chưa cấu hình GEMINI_API_KEY trong file .env."

    system_prompt = f"""
    You are Student AI Assistant. You help students achieve "Sinh Vien 5 Tot" (SV5T) criteria.
    Dưới đây là hồ sơ hiện tại của sinh viên:
    {student_profile}
    
    Hãy dựa vào hồ sơ này để trả lời câu hỏi của sinh viên một cách ngắn gọn, khích lệ và thực tế bằng tiếng Việt.
    Câu hỏi của sinh viên: {user_question}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=system_prompt
        )
        return response.text
    except Exception as e:
        return f"Đã xảy ra lỗi kết nối với AI: {str(e)}"