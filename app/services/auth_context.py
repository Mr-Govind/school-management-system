from flask import request
from app.models.user import User
from app.services.jwt_service import decode_token


def get_current_user():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None, ("Missing or invalid Authorization header", 401)

    token = auth_header.split(" ")[1]
    payload = decode_token(token)

    if not payload:
        return None, ("Invalid or expired token", 401)

    user = User.query.get(payload["sub"])

    if not user:
        return None, ("User not found", 401)

    return user, None

def get_current_user_id():
    user, error = get_current_user()

    if error:
        return None

    return user.id
