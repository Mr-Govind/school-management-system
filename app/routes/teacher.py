from flask import Blueprint, jsonify, g
from app.models.students import Student
from app.models.classes import Class
from app.services.security import require_role

teacher_bp = Blueprint("teacher", __name__)

@teacher_bp.route("/class/<uuid:class_id>/students", methods=["GET"])
@require_role(["teacher"])
def get_students_by_class(class_id):
    """
    Teacher: Fetch all students for a given class
    """

    teacher_id = g.user_id  # set by require_role

    # Ensure this class belongs to the logged-in teacher
    cls = Class.query.filter_by(
        id=class_id,
        teacher_id=teacher_id
    ).first()

    if not cls:
        return jsonify({"error": "Unauthorized access to class"}), 403

    students = Student.query.filter_by(class_id=class_id).all()

    return jsonify([
        {
            "id": str(s.id),
            "full_name": s.full_name,
            "roll_no": s.roll_no
        }
        for s in students
    ])

@teacher_bp.route("/classes", methods=["GET"])
@require_role(["teacher"])
def get_teacher_classes():
    """
    Teacher: Fetch classes assigned to the logged-in teacher
    """
    teacher_id = g.user_id

    classes = Class.query.filter_by(teacher_id=teacher_id).all()

    return jsonify([
        {
            "id": str(c.id),
            "class_name": c.class_name
        }
        for c in classes
    ])
