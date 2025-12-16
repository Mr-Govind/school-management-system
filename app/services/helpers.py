from functools import wraps
from flask import request, jsonify
from app.models.user import User


def require_role(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = request.headers.get("X-USER-ID")

            if not user_id:
                return jsonify({"error": "Missing user context"}), 401

            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": "Invalid user"}), 401

            if user.role not in allowed_roles:
                return jsonify({"error": "Access denied"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
