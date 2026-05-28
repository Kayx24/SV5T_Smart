#not model
from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

Base = declarative_base()


# STUDENT EVALUATION TABLE

class StudentEvaluation(Base):

    __tablename__ = (
        "student_evaluations"
    )

    # PRIMARY KEY

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # BASIC INFO
    batch_id = Column(String)
    student_id = Column(String)
    student_name = Column(String)
    university = Column(String)

    # FINAL RESULT
    result = Column(String)
    fail_reasons = Column(Text)

    # ĐẠO ĐỨC TỐT
    dao_duc_status = Column(String)
    dao_duc_details = Column(Text)

    # HỌC TẬP TỐT
    hoc_tap_status = Column(String)
    hoc_tap_details = Column(Text)

    # THỂ LỰC TỐT
    the_luc_status = Column(String)
    the_luc_details = Column(Text)

    # TÌNH NGUYỆN TỐT
    tinh_nguyen_status = Column(String)
    tinh_nguyen_details = Column(Text)

    # HỘI NHẬP TỐT
    hoi_nhap_status = Column(String)
    hoi_nhap_details = Column(Text)

    # REVIEW WORKFLOW

    review_status = Column(
        String,
        default="QUEUE"
    )

    reviewer_name = Column(String)

    reviewer_notes = Column(Text)

    # AI ANALYTICS

    risk_level = Column(String)
    confidence_score = Column(Integer)
    suspicious_flags = Column(Text)
