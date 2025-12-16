from app.models.base import BaseModel
from app import db

class User(BaseModel):
    __tablename__ = "users"

    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(50), nullable=False)
    # is_active = db.Column(db.Boolean, default=True)
