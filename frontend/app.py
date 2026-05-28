import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
import random

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
from batch_processor import process_batch
from main import process_student
from analytics_engine import analytics_query
from reasoning import generate_ai_reasoning

# PAGE CONFIG
st.set_page_config(
    page_title="SV5T AI Reviewer",
    layout="wide"
)

# TITLE
st.title(
    "🎓 SV5T AI Reviewer System"
)

st.markdown("""
AI-assisted reviewer system hỗ trợ:

- xét duyệt Sinh viên 5 tốt
- batch processing
- reviewer workflow
- AI analytics
- explainable review
- reviewer dashboard
""")

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

# SIDEBAR
st.sidebar.header(
    "⚙️ Control Panel"
)

# DEMO GENERATOR
if "demo_counter" not in st.session_state:

    st.session_state.demo_counter = 0

if st.sidebar.button(
    "Generate Demo Student"
):

    st.session_state.demo_counter += 1

    # 4 FAIL -> 1 PASS
    if st.session_state.demo_counter % 5 == 0:

        demo_student = {

            "student_id":
            f"SVPASS{random.randint(100,999)}",

            "student_name":
            "Sinh Vien PASS Demo",

            "university":
            "ĐH Quốc Gia",

            "gpa":
            3.85,

            "conduct_score":
            95,

            "ielts":
            7.0,

            "research":
            True,

            "academic_award":
            True,

            "physical_certificate":
            True,

            "sports_award":
            False,

            "volunteer_days":
            10,

            "volunteer_award":
            True,

            "soft_skill_certificate":
            True,

            "international_activity":
            True,

            "disciplinary_action":
            False
        }

        result = process_student(
            demo_student
        )

    else:

        result = process_student()

    st.success(
        "Đã xử lý hồ sơ demo"
    )

# BATCH UPLOAD
st.header(
    "📂 Batch Upload"
)

uploaded_files = st.file_uploader(

    "Upload hồ sơ sinh viên",

    accept_multiple_files=True,

    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg",
        "xlsx",
        "csv"
    ]
)

if uploaded_files:

    st.success(
        f"Đã upload {len(uploaded_files)} file"
    )

    if st.button(
        "🚀 Process Batch"
    ):

        with st.spinner(
            "Đang xử lý batch..."
        ):

            results = process_batch(
                uploaded_files
            )

        st.success(
            f"Đã xử lý {len(results)} hồ sơ"
        )

# LOAD DATABASE
query = """
SELECT *
FROM student_evaluations
"""

df = pd.read_sql(
    query,
    engine
)

# DASHBOARD
if not df.empty:

    st.divider()

    st.header(
        "📊 Reviewer Dashboard"
    )

    # METRICS
    total_students = len(df)

    total_pass = len(
        df[df["result"] == "PASS"]
    )

    total_fail = len(
        df[df["result"] == "FAIL"]
    )

    total_high_risk = len(
        df[df["risk_level"] == "HIGH"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "TOTAL",
        total_students
    )

    col2.metric(
        "PASS",
        total_pass
    )

    col3.metric(
        "FAIL",
        total_fail
    )

    col4.metric(
        "HIGH RISK",
        total_high_risk
    )


    # PIE CHART
    st.subheader(
        "📈 PASS / FAIL Distribution"
    )

    pie_data = pd.DataFrame({

        "Result":
        ["PASS", "FAIL"],

        "Count":
        [total_pass, total_fail]
    })

    fig = px.pie(
        pie_data,
        names="Result",
        values="Count"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # RISK CHART
    st.subheader(
        "⚠️ Risk Level Distribution"
    )

    risk_chart = px.histogram(
        df,
        x="risk_level"
    )

    st.plotly_chart(
        risk_chart,
        width="stretch"
    )

    # FAIL STUDENTS

    st.subheader(
        "❌ FAIL Students"
    )

    fail_df = df[
        df["result"] == "FAIL"
    ]

    if not fail_df.empty:

        st.dataframe(

            fail_df[
                [
                    "student_id",
                    "student_name",
                    "university",
                    "fail_reasons",
                    "risk_level"
                ]
            ],

            width="stretch"
        )

    # STUDENT DETAIL VIEW
    st.divider()

    st.header(
        "🧠 Explainable Review"
    )

    student_ids = df[
        "student_id"
    ].tolist()

    selected_student = st.selectbox(

        "Chọn sinh viên",

        student_ids
    )

    selected_df = df[
        df["student_id"] == selected_student
    ]

    if not selected_df.empty:

        student = selected_df.iloc[0]

        st.subheader(
            f"🎓 {student['student_name']}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"""
### 📌 Thông tin

- Student ID: {student['student_id']}
- Trường: {student['university']}
- Result: {student['result']}
- Risk: {student['risk_level']}
"""
            )

        with col2:

            st.markdown(
                f"""
### ⚠️ Fail Reasons

{student['fail_reasons']}
"""
            )

        st.divider()

        # CRITERIA DETAILS

        st.subheader(
            "📋 5 Tiêu chí SV5T"
        )

        criteria_mapping = [

            (
                "Đạo đức tốt",
                "dao_duc_status",
                "dao_duc_details"
            ),

            (
                "Học tập tốt",
                "hoc_tap_status",
                "hoc_tap_details"
            ),

            (
                "Thể lực tốt",
                "the_luc_status",
                "the_luc_details"
            ),

            (
                "Tình nguyện tốt",
                "tinh_nguyen_status",
                "tinh_nguyen_details"
            ),

            (
                "Hội nhập tốt",
                "hoi_nhap_status",
                "hoi_nhap_details"
            )
        ]

        for title, status_col, detail_col in criteria_mapping:

            status = student[status_col]

            details = student[detail_col]

            if status == "PASS":

                st.success(
                    f"{title}: PASS"
                )

            else:

                st.error(
                    f"{title}: FAIL"
                )

            detail_lines = str(
                details
            ).split("\n")

            for line in detail_lines:

                st.markdown(
                    f"- {line}"
                )

            st.divider()

    # FULL DATABASE

    st.subheader(
        "📋 Full Database"
    )

    st.dataframe(
        df,
        width="stretch"
    )


# AI ANALYTICS
st.divider()
st.header(
    "🤖 AI Analytics Assistant"
)

question = st.text_input(
    "Hỏi AI Analytics"
)

if st.button(
    "Ask AI"
):

    if question.strip() == "":

        st.warning(
            "Nhập câu hỏi"
        )

    else:

        with st.spinner(
            "AI đang phân tích..."
        ):

            answer = analytics_query(
                question
            )

        st.markdown(
            answer
        )