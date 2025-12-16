from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db


def create_user(full_name, email, password, role):
    hashed_password = generate_password_hash(password)

    user = User(
        full_name=full_name,
        email=email,
        password_hash=hashed_password,
        role=role
    )

    db.session.add(user)
    db.session.commit()
    return user


def verify_user(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        return None

    if not check_password_hash(user.password_hash, password):
        return None

    return user
