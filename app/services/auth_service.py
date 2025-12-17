from flask import Blueprint, request, jsonify
from app.services.auth_service import verify_user
from app.services.jwt_service import generate_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = verify_user(email, password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user)

    return jsonify({
        "access_token": token,
        "token_type": "Bearer",
        "role": user.role
    }), 200
