from flask import Blueprint, jsonify, g
from app.models.students import Student
from app.models.classes import Class
from app.models.user import User
from app.services.security import require_role

teacher_bp = Blueprint("teacher", __name__)

# -----------------------------------------
# Get students by class
# -----------------------------------------
@teacher_bp.route("/class/<uuid:class_id>/students", methods=["GET"])
@require_role(["teacher"])
def get_students_by_class(class_id):
    teacher_id = g.user_id

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


# -----------------------------------------
# Get teacher classes
# -----------------------------------------
@teacher_bp.route("/classes", methods=["GET"])
@require_role(["teacher"])
def get_teacher_classes():
    teacher_id = g.user_id

    classes = Class.query.filter_by(teacher_id=teacher_id).all()

    return jsonify([
        {
            "id": str(c.id),
            "class_name": c.class_name
        }
        for c in classes
    ])


# -----------------------------------------
# Get parents of teacher's students
# -----------------------------------------
@teacher_bp.route("/parents", methods=["GET"])
@require_role(["teacher"])
def get_teacher_parents():
    teacher_id = g.user_id

    # 1️⃣ Get teacher's classes
    class_ids = [
        c.id for c in Class.query.filter_by(teacher_id=teacher_id).all()
    ]

    if not class_ids:
        return jsonify([])

    # 2️⃣ Get students in those classes
    students = Student.query.filter(
        Student.class_id.in_(class_ids),
        Student.parent_id.isnot(None)
    ).all()

    parent_map = {}

    for s in students:
        parent = User.query.filter_by(
            id=s.parent_id,
            role="parent"
        ).first()

        if not parent:
            continue

        if parent.id not in parent_map:
            parent_map[parent.id] = {
                "id": str(parent.id),
                "full_name": parent.full_name,
                "email": parent.email,
                "children_count": 1
            }
        else:
            parent_map[parent.id]["children_count"] += 1

    return jsonify(list(parent_map.values()))
