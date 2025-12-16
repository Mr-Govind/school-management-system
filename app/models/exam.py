from app.models.base import BaseModel
from app import db

class Exam(BaseModel):
    __tablename__ = "exams"

    name = db.Column(db.String(100), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)

    class_id = db.Column(
        db.Integer,
        db.ForeignKey("classes.id"),
        nullable=False
    )

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    class_ = db.relationship("Class")
    subjects = db.relationship(
        "ExamSubject",
        back_populates="exam",
        cascade="all, delete-orphan"
    )
