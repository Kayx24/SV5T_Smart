from sqlalchemy import create_engine
import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "sv5tot.db")

engine = create_engine(f"sqlite:///{db_path}")


def analytics_query(question):

    df = pd.read_sql(
        "SELECT * FROM student_evaluations",
        engine
    )

    question = question.lower()

    if "bao nhiêu sinh viên fail" in question:

        total = len(
            df[df["result"] == "FAIL"]
        )

        return f"Có {total} sinh viên FAIL."

    elif "bao nhiêu sinh viên pass" in question:

        total = len(
            df[df["result"] == "PASS"]
        )

        return f"Có {total} sinh viên PASS."

    elif "risk high" in question:

        high_risk = df[
            df["risk_level"] == "HIGH"
        ]

        return high_risk[
            [
                "student_id",
                "student_name",
                "university"
            ]
        ].to_string(index=False)

    else:

        return "Không hiểu câu hỏi."