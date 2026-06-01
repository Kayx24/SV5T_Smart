import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
import random
import json

# ==========================================
# 1. SETUP PATHS & IMPORTS
# ==========================================
# CONNECT BACKEND
BACKEND_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.insert(0, BACKEND_PATH)

# Đảm bảo đường dẫn tới thư mục gốc (để load config/modules)
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_PATH)

RULES_PATH = os.path.join(ROOT_PATH, "config", "sv5t_rules.json")
sv5t_rules = None
    
if os.path.exists(RULES_PATH):
    with open(RULES_PATH, 'r', encoding='utf-8') as f:
         sv5t_rules = json.load(f)

# IMPORT BACKEND
from sqlalchemy import create_engine
from batch_processor import process_batch
from main import process_student
from analytics_engine import analytics_query
from reasoning import generate_ai_reasoning
from modules.gap_analysis import analyze_gap
from modules.recommendation import generate_recommendations
from modules.gemini_chat import get_ai_advice
HAS_STUDENT_MODULES = True

# ==========================================
# 2. PAGE CONFIG & DATABASE
# ==========================================
st.set_page_config(
    page_title="SV5T Smart System",
    layout="wide",
    page_icon="🎓"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "backend", "sv5tot.db")
engine = create_engine(f"sqlite:///{DB_PATH}")


# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🧭 Điều hướng (Navigation)")
app_mode = st.sidebar.radio(
    "Chọn phân hệ:",
    ["👨‍🏫 Cán bộ (Reviewer Dashboard)", "🎓 Sinh viên (AI Assistant)"]
)

# ================== PHÂN HỆ 1: CÁN BỘ XÉT DUYỆT ==================

