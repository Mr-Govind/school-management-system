from flask import Blueprint, request, jsonify
from datetime import date
from sqlalchemy import and_

from app import db
from app.models.attendance import Attendance
from app.models.students import Student
from app.services.security import require_role

attendance_bp = Blueprint("attendance", __name__)

# --------------------------------------------------
# MARK ATTENDANCE (TEACHER ONLY)
# --------------------------------------------------
@attendance_bp.route("/mark", methods=["POST"])
def mark_attendance():
    # ---- SECURITY CHECK ----
    user_id = request.headers.get("X-User-Id")
    user, error = require_role(user_id, ["teacher"])
    if error:
        return jsonify({"error": error[0]}), error[1]

    # ---- REQUEST DATA ----
    data = request.get_json(force=True)

    student_id = data.get("student_id")
    status = data.get("status")
    att_date = data.get("date")  # optional (YYYY-MM-DD)

    # ---- VALIDATION ----
    if not student_id or not status:
        return jsonify({
            "error": "student_id and status are required"
        }), 400

    if status not in ["present", "absent"]:
        return jsonify({
            "error": "status must be 'present' or 'absent'"
        }), 400

    # ---- STUDENT CHECK ----
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    # ---- DATE HANDLING ----
    attendance_date = att_date if att_date else date.today()

    # ---- DUPLICATE CHECK (IMPORTANT) ----
    existing = Attendance.query.filter(
        and_(
            Attendance.student_id == student_id,
            Attendance.date == attendance_date
        )
    ).first()

    if existing:
        return jsonify({
            "error": "Attendance already marked for this student on this date"
        }), 409

    # ---- CREATE ATTENDANCE ----
    attendance = Attendance(
        student_id=student_id,
        date=attendance_date,
        status=status,
        marked_by=user.id
    )

    db.session.add(attendance)
    db.session.commit()

    return jsonify({
        "message": "Attendance marked successfully",
        "attendance": {
            "id": str(attendance.id),
            "student_id": str(attendance.student_id),
            "date": str(attendance.date),
            "status": attendance.status,
            "marked_by": str(attendance.marked_by)
        }
    }), 201


# --------------------------------------------------
# VIEW ATTENDANCE BY STUDENT (ADMIN / TEACHER)
# --------------------------------------------------
@attendance_bp.route("/student/<student_id>", methods=["GET"])
def attendance_by_student(student_id):
    # ---- SECURITY CHECK ----
    user_id = request.headers.get("X-User-Id")
    user, error = require_role(user_id, ["admin", "teacher"])
    if error:
        return jsonify({"error": error[0]}), error[1]

    records = Attendance.query.filter_by(student_id=student_id).order_by(
        Attendance.date.desc()
    ).all()

    return jsonify([
        {
            "id": str(r.id),
            "date": str(r.date),
            "status": r.status,
            "marked_by": str(r.marked_by)
        }
        for r in records
    ])
