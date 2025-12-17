from app.models.user import User

def require_role(user_id, allowed_roles):
    if not user_id:
        return None, ("Missing X-User-Id header", 401)

    user = User.query.get(user_id)
    if not user:
        return None, ("Invalid user", 401)

    if user.role not in allowed_roles:
        return None, ("Access denied", 403)

    return user, None