if app_mode == "👨‍🏫 Cán bộ (Reviewer Dashboard)":
    st.title("🎓 SV5T AI Reviewer System")
    st.markdown("""
    AI-assisted reviewer system hỗ trợ:
    - xét duyệt Sinh viên 5 tốt
    - batch processing
    - reviewer workflow
    - AI analytics
    - explainable review
    - reviewer dashboard
    """)

    st.sidebar.header("⚙️ Control Panel")

    # DEMO GENERATOR
    if "demo_counter" not in st.session_state:
        st.session_state.demo_counter = 0

    if st.sidebar.button("Generate Demo Student"):
        st.session_state.demo_counter += 1
        # 4 FAIL -> 1 PASS
        if st.session_state.demo_counter % 5 == 0:
            demo_student = {
                "student_id": f"SVPASS{random.randint(100,999)}",
                "student_name": "Sinh Vien PASS Demo",
                "university": "ĐH Quốc Gia",
                "gpa": 3.85,
                "conduct_score": 95,
                "ielts": 7.0,
                "research": True,
                "academic_award": True,
                "physical_certificate": True,
                "sports_award": False,
                "volunteer_days": 10,
                "volunteer_award": True,
                "soft_skill_certificate": True,
                "international_activity": True,
                "disciplinary_action": False
            }
            result = process_student(demo_student)
        else:
            result = process_student()
        st.success("Đã xử lý hồ sơ demo")

    # BATCH UPLOAD
    st.header("📂 Batch Upload")
    uploaded_files = st.file_uploader(
        "Upload hồ sơ sinh viên",
        accept_multiple_files=True,
        type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"]
    )

    if uploaded_files:
        st.success(f"Đã upload {len(uploaded_files)} file")
        if st.button("🚀 Process Batch"):
            with st.spinner("Đang xử lý batch..."):
                results = process_batch(uploaded_files)
            st.success(f"Đã xử lý {len(results)} hồ sơ")

    # LOAD DATABASE
    try:
        query = "SELECT * FROM student_evaluations"
        df = pd.read_sql(query, engine)
    except Exception:
        df = pd.DataFrame()

    # DASHBOARD
    if not df.empty:
        st.divider()
        st.header("📊 Reviewer Dashboard")

        # METRICS
        total_students = len(df)
        total_pass = len(df[df["result"] == "PASS"])
        total_fail = len(df[df["result"] == "FAIL"])
        total_high_risk = len(df[df["risk_level"] == "HIGH"])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("TOTAL", total_students)
        col2.metric("PASS", total_pass)
        col3.metric("FAIL", total_fail)
        col4.metric("HIGH RISK", total_high_risk)

        # PIE CHART
        st.subheader("📈 PASS / FAIL Distribution")
        pie_data = pd.DataFrame({
            "Result": ["PASS", "FAIL"],
            "Count": [total_pass, total_fail]
        })
        fig = px.pie(pie_data, names="Result", values="Count")
        st.plotly_chart(fig, width="stretch")

        # RISK CHART
        st.subheader("⚠️ Risk Level Distribution")
        risk_chart = px.histogram(df, x="risk_level")
        st.plotly_chart(risk_chart, width="stretch")

        # FAIL STUDENTS
        st.subheader("❌ FAIL Students")
        fail_df = df[df["result"] == "FAIL"]
        if not fail_df.empty:
            st.dataframe(
                fail_df[["student_id", "student_name", "university", "fail_reasons", "risk_level"]],
                width="stretch"
            )

        # STUDENT DETAIL VIEW
        st.divider()
        st.header("🧠 Explainable Review")
        student_ids = df["student_id"].tolist()
        selected_student = st.selectbox("Chọn sinh viên", student_ids)
        selected_df = df[df["student_id"] == selected_student]

        if not selected_df.empty:
            student = selected_df.iloc[0]
            st.subheader(f"🎓 {student['student_name']}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                ### 📌 Thông tin
                - **Student ID:** {student['student_id']}
                - **Trường:** {student['university']}
                - **Result:** {student['result']}
                - **Risk:** {student['risk_level']}
                """)
            with c2:
                st.markdown(f"""
                ### ⚠️ Fail Reasons
                {student['fail_reasons']}
                """)
            st.divider()

        # FULL DATABASE
        st.subheader("📋 Full Database")
        st.dataframe(df, width="stretch")

    # AI ANALYTICS
    st.divider()
    st.header("🤖 AI Analytics Assistant")
    question = st.text_input("Hỏi AI Analytics")
    if st.button("Ask AI"):
        if question.strip() == "":
            st.warning("Nhập câu hỏi")
        else:
            with st.spinner("AI đang phân tích..."):
                answer = analytics_query(question)
            st.markdown(answer)


# ================== PHÂN HỆ 2: TRỢ LÝ SINH VIÊN =================

elif app_mode == "🎓 Sinh viên (AI Assistant)":
    
    st.title("🎓 STUDENT AI ASSISTANT & GAP ANALYSIS")
    st.markdown("Hệ thống hỗ trợ sinh viên tự đánh giá khả năng đạt danh hiệu **Sinh viên 5 Tốt** và đề xuất lộ trình cải thiện cá nhân hóa bằng AI.")

    if not HAS_STUDENT_MODULES:
        st.error("Hệ thống chưa tìm thấy các file logic của Sinh viên. Vui lòng kiểm tra lại cấu trúc thư mục `modules/`.")
    else:
        # 1. FORM NHẬP THÔNG TIN
        st.sidebar.header("📝 Nhập Hồ Sơ Của Bạn")
        with st.sidebar.form("student_form"):
            st.subheader("1. Thông tin học thuật")
            gpa = st.number_input("GPA hiện tại (Hệ 4.0)", min_value=0.0, max_value=4.0, step=0.1, value=3.0)
            conduct_score = st.number_input("Điểm rèn luyện", min_value=0, max_value=100, step=1, value=75)
            
            st.subheader("2. Ngoại ngữ & Tình nguyện")
            ielts = st.number_input("Điểm IELTS (hoặc tương đương)", min_value=0.0, max_value=9.0, step=0.5, value=5.0)
            volunteer_days = st.number_input("Số ngày tình nguyện", min_value=0, step=1, value=2)
            
            st.subheader("3. NCKH & Thể lực")
            research_projects = st.number_input("Số đề tài NCKH (cấp Khoa trở lên)", min_value=0, step=1, value=0)
            fitness_passed = st.checkbox("Đã đạt chứng nhận Thanh niên khỏe")
            
            submit_button = st.form_submit_button("🔍 Phân tích hồ sơ")

        # 2. XỬ LÝ GAP ANALYSIS
        if submit_button:
            student_data = {
                "gpa": gpa,
                "conduct_score": conduct_score,
                "ielts": ielts,
                "volunteer_days": volunteer_days,
                "research_projects": research_projects,
                "fitness_passed": fitness_passed
            }
            
            # Lưu state cho chatbot
            st.session_state['current_student_data'] = student_data
            
            # Gọi hàm analysis
            analysis_result = analyze_gap(student_data, sv5t_rules)
            st.session_state['analysis_result'] = analysis_result
            st.session_state['recommendations'] = generate_recommendations(analysis_result["gaps"])

        if 'analysis_result' in st.session_state:
            # Lấy dữ liệu từ bộ nhớ tạm ra để hiển thị
            analysis_result = st.session_state['analysis_result']
            recommendations = st.session_state['recommendations']
            
            col1, col2 = st.columns(2)
            with col1:
                st.header("📊 Kết quả đánh giá (Gap Analysis)")
                if analysis_result["qualified"]:
                    st.success("🎉 Xin chúc mừng! Hồ sơ của bạn ĐỦ ĐIỀU KIỆN xét duyệt Sinh viên 5 Tốt!")
                else:
                    st.error("⚠️ Bạn CHƯA ĐỦ ĐIỀU KIỆN. Cần cải thiện các tiêu chí sau:")
                    gaps = analysis_result["gaps"]
                    if 'gpa' in gaps: st.warning(f"- **Học tập:** Cần tăng thêm **{gaps['gpa']}** điểm GPA.")
                    if 'conduct_score' in gaps: st.warning(f"- **Đạo đức:** Còn thiếu **{gaps['conduct_score']}** điểm rèn luyện.")
                    if 'ielts' in gaps: st.warning(f"- **Hội nhập:** IELTS cần tăng thêm **{gaps['ielts']}** band.")
                    if 'volunteer_days' in gaps: st.warning(f"- **Tình nguyện:** Còn thiếu **{gaps['volunteer_days']}** ngày.")
                    if 'research_projects' in gaps: st.warning(f"- **Nghiên cứu:** Cần thực hiện thêm **{gaps['research_projects']}** đề tài NCKH.")
                    if 'fitness_passed' in gaps: st.warning(f"- **Thể lực:** Chưa đạt chứng nhận Thể lực.")

            with col2:
                st.header("🗺️ Lộ trình đề xuất (Recommendation Plan)")
                # recommendations = generate_recommendations(analysis_result["gaps"])
                
                if not recommendations:
                    st.info("Hồ sơ của bạn rất xuất sắc. Hãy tiếp tục duy trì phong độ nhé!")
                else:
                    for rec in recommendations:
                        if rec["priority"] == "High Priority":
                            st.error(f"🔴 **{rec['priority']}:** {rec['action']}")
                        elif rec["priority"] == "Medium Priority":
                            st.warning(f"🟡 **{rec['priority']}:** {rec['action']}")
                        else:
                            st.info(f"🔵 **{rec['priority']}:** {rec['action']}")

        # 3. GEMINI AI ASSISTANT CHATBOT
        st.divider()
        st.header("🤖 Cố vấn AI (Sinh viên 5 Tốt)")

        if "student_chat_history" not in st.session_state:
            st.session_state.student_chat_history = []

        # Hiển thị lịch sử chat
        for message in st.session_state.student_chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("VD: Đề tài NCKH cấp Khoa thường làm về chủ đề gì?"):
            st.session_state.student_chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Đang phân tích..."):
                    current_profile = st.session_state.get('current_student_data', "Sinh viên chưa điền form phân tích.")
                    response = get_ai_advice(current_profile, prompt)
                    st.markdown(response)
            
            st.session_state.student_chat_history.append({"role": "assistant", "content": response})