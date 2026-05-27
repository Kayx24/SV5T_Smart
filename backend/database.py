from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models import StudentEvaluation

DATABASE_URL = "sqlite:///sv5tot.db"

engine = create_engine(

    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def save_to_database(data):

    db = SessionLocal()
    result_text = (
        "PASS"
        if data["evaluation"]["passed"]
        else "FAIL"
    )

    risk_level = "LOW"
    if result_text == "FAIL":
        risk_level = "HIGH"

    new_record = StudentEvaluation(

        student_id=data["student_data"]["student_id"],
        student_name=data["student_data"]["student_name"],
        university=data["student_data"]["university"],
        result=result_text,
        reasoning=data["reasoning"],
        reviewer_decision="PENDING",
        risk_level=risk_level
    )

    db.add(new_record)
    db.commit()
    db.close()