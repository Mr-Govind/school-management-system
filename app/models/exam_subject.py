from app.models.base import BaseModel
from app import db

class ExamSubject(BaseModel):
    __tablename__ = "exam_subjects"

    exam_id = db.Column(
        db.Integer,
        db.ForeignKey("exams.id"),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    max_marks = db.Column(db.Integer, nullable=False)

    exam = db.relationship("Exam", back_populates="subjects")
    subject = db.relationship("Subject")

    __table_args__ = (
        db.UniqueConstraint(
            "exam_id", "subject_id",
            name="uq_exam_subject"
        ),
    )
