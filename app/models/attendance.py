from app.models.base import BaseModel
from app import db

class Attendance(BaseModel):
    __tablename__ = "attendance"

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    class_id = db.Column(
        db.Integer,
        db.ForeignKey("classes.id"),
        nullable=False
    )

    date = db.Column(db.Date, nullable=False)

    status_id = db.Column(
        db.Integer,
        db.ForeignKey("attendance_status.id"),
        nullable=False
    )

    remarks = db.Column(db.String(255))

    student = db.relationship("Student", back_populates="attendance_records")
    class_ = db.relationship("Class")
    status = db.relationship("AttendanceStatus")

    __table_args__ = (
        db.UniqueConstraint(
            "student_id", "date",
            name="uq_student_attendance_per_day"
        ),
    )
