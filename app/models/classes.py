from app.models.base import BaseModel
from app import db
from sqlalchemy.dialects.postgresql import UUID


class Class(BaseModel):
    __tablename__ = "classes"

    class_name = db.Column(db.Text, nullable=False)

    teacher_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id"),
        nullable=True
    )

    # Relationships (optional, read-only for now)
    students = db.relationship(
        "Student",
        back_populates="class_",
        lazy="select"
    )

    subjects = db.relationship(
        "Subject",
        back_populates="class_",
        lazy="select"
    )

    timetables = db.relationship(
        "Timetable",
        back_populates="class_",
        lazy="select"
    )
