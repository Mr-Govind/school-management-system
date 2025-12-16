# from app.models.base import db, BaseModel

# class User(BaseModel):
#     __tablename__ = "users"

#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)
#     role_id = db.Column(
#         db.Integer,
#         db.ForeignKey("roles.id"),
#         nullable=False
#     )
#     is_active = db.Column(db.Boolean, default=True)

#     role = db.relationship("Role", back_populates="users")


from app.models.base import BaseModel
from app import db

class User(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    role = db.relationship("Role", back_populates="users")
