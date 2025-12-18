from flask import Blueprint, jsonify, g
from app.models.students import Student
from app.models.attendance import Attendance
from app.services.security import require_role

parent_bp = Blueprint("parent", __name__)


@parent_bp.route("/student/<student_id>", methods=["GET"])
@require_role("parent")
def view_student(student_id):
    student = Student.query.filter_by(
        id=student_id,
        parent_id=g.user_id
    ).first()

    if not student:
        return jsonify({"error": "Forbidden"}), 403

    return jsonify({
        "id": str(student.id),
        "full_name": student.full_name,
        "roll_no": student.roll_no,
        "class_id": str(student.class_id),
        "parent_name": student.parent_name,
        "parent_contact": student.parent_contact
    })


@parent_bp.route("/student/<student_id>/attendance", methods=["GET"])
@require_role("parent")
def view_attendance(student_id):
    # Optional safety check: ensure this student belongs to parent
    student = Student.query.filter_by(
        id=student_id,
        parent_id=g.user_id
    ).first()

    if not student:
        return jsonify({"error": "Forbidden"}), 403

    records = Attendance.query.filter_by(
        student_id=student_id
    ).order_by(Attendance.date.desc()).all()

    return jsonify([
        {
            "date": str(r.date),
            "status": r.status
        }
        for r in records
    ])


@parent_bp.route("/children", methods=["GET"])
@require_role("parent")
def my_children():
    students = Student.query.filter_by(
        parent_id=g.user_id
    ).all()

    return jsonify([{
        "id": str(s.id),
        "full_name": s.full_name,
        "roll_no": s.roll_no,
        "class_id": str(s.class_id)
    } for s in students])
