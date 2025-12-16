from app.models.base import BaseModel
from app import db

class Subject(BaseModel):
    __tablename__ = "subjects"

    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=True)

    class_id = db.Column(
        db.Integer,
        db.ForeignKey("classes.id"),
        nullable=False
    )

    class_ = db.relationship("Class", back_populates="subjects")
