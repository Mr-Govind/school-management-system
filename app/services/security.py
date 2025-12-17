from app.services.auth_context import get_current_user


def require_role(allowed_roles):
    user = get_current_user()
    if not user:
        return None, ("Unauthorized", 401)

    if user.role not in allowed_roles:
        return None, ("Forbidden", 403)

    return user, None
