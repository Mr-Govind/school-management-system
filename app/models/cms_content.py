import uuid
from app.models.base import BaseModel
from app import db
from sqlalchemy.dialects.postgresql import UUID

class CMSContent(BaseModel):
    __tablename__ = "cms_contents"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4   # ✅ FIX
    )

    content_key = db.Column(db.String(100), nullable=False)
    page_key = db.Column(db.String(100), nullable=False)

    content_type = db.Column(db.String(30), nullable=False)
    content_value = db.Column(db.Text)

    media_url = db.Column(db.Text)

    style = db.Column(db.JSON)
    meta = db.Column("metadata", db.JSON)

    is_active = db.Column(db.Boolean, default=True)

    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    updated_by = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
