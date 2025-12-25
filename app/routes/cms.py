from flask import Blueprint, request, jsonify

from app.services.cms_service import (
    create_content,
    update_content,
    get_page_content   # ✅ FIX 1
)

from app.models.cms_content import CMSContent
from app.services.security import admin_required
from app.services.auth_context import get_current_user_id

cms_bp = Blueprint("cms", __name__)

# -----------------------------
# ADMIN: CREATE CMS CONTENT
# -----------------------------
@cms_bp.route("/admin/cms", methods=["POST"])
@admin_required
def create_cms():
    user_id = get_current_user_id()
    content = create_content(request.json, user_id)
    return jsonify({"id": str(content.id)}), 201


# -----------------------------
# ADMIN: UPDATE CMS CONTENT
# -----------------------------
@cms_bp.route("/admin/cms/<uuid:content_id>", methods=["PUT"])
@admin_required
def update_cms(content_id):
    content = CMSContent.query.get_or_404(content_id)
    user_id = get_current_user_id()
    update_content(content, request.json, user_id)
    return jsonify({"status": "updated"})


# -----------------------------
# ADMIN: FETCH ALL CMS CONTENT
# -----------------------------
@cms_bp.route("/admin/cms", methods=["GET"])
@admin_required
def get_all_cms():
    contents = (
        CMSContent
        .query
        .order_by(CMSContent.created_at.desc())
        .all()
    )

    return jsonify([
        {
            "id": str(c.id),
            "content_key": c.content_key,
            "page_key": c.page_key,
            "content_type": c.content_type,
            "content_value": c.content_value,
            "media_url": c.media_url,
            "style": c.style,
            "metadata": c.meta,
            "is_active": c.is_active
        }
        for c in contents
    ])
