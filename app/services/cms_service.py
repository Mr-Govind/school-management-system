from app.models.cms_content import CMSContent
from app import db

def create_content(data, user_id):
    content = CMSContent(
    content_key=data["content_key"],
    page_key=data["page_key"],
    content_type=data["content_type"],
    content_value=data.get("content_value"),
    media_url=data.get("media_url"),
    style=data.get("style"),
    meta=data.get("metadata"),  
    created_by=user_id,
    updated_by=user_id
)

    db.session.add(content)
    db.session.commit()
    return content


def get_page_content(page_key):
    return CMSContent.query.filter_by(
        page_key=page_key,
        is_active=True
    ).all()


def update_content(content, data, user_id):
    for field in [
        "content_value", "media_url",
        "style", "is_active"
    ]:
        if field in data:
            setattr(content, field, data[field])

    if "metadata" in data:
        content.meta = data["metadata"]

    content.updated_by = user_id
    db.session.commit()
    return content
