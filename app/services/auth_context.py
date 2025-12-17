from flask import request
from app.models.user import User
from app.services.jwt_service import decode_token


def get_current_user():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ", 1)[1]
    payload = decode_token(token)
    if not payload:
        return None

    return User.query.get(payload["sub"])
