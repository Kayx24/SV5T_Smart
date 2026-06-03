import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
import random
import time
import google.genai as genai

# CONNECT BACKEND
BACKEND_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "backend"
    )
)

sys.path.insert(0, BACKEND_PATH)
# IMPORT BACKEND
from sqlalchemy import create_engine
from main import process_student
from analytics_engine import analytics_query
from reasoning import generate_ai_reasoning
from batch_processor import process_batch

# PAGE CONFIG
st.set_page_config(
    page_title="SV5T AI Reviewer",
    layout="wide"
)

# DATABASE

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_PATH = os.path.join(
    BASE_DIR,
    "..",
    "backend",
    "sv5tot.db"
)

engine = create_engine(
    f"sqlite:///{DB_PATH}"
)

# KHU VỰC SIDEBAR
st.sidebar.markdown("## 🎓 SV5T Smart")
st.sidebar.caption("AI-Assisted Reviewer Platform")

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
    st.sidebar.success("Đã xử lý hồ sơ demo")
st.sidebar.markdown("---")

menu_options = [
    "📊 Tổng quan"
]
selected_menu = st.sidebar.radio("Điều hướng menu", menu_options, index=0)

st.sidebar.markdown("---")

# User Profile
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

# LOAD DATABASE
query = """
SELECT *
FROM student_evaluations
"""

try:
    df = pd.read_sql(query, engine)
except Exception:
    df = pd.DataFrame()

# KHU VỰC NỘI DUNG CHÍNH (MAIN CONTENT)
if selected_menu == "📊 Tổng quan":
    # Header
    st.title("Tổng quan hệ thống")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- KHU VỰC TẢI LÊN HỒ SƠ ---
    with st.expander("📂 Tải lên & Xử lý hồ sơ (Batch Upload)", expanded=True):
        uploaded_files = st.file_uploader(
            "Kéo thả tệp danh sách (Excel, CSV) hoặc tài liệu minh chứng (PDF, JPG, PNG) vào đây:",
            accept_multiple_files=True,
            type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"]
        )
        if uploaded_files:
            if st.button("🚀 Bắt đầu xử lý AI & Rule Engine", use_container_width=True):
                with st.spinner("Hệ thống đang chạy thuật toán phân tích hồ sơ..."):
                    results = process_batch(uploaded_files)
                st.success(f"✅ Đã xử lý thành công {len(results)} hồ sơ!")
                st.balloons()
                time.sleep(1.5)
                st.rerun()  # Tự động load lại trang để cập nhật KPI & Biểu đồ
    st.markdown("<br>", unsafe_allow_html=True)

    # Tính toán dữ liệu thực tế từ Database
    total_students = len(df)
    total_approved = len(df[df["result"] == "PASS"]) if not df.empty and "result" in df.columns else 0
    total_rejected = len(df[df["result"] == "FAIL"]) if not df.empty and "result" in df.columns else 0

    # Hàng 1: Các chỉ số KPI (Dạng thẻ Gradient sinh động)
    kpi_html = f"""
    <div style="display: flex; gap: 20px; margin-bottom: 25px;">
        <div style="flex: 1; background: linear-gradient(135deg, #3a7bd5, #3a6073); padding: 25px; border-radius: 15px; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.15); text-align: center; transition: transform 0.3s;">
            <h3 style="margin: 0; font-size: 1.2rem; font-weight: 500; opacity: 0.9;">📦 Tổng hồ sơ</h3>
            <h1 style="margin: 10px 0 0 0; font-size: 3.5rem; font-weight: 700;">{total_students:,}</h1>
        </div>
        <div style="flex: 1; background: linear-gradient(135deg, #11998e, #38ef7d); padding: 25px; border-radius: 15px; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.15); text-align: center; transition: transform 0.3s;">
            <h3 style="margin: 0; font-size: 1.2rem; font-weight: 500; opacity: 0.9;">✅ Đã duyệt</h3>
            <h1 style="margin: 10px 0 0 0; font-size: 3.5rem; font-weight: 700;">{total_approved:,}</h1>
        </div>
        <div style="flex: 1; background: linear-gradient(135deg, #FF416C, #FF4B2B); padding: 25px; border-radius: 15px; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.15); text-align: center; transition: transform 0.3s;">
            <h3 style="margin: 0; font-size: 1.2rem; font-weight: 500; opacity: 0.9;">❌ Bị từ chối</h3>
            <h1 style="margin: 10px 0 0 0; font-size: 3.5rem; font-weight: 700;">{total_rejected:,}</h1>
        </div>
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)

    # Hàng 2: Biểu đồ Donut Chart
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
                    color_discrete_map={
                        "Đã duyệt": "#3498db",  # Xanh dương
                        "Không đạt": "#e74c3c"  # Đỏ
                    }
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
                        color_discrete_map={
                            "Cao": "#e74c3c",       # Đỏ
                            "Trung bình": "#f1c40f", # Vàng
                            "Thấp": "#2ecc71"       # Xanh lá
                        }
                    )
                    st.plotly_chart(fig_risk, width="stretch")
            else:
                st.info("Chưa có dữ liệu rủi ro.")

    # Hàng 3: Bảng dữ liệu với tuỳ chỉnh CSS cho Badges (Pills)
    with st.container(border=True):
        st.subheader("Hoạt động gần đây")
        
        html_rows = ""
        if not df.empty:
            # Lấy 10 hoạt động / hồ sơ gần nhất
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
.styled-table th:nth-child(5), .styled-table td:nth-child(5) {{ 
    width: 15%; 
    text-align: center; 
}}
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