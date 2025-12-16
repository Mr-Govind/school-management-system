from app.models.base import BaseModel
from app import db

class Timetable(BaseModel):
    __tablename__ = "timetable"

    class_id = db.Column(
        db.Integer,
        db.ForeignKey("classes.id"),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    day_of_week = db.Column(db.String(20), nullable=False)
    period = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    class_ = db.relationship("Class", back_populates="timetables")
    subject = db.relationship("Subject")
    teacher = db.relationship("User")
