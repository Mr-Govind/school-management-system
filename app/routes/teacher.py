from flask import Blueprint

teacher_bp = Blueprint("teacher", __name__)

@teacher_bp.route("/")
def teacher_home():
    return "Teacher Dashboard Route"
