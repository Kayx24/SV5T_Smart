
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import (
    Base,
    StudentEvaluation
)

import os

# =====================================================
# DATABASE PATH
# =====================================================

current_dir = os.path.dirname(
    os.path.abspath(__file__)
)

db_path = os.path.join(
    current_dir,
    "sv5tot.db"
)

DATABASE_URL = f"sqlite:///{db_path}"

# =====================================================
# ENGINE
# =====================================================

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

# =====================================================
# SAVE TO DATABASE
# =====================================================

def save_to_database(data):

    db = SessionLocal()

    try:

        student = data["student_data"]

        evaluation = data["evaluation"]

        criteria = evaluation.get(
            "criteria",
            {}
        )

        # =============================================
        # EXTRACT CRITERIA
        # =============================================

        dao_duc = criteria.get(
            "dao_duc_tot",
            {}
        )

        hoc_tap = criteria.get(
            "hoc_tap_tot",
            {}
        )

        the_luc = criteria.get(
            "the_luc_tot",
            {}
        )

        tinh_nguyen = criteria.get(
            "tinh_nguyen_tot",
            {}
        )

        hoi_nhap = criteria.get(
            "hoi_nhap_tot",
            {}
        )

        # =============================================
        # CREATE RECORD
        # =============================================

        new_record = StudentEvaluation(

            # =========================================
            # BASIC INFO
            # =========================================

            batch_id="SINGLE_UPLOAD",

            student_id=student.get(
                "student_id"
            ),

            student_name=student.get(
                "student_name"
            ),

            university=student.get(
                "university"
            ),

            # =========================================
            # FINAL RESULT
            # =========================================

            result=(

                "PASS"

                if evaluation.get(
                    "passed"
                )

                else "FAIL"
            ),

            fail_reasons=", ".join(

                evaluation.get(
                    "reasons",
                    []
                )
            ),

            # =========================================
            # ĐẠO ĐỨC
            # =========================================

            dao_duc_status=dao_duc.get(
                "status",
                "FAIL"
            ),

            dao_duc_details="\n".join(

                dao_duc.get(
                    "details",
                    []
                )
            ),

            # =========================================
            # HỌC TẬP
            # =========================================

            hoc_tap_status=hoc_tap.get(
                "status",
                "FAIL"
            ),

            hoc_tap_details="\n".join(

                hoc_tap.get(
                    "details",
                    []
                )
            ),

            # =========================================
            # THỂ LỰC
            # =========================================

            the_luc_status=the_luc.get(
                "status",
                "FAIL"
            ),

            the_luc_details="\n".join(

                the_luc.get(
                    "details",
                    []
                )
            ),

            # =========================================
            # TÌNH NGUYỆN
            # =========================================

            tinh_nguyen_status=tinh_nguyen.get(
                "status",
                "FAIL"
            ),

            tinh_nguyen_details="\n".join(

                tinh_nguyen.get(
                    "details",
                    []
                )
            ),

            # =========================================
            # HỘI NHẬP
            # =========================================

            hoi_nhap_status=hoi_nhap.get(
                "status",
                "FAIL"
            ),

            hoi_nhap_details="\n".join(

                hoi_nhap.get(
                    "details",
                    []
                )
            ),

            # =========================================
            # REVIEW WORKFLOW
            # =========================================

            review_status="QUEUE",

            reviewer_name="",

            reviewer_notes="",

            # =========================================
            # AI ANALYTICS
            # =========================================

            risk_level=data.get(
                "risk_level",
                "LOW"
            ),

            confidence_score=data.get(
                "confidence_score",
                100
            ),

            suspicious_flags=data.get(
                "suspicious_flags",
                "Không phát hiện"
            )
        )

        # =============================================
        # SAVE
        # =============================================

        db.add(new_record)

        db.commit()

        db.refresh(new_record)

        return new_record

    except Exception as e:

        db.rollback()

        print(
            f"Lỗi lưu CSDL: {e}"
        )

        return None

    finally:

        db.close()