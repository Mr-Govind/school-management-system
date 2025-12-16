from app.models.base import BaseModel
from app import db

class Result(BaseModel):
    __tablename__ = "results"

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    exam_subject_id = db.Column(
        db.Integer,
        db.ForeignKey("exam_subjects.id"),
        nullable=False
    )

    marks_obtained = db.Column(db.Float, nullable=False)
    remarks = db.Column(db.String(255))

    student = db.relationship("Student")
    exam_subject = db.relationship("ExamSubject")

    __table_args__ = (
        db.UniqueConstraint(
            "student_id", "exam_subject_id",
            name="uq_student_exam_subject"
        ),
    )
