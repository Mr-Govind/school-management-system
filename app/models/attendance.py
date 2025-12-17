from app.models.base import BaseModel
from app import db
from sqlalchemy.dialects.postgresql import UUID


class Attendance(BaseModel):
    __tablename__ = "attendance"

    student_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("students.id"),
        nullable=False
    )

    date = db.Column(db.Date, nullable=False)

    status = db.Column(
        db.Text,
        nullable=False   # present / absent
    )

    marked_by = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id"),
        nullable=False
    )
