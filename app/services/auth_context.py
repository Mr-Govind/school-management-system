from flask import request
from app.models.user import User
from app.services.jwt_service import decode_token


def get_current_user():
    """
    Priority:
    1. JWT Authorization header
    2. X-User-Id header (legacy)
    """

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]
        payload = decode_token(token)
        if payload:
            return User.query.get(payload["sub"])

    # Fallback (Version-1 support)
    user_id = request.headers.get("X-User-Id")
    if user_id:
        return User.query.get(user_id)

    return None
