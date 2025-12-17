from flask import Blueprint, jsonify
from app.models.students import Student
from app.models.attendance import Attendance
from app.services.security import require_role

parent_bp = Blueprint("parent", __name__)


@parent_bp.route("/student/<student_id>", methods=["GET"])
def view_student(student_id):
    user, error = require_role(["parent"])
    if error:
        return jsonify({"error": error[0]}), error[1]

    student = Student.query.filter_by(id=student_id, parent_id=user.id).first()

    if not student:
        return {"error": "Forbidden"}, 403


    return jsonify({
        "id": str(student.id),
        "full_name": student.full_name,
        "roll_no": student.roll_no,
        "class_id": str(student.class_id),
        "parent_name": student.parent_name,
        "parent_contact": student.parent_contact
    })


@parent_bp.route("/student/<student_id>/attendance", methods=["GET"])
def view_attendance(student_id):
    user, error = require_role(["parent"])
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


@parent_bp.route("/children", methods=["GET"])
def my_children():
    user, error = require_role(["parent"])
    if error:
        return {"error": error[0]}, error[1]

    students = Student.query.filter_by(parent_id=user.id).all()

    return [{
        "id": str(s.id),
        "full_name": s.full_name,
        "roll_no": s.roll_no,
        "class_id": str(s.class_id)
    } for s in students]
