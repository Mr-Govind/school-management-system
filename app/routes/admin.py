from flask import Blueprint, request, jsonify
from app.models.classes import Class
from app.models.students import Student
from app.models.user import User
from app import db
from app.services.security import require_role







admin_bp = Blueprint("admin", __name__)






@admin_bp.route("/students/<student_id>/assign-parent", methods=["POST"])
def assign_parent(student_id):
    user, error = require_role(["admin"])
    if error:
        return {"error": error[0]}, error[1]

    data = request.get_json() or {}
    parent_id = data.get("parent_id")
    if not parent_id:
        return {"error": "parent_id required"}, 400

    student = Student.query.get(student_id)
    if not student:
        return {"error": "Student not found"}, 404

    student.parent_id = parent_id
    db.session.commit()

    return {"message": "Parent assigned successfully"}, 200

# -------------------------
# CREATE CLASS
# -------------------------
@admin_bp.route("/classes", methods=["POST"])
def create_class():
    data = request.get_json(force=True)

    class_name = data.get("class_name")
    if not class_name:
        return jsonify({"error": "class_name is required"}), 400

    new_class = Class(class_name=class_name)
    db.session.add(new_class)
    db.session.commit()

    return jsonify({
        "message": "Class created successfully",
        "class": {
            "id": str(new_class.id),
            "class_name": new_class.class_name,
            "teacher_id": None
        }
    }), 201


# -------------------------
# LIST CLASSES
# -------------------------
@admin_bp.route("/classes", methods=["GET"])
def list_classes():
    classes = Class.query.all()
    return jsonify([
        {
            "id": str(c.id),
            "class_name": c.class_name,
            "teacher_id": str(c.teacher_id) if c.teacher_id else None
        }
        for c in classes
    ])


# -------------------------
# ADD STUDENT
# -------------------------
@admin_bp.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(force=True)

    full_name = data.get("full_name")
    roll_no = data.get("roll_no")
    class_id = data.get("class_id")
    parent_name = data.get("parent_name")
    parent_contact = data.get("parent_contact")

    if not full_name or not roll_no or not class_id:
        return jsonify({
            "error": "full_name, roll_no, and class_id are required"
        }), 400

    class_obj = Class.query.get(class_id)
    if not class_obj:
        return jsonify({"error": "Class not found"}), 404

    student = Student(
        full_name=full_name,
        roll_no=roll_no,
        class_id=class_id,
        parent_name=parent_name,
        parent_contact=parent_contact
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student added successfully",
        "student": {
            "id": str(student.id),
            "full_name": student.full_name,
            "roll_no": student.roll_no,
            "class_id": str(student.class_id)
        }
    }), 201


# -------------------------
# LIST STUDENTS
# -------------------------
@admin_bp.route("/students", methods=["GET"])
def list_students():
    students = Student.query.all()
    return jsonify([
        {
            "id": str(s.id),
            "full_name": s.full_name,
            "roll_no": s.roll_no,
            "class_id": str(s.class_id)
        }
        for s in students
    ])

@admin_bp.route("/users", methods=["GET"])
def list_users():
    from app.models.user import User

    users = User.query.all()

    return jsonify([
        {
            "id": str(u.id),
            "full_name": u.full_name,
            "email": u.email,
            "role": u.role
        }
        for u in users
    ])
