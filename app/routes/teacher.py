# from flask import Blueprint

# teacher_bp = Blueprint("teacher", __name__)

# @teacher_bp.route("/")
# def teacher_home():
#     return "Teacher Dashboard Route"


from flask import Blueprint, jsonify
from app.models.students import Student
from app.services.security import require_role

teacher_bp = Blueprint("teacher", __name__)


@teacher_bp.route("/class/<class_id>/students", methods=["GET"])
def get_students_by_class(class_id):
    """
    Teacher: Fetch all students for a given class
    """
    user, error = require_role(["teacher"])
    if error:
        return {"error": error[0]}, error[1]

    students = Student.query.filter_by(class_id=class_id).all()

    return jsonify([
        {
            "id": str(s.id),
            "name": s.full_name,
            "roll_no": s.roll_no
        }
        for s in students
    ])
