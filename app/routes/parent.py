from flask import Blueprint, request, jsonify
from app.models.students import Student
from app.models.attendance import Attendance
from app.services.security import require_role

parent_bp = Blueprint("parent", __name__)


# -------------------------
# VIEW STUDENT PROFILE
# -------------------------
@parent_bp.route("/student/<student_id>", methods=["GET"])
def view_student(student_id):
    user_id = request.headers.get("X-User-Id")
    user, error = require_role(user_id, ["parent"])
    if error:
        return jsonify({"error": error[0]}), error[1]

    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "id": str(student.id),
        "full_name": student.full_name,
        "roll_no": student.roll_no,
        "class_id": str(student.class_id),
        "parent_name": student.parent_name,
        "parent_contact": student.parent_contact
    })


# -------------------------
# VIEW ATTENDANCE (READ-ONLY)
# -------------------------
@parent_bp.route("/student/<student_id>/attendance", methods=["GET"])
def view_attendance(student_id):
    user_id = request.headers.get("X-User-Id")
    user, error = require_role(user_id, ["parent"])
    if error:
        return jsonify({"error": error[0]}), error[1]

    records = Attendance.query.filter_by(student_id=student_id).order_by(
        Attendance.date.desc()
    ).all()

    return jsonify([
        {
            "date": str(r.date),
            "status": r.status
        }
        for r in records
    ])
