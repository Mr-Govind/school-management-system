from app.models.base import BaseModel
from app import db

class AttendanceStatus(BaseModel):
    __tablename__ = "attendance_status"

    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(100))
