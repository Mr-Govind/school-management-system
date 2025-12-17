from app.models.base import BaseModel
from app import db
from sqlalchemy.dialects.postgresql import UUID


class Student(BaseModel):
    __tablename__ = "students"

    full_name = db.Column(db.Text, nullable=False)
    roll_no = db.Column(db.Text, nullable=False)

    class_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("classes.id"),
        nullable=False
    )

    parent_name = db.Column(db.Text, nullable=True)
    parent_contact = db.Column(db.Text, nullable=True)

    # Relationship
    class_ = db.relationship("Class", back_populates="students")
