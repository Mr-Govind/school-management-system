from app.models.base import BaseModel
from app import db

class Student(BaseModel):
    __tablename__ = "students"

    admission_number = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)

    class_id = db.Column(
        db.Integer,
        db.ForeignKey("classes.id"),
        nullable=False
    )

    guardian_name = db.Column(db.String(100), nullable=True)
    guardian_contact = db.Column(db.String(20), nullable=True)

    # Relationships
    class_ = db.relationship("Class", back_populates="students")

    attendance_records = db.relationship(
        "Attendance",
        back_populates="student",
        cascade="all, delete-orphan"
    )
