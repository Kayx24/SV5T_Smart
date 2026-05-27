from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text


Base = declarative_base()


class StudentEvaluation(Base):

    __tablename__ = "student_evaluations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(String)
    student_name = Column(String)
    university = Column(String)
    result = Column(String)
    reasoning = Column(Text)
    reviewer_decision = Column(String)
    risk_level = Column(String)