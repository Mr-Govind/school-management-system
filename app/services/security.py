from functools import wraps
from flask import jsonify, g
from app.services.auth_context import get_current_user


def require_role(allowed_roles):
    # Normalize single role → list
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user, error = get_current_user()

            if error:
                return jsonify({"error": error[0]}), error[1]

            if user.role not in allowed_roles:
                return jsonify({"error": "Forbidden"}), 403

            # Attach user info to request context
            g.user_id = user.id
            g.user_role = user.role

            return fn(*args, **kwargs)

        return wrapper
    return decorator


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user, error = get_current_user()

        if error:
            message, status = error
            return jsonify({"error": message}), status

        # adjust role check to match your User model
        if user.role.lower() != "admin":
            return jsonify({"error": "Admin access required"}), 403

        return f(*args, **kwargs)

    return wrapper
