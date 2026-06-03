import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
import random
import time
import google.genai as genai
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
from main import process_student
from analytics_engine import analytics_query
from reasoning import generate_ai_reasoning
from batch_processor import process_batch
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

# DATABASE
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "backend", "sv5tot.db")
engine = create_engine(f"sqlite:///{DB_PATH}")


# ==========================================
# 3. SIDEBAR NAVIGATION (GLOBAL)
# ==========================================
st.sidebar.title("🧭 Điều hướng (Navigation)")
app_mode = st.sidebar.radio(
    "Chọn phân hệ:",
    ["👨‍🏫 Cán bộ (Reviewer Dashboard)", "🎓 Sinh viên (AI Assistant)"]
)


# =================================================================
# ================== PHÂN HỆ 1: CÁN BỘ XXét DUYỆT ==================
# =================================================================
if app_mode == "👨‍🏫 Cán bộ (Reviewer Dashboard)":
    
    # KHU VỰC SIDEBAR CHO CÁN BỘ
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🎓 SV5T Smart")
    st.sidebar.caption("AI-Assisted Reviewer Platform")
    
    st.sidebar.header("⚙️ Control Panel")

    # Khởi tạo trạng thái demo_counter
    if "demo_counter" not in st.session_state:
        st.session_state.demo_counter = 0

    # NÚT GENERATOR DUY NHẤT (Đã sửa lỗi trùng lặp ID)
    if st.sidebar.button("Generate Demo Student", key="btn_generate_demo_reviewer"):
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
        st.sidebar.success("Đã xử lý hồ sơ demo")
        time.sleep(0.5)
        st.rerun()

    st.sidebar.markdown("---")
    menu_options = ["📊 Tổng quan"]
    selected_menu = st.sidebar.radio("Điều hướng menu", menu_options, index=0)
    st.sidebar.markdown("---")

    # User Profile hiển thị ở Sidebar Cán bộ
    st.sidebar.markdown("""
    <div style="display: flex; align-items: center; gap: 15px;">
        <div style="background-color: #3498db; color: white; border-radius: 50%; width: 45px; height: 45px; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: 20px;">
            A
        </div>
        <div>
            <div style="font-weight: bold; font-size: 16px; line-height: 1.2;">Nguyễn Văn A</div>
            <div style="font-size: 13px; color: gray;">Admin</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # LOAD DATABASE (Chỉ chạy khi ở vai trò Cán bộ)
    try:
        query = "SELECT * FROM student_evaluations"
        df = pd.read_sql(query, engine)
    except Exception:
        df = pd.DataFrame()

    # KHU VỰC NỘI DUNG CHÍNH (MAIN CONTENT)
    if selected_menu == "📊 Tổng quan":
        st.title("Tổng quan hệ thống")
        st.markdown("<br>", unsafe_allow_html=True)

        # 1. KHU VỰC TẢI LÊN HỒ SƠ (BATCH UPLOAD)
        with st.container(border=True):
            st.markdown("## 📂 Tải lên & Xử lý hồ sơ (Batch Upload)")
            st.info("💡 **Hướng dẫn:** Kéo thả tệp danh sách (Excel, CSV) hoặc tài liệu minh chứng (PDF, JPG, PNG) vào khung bên dưới để hệ thống tự động phân tích và đánh giá.")
            uploaded_files = st.file_uploader(
                "Chọn tệp dữ liệu:",
                accept_multiple_files=True,
                type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"],
                key="uploader_main_dashboard"
            )
            if uploaded_files:
                if st.button("🚀 Bắt đầu xử lý AI & Rule Engine", use_container_width=True, key="btn_process_main_dashboard"):
                    with st.spinner("Hệ thống đang chạy thuật toán phân tích hồ sơ..."):
                        results = process_batch(uploaded_files)
                    st.success(f"✅ Đã xử lý thành công {len(results)} hồ sơ!")
                    st.balloons()
                    time.sleep(1.5)
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

        # 2. TÍNH TOÁN KPI & HIỂN THỊ THẺ GRADIENT
        total_students = len(df)
        total_approved = len(df[df["result"] == "PASS"]) if not df.empty and "result" in df.columns else 0
        total_rejected = len(df[df["result"] == "FAIL"]) if not df.empty and "result" in df.columns else 0
        total_high_risk = len(df[df["risk_level"] == "HIGH"]) if not df.empty and "risk_level" in df.columns else 0

        kpi_html = f"""
        <div style="display: flex; gap: 20px; margin-bottom: 25px;">
            <div style="flex: 1; background: linear-gradient(135deg, #3a7bd5, #3a6073); padding: 25px; border-radius: 15px; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.15); text-align: center;">
                <h3 style="margin: 0; font-size: 1.2rem; font-weight: 500; opacity: 0.9;">📦 Tổng hồ sơ</h3>
                <h1 style="margin: 10px 0 0 0; font-size: 3.5rem; font-weight: 700;">{total_students:,}</h1>
            </div>
            <div style="flex: 1; background: linear-gradient(135deg, #11998e, #38ef7d); padding: 25px; border-radius: 15px; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.15); text-align: center;">
                <h3 style="margin: 0; font-size: 1.2rem; font-weight: 500; opacity: 0.9;">✅ Đã duyệt</h3>
                <h1 style="margin: 10px 0 0 0; font-size: 3.5rem; font-weight: 700;">{total_approved:,}</h1>
            </div>
            <div style="flex: 1; background: linear-gradient(135deg, #FF416C, #FF4B2B); padding: 25px; border-radius: 15px; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.15); text-align: center;">
                <h3 style="margin: 0; font-size: 1.2rem; font-weight: 500; opacity: 0.9;">❌ Bị từ chối</h3>
                <h1 style="margin: 10px 0 0 0; font-size: 3.5rem; font-weight: 700;">{total_rejected:,}</h1>
            </div>
        </div>
        """
        st.markdown(kpi_html, unsafe_allow_html=True)

        # 3. HÀNG BIỂU ĐỒ DONUT CHART
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            with st.container(border=True):
                st.markdown("### Tổng quan đánh giá")
                df_eval = pd.DataFrame({
                    "Trạng thái": ["Đã duyệt", "Không đạt"],
                    "Số lượng": [total_approved, total_rejected]
                })
                if total_approved + total_rejected > 0:
                    fig_eval = px.pie(
                        df_eval,
                        values="Số lượng",
                        names="Trạng thái",
                        hole=0.6,
                        color="Trạng thái",
                        color_discrete_map={"Đã duyệt": "#3498db", "Không đạt": "#e74c3c"}
                    )
                    st.plotly_chart(fig_eval, width="stretch")
                else:
                    st.info("Chưa có dữ liệu đánh giá.")

        with chart_col2:
            with st.container(border=True):
                st.markdown("### Risk Level")
                if not df.empty and "risk_level" in df.columns:
                    vi_mapping = {"LOW": "Thấp", "MEDIUM": "Trung bình", "HIGH": "Cao", "CAO": "Cao", "THẤP": "Thấp", "TRUNG BÌNH": "Trung bình"}
                    df_risk = df['risk_level'].replace(vi_mapping).value_counts().reset_index()
                    df_risk.columns = ['Mức độ', 'Số lượng']
                    
                    if not df_risk.empty:
                        fig_risk = px.pie(
                            df_risk,
                            values="Số lượng",
                            names="Mức độ",
                            hole=0.6,
                            color="Mức độ",
                            color_discrete_map={"Cao": "#e74c3c", "Trung bình": "#f1c40f", "Thấp": "#2ecc71"}
                        )
                        st.plotly_chart(fig_risk, width="stretch")
                else:
                    st.info("Chưa có dữ liệu rủi ro.")

        # 4. HÀNG BẢNG DỮ LIỆU HOẠT ĐỘNG GẦN ĐÂY CÓ CĂN GIỮA TRẠNG THÁI
        with st.container(border=True):
            st.subheader("Hoạt động gần đây")
            
            html_rows = ""
            if not df.empty:
                recent_df = df.tail(10).iloc[::-1]
                for _, row in recent_df.iterrows():
                    time_str = row.get("created_at", "-")
                    student_id = row.get("student_id", "-")
                    student_name = row.get("student_name", "-")
                    status_raw = row.get("result", "QUEUE")
                    
                    fail_reasons = row.get("fail_reasons", "")
                    if pd.isna(fail_reasons) or not str(fail_reasons).strip() or status_raw == "PASS":
                        reasons_html = "-"
                    else:
                        reasons_list = [r.strip("- *") for r in str(fail_reasons).split('\n') if r.strip("- *")]
                        reasons_html = "<br>".join([f"• {r}" for r in reasons_list])
                        if not reasons_html:
                            reasons_html = str(fail_reasons)
                    
                    if status_raw == "PASS":
                        status_class = "status-approved"
                        status_text = "PASS"
                    elif status_raw == "FAIL":
                        status_class = "status-rejected"
                        status_text = "FAIL"
                    else:
                        status_class = "status-queue"
                        status_text = "QUEUE"
                        
                    html_rows += f"""<tr>
<td>{time_str}</td>
<td>{student_id}</td>
<td>{student_name}</td>
<td>{reasons_html}</td>
<td><span class="status-badge {status_class}">{status_text}</span></td>
</tr>"""
                
            if not html_rows:
                html_rows = "<tr><td colspan='5' style='text-align:center;'>Chưa có hoạt động hồ sơ nào</td></tr>"

            html_table = f"""
<style>
.status-badge {{
    padding: 6px 14px;
    border-radius: 14px;
    color: white;
    font-weight: 600;
    font-size: 0.85em;
    display: inline-block;
    text-align: center;
    min-width: 100px;
}}
.status-approved {{ background-color: #2ecc71; }}
.status-under-review {{ background-color: #f1c40f; color: #333; }}
.status-rejected {{ background-color: #e74c3c; }}
.status-queue {{ background-color: #95a5a6; }}

.table-wrapper {{
    border-radius: 12px;
    overflow: hidden;
    margin-top: 10px;
}}
.styled-table {{
    width: 100%;
    border-collapse: collapse;
    font-family: sans-serif;
    color: var(--text-color);
    background-color: var(--background-color);
}}
.styled-table th, .styled-table td {{
    padding: 14px 16px;
    border-bottom: 1px solid var(--border-color);
    text-align: left;
}}
.styled-table th:last-child, .styled-table td:last-child {{
    text-align: center;
}}
.styled-table th {{
    background-color: var(--secondary-background-color);
    color: var(--text-color);
    font-weight: bold;
}}
.styled-table tr:hover {{
    background-color: rgba(128, 128, 128, 0.1);
}}
.styled-table th:nth-child(1), .styled-table td:nth-child(1) {{ width: 15%; }}
.styled-table th:nth-child(2), .styled-table td:nth-child(2) {{ width: 15%; font-weight: bold; }}
.styled-table th:nth-child(3), .styled-table td:nth-child(3) {{ width: 20%; }}
.styled-table th:nth-child(4), .styled-table td:nth-child(4) {{ width: 35%; }}
.styled-table th:nth-child(5), .styled-table td:nth-child(5) {{ width: 15%; }}
</style>

<div class="table-wrapper">
<table class="styled-table">
<thead>
<tr>
<th>Thời gian</th>
<th>Mã hồ sơ</th>
<th>Tên sinh viên</th>
<th>Tiêu chí chưa đạt</th>
<th>Trạng thái</th>
</tr>
</thead>
<tbody>
{html_rows}
</tbody>
</table>
</div>
"""
            st.markdown(html_table, unsafe_allow_html=True)

        # 5. EXPLAINABLE REVIEW & AI ANALYTICS (Nằm trong Cán bộ)
        if not df.empty:
            st.divider()
            st.header("🧠 Giải thích hồ sơ nâng cao (Explainable Review)")
            student_ids = df["student_id"].tolist()
            selected_student = st.selectbox("Chọn mã số sinh viên để chẩn đoán chuyên sâu:", student_ids)
            selected_df = df[df["student_id"] == selected_student]

            if not selected_df.empty:
                student = selected_df.iloc[0]
                st.subheader(f"🎓 Sinh viên: {student['student_name']}")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                    ### 📌 Thông tin chung
                    - **Mã sinh viên:** {student['student_id']}
                    - **Trường:** {student['university']}
                    - **Kết quả:** `{student['result']}`
                    - **Mức độ rủi ro hệ thống cảnh báo:** `{student['risk_level']}`
                    """)
                with c2:
                    st.markdown(f"### ⚠️ Lý do chưa đạt từ AI\n{student['fail_reasons']}")
                    
                    # Bảng chi tiết tiêu chí chưa đạt
                    failed_criteria = []
                    criteria_map = {
                        "Đạo đức tốt": ("dao_duc_status", "dao_duc_details"),
                        "Học tập tốt": ("hoc_tap_status", "hoc_tap_details"),
                        "Thể lực tốt": ("the_luc_status", "the_luc_details"),
                        "Tình nguyện tốt": ("tinh_nguyen_status", "tinh_nguyen_details"),
                        "Hội nhập tốt": ("hoi_nhap_status", "hoi_nhap_details")
                    }
                    
                    for crit_name, (status_col, details_col) in criteria_map.items():
                        if status_col in student and student[status_col] == "FAIL":
                            details_text = str(student.get(details_col, ""))
                            details_html = details_text.replace('\n', '<br>')
                            failed_criteria.append(f"<tr><td style='padding: 8px; border-bottom: 1px solid var(--border-color);'><b>{crit_name}</b></td><td style='padding: 8px; border-bottom: 1px solid var(--border-color);'>{details_html}</td></tr>")
                            
                    if failed_criteria:
                        st.markdown("<br><b>📊 Chi tiết tiêu chí:</b>", unsafe_allow_html=True)
                        table_html = f"""
                        <table style="width:100%; border-collapse: collapse; font-size: 0.9em; margin-top: 10px;">
                            <thead><tr style="background-color: var(--secondary-background-color); text-align: left;"><th style="padding: 8px; border-bottom: 1px solid var(--border-color);">Tiêu chí</th><th style="padding: 8px; border-bottom: 1px solid var(--border-color);">Chi tiết đánh giá hệ thống</th></tr></thead>
                            <tbody>{''.join(failed_criteria)}</tbody>
                        </table>
                        """
                        st.markdown(table_html, unsafe_allow_html=True)
                st.divider()

            # TRỢ LÝ AI PHÂN TÍCH DỮ LIỆU
            st.header("🤖 Trợ lý AI Analytics")
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
            question = st.text_input("Nhập câu hỏi để AI truy vấn dữ liệu hệ thống (Ví dụ: 'Có bao nhiêu hồ sơ bị loại vì GPA?'):")
            if st.button("Hỏi AI Analytics"):
                if question.strip() == "":
                    st.warning("Vui lòng nhập câu hỏi.")
                else:
                    with st.spinner("AI đang tính toán phân tích dữ liệu..."):
                        answer = analytics_query(question)
                    st.markdown(answer)

            # FULL DATABASE VIEW
            st.subheader("📋 Toàn bộ cơ sở dữ liệu hệ thống (Full Database)")
            st.dataframe(df, width="stretch")


# =================================================================
# ================== PHÂN HỆ 2: TRỢ LÝ SINH VIÊN =================
# =================================================================
elif app_mode == "🎓 Sinh viên (AI Assistant)":
    
    st.title("🎓 STUDENT AI ASSISTANT & GAP ANALYSIS")
    st.markdown("Hệ thống hỗ trợ sinh viên tự đánh giá khả năng đạt danh hiệu **Sinh viên 5 Tốt** và đề xuất lộ trình cải thiện cá nhân hóa bằng AI.")

    if not HAS_STUDENT_MODULES:
        st.error("Hệ thống chưa tìm thấy các file logic của Sinh viên. Vui lòng kiểm tra lại cấu trúc thư mục `modules/`.")
    else:
        # 1. FORM NHẬP THÔNG TIN TẠI SIDEBAR
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

        # 2. XỬ LÝ PHÂN TÍCH TIÊU CHÍ (GAP ANALYSIS)
        if submit_button:
            student_data = {
                "gpa": gpa,
                "conduct_score": conduct_score,
                "ielts": ielts,
                "volunteer_days": volunteer_days,
                "research_projects": research_projects,
                "fitness_passed": fitness_passed
            }
            
            st.session_state['current_student_data'] = student_data
            analysis_result = analyze_gap(student_data, sv5t_rules)
            st.session_state['analysis_result'] = analysis_result
            st.session_state['recommendations'] = generate_recommendations(analysis_result["gaps"])

        if 'analysis_result' in st.session_state:
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

        # 3. CHATBOT CỐ VẤN AI
        st.divider()
        st.header("🤖 Cố vấn AI (Sinh viên 5 Tốt)")

        if "student_chat_history" not in st.session_state:
            st.session_state.student_chat_history = []

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