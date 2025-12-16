from app.models.base import BaseModel
from app import db


class Class(BaseModel):
    __tablename__ = "classes"

    name = db.Column(db.String(50), nullable=False)
    section = db.Column(db.String(10), nullable=True)
    academic_year = db.Column(db.String(20), nullable=False)

    class_teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    # Relationships
    students = db.relationship(
        "Student",
        back_populates="class_",
        cascade="all, delete-orphan"
    )

    subjects = db.relationship(
        "Subject",
        back_populates="class_",
        cascade="all, delete-orphan"
    )

    timetables = db.relationship(
        "Timetable",
        back_populates="class_",
        cascade="all, delete-orphan"
    )
