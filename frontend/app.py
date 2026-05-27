import streamlit as st
import pandas as pd
import sys
import os
from reasoning import model

sys.path.append(
    os.path.abspath(
        "../backend"
    )
)

from main import process_student
from database import (
    SessionLocal,
    StudentEvaluation
)


st.set_page_config(
    page_title="SV5T AI Reviewer",
    page_icon="🎓",
    layout="wide"
)


st.title(
    "🎓 AI Reviewer Platform"
)

st.markdown(
    """
Hệ thống AI hỗ trợ xét duyệt
Sinh viên 5 tốt cấp Trung ương
"""
)


st.subheader(
    "📂 Upload Student Documents"
)

uploaded_file = st.file_uploader(

    "Upload document",

    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg"
    ]
)


if uploaded_file:

    if st.button(
        "🚀 Analyze Student"
    ):

        with st.spinner(
            "AI analyzing..."
        ):

            result = process_student()


        st.success(
            "Analysis completed"
        )

        col1, col2 = st.columns(2)


        with col1:

            st.subheader(
                "👨‍🎓 Student Information"
            )

            st.json(
                result["student_data"]
            )

        with col2:

            st.subheader(
                "📊 Evaluation"
            )

            st.json(
                result["evaluation"]
            )


        st.subheader("🤖 AI Reviewer Assistant")

        user_question = st.text_input(

            "Ask AI about this student"
        )

        if user_question:

            with st.spinner(
                "Gemini thinking..."
            ):

                prompt = f"""

        You are an AI reviewer assistant.

        Student data:
        {result["student_data"]}
        Evaluation:
        {result["evaluation"]}
        AI reasoning:
        {result["reasoning"]}
        Reviewer question:
        {user_question}
        Answer professionally.
        """

                response = model.generate_content(
                    prompt
                )

                st.info(
                    response.text
                )

        st.write(
            result["reasoning"]
        )

        st.subheader(
            "🧑‍⚖ Reviewer Decision"
        )

        decision = st.radio(
            "Reviewer Action",
            [
                "APPROVED",
                "REJECTED",
                "MANUAL_REVIEW"

            ]
        )

        if st.button(
            "💾 Save Reviewer Decision"
        ):

            db = SessionLocal()

            latest_record = db.query(
                StudentEvaluation
            ).order_by(
                StudentEvaluation.id.desc()
            ).first()

            if latest_record:

                latest_record.reviewer_decision = decision

                db.commit()

            db.close()

            st.success(
                f"Decision saved: {decision}"
            )


st.divider()
st.header(
    "📈 Reviewer Dashboard"
)

db = SessionLocal()

records = db.query(
    StudentEvaluation
).all()
db.close()

data = []

for r in records:

    data.append({

        "Student ID": r.student_id,
        "Name": r.student_name,
        "University": r.university,
        "Result": r.result,
        "Reviewer": r.reviewer_decision,
        "Risk": r.risk_level
    })

df = pd.DataFrame(data)

st.dataframe(

    df,
    use_container_width=True
)



if not df.empty:
    st.subheader(
        "📊 Analytics"
    )

    col1, col2 = st.columns(2)
    with col1:

        st.markdown(
            "### PASS / FAIL"
        )

        pass_fail = df[
            "Result"
        ].value_counts()

        st.plotly_chart({
            "data": [

                {
                    "labels": pass_fail.index,
                    "values": pass_fail.values,
                    "type": "pie",
                    "hole": 0.4
                }

            ]

        })


    with col2:
        st.markdown(
            "### Reviewer Decision"
        )

        reviewer_stats = df[
            "Reviewer"
        ].value_counts()

        st.plotly_chart({

            "data": [

                {

                    "labels": reviewer_stats.index,
                    "values": reviewer_stats.values,
                    "type": "pie"
                }
            ]
        })