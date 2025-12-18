from flask import Blueprint, request, jsonify, g
from datetime import date
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.attendance import Attendance
from app.services.security import require_role

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/mark", methods=["POST"])
@require_role("teacher")
def mark_attendance():
    data = request.get_json()

    attendance = Attendance(
        student_id=data["student_id"],
        date=date.today(),
        status=data["status"],
        marked_by=g.user_id
    )

    db.session.add(attendance)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "Attendance already marked for this student today"
        }), 409

    return jsonify({"message": "Attendance marked successfully"}), 201


@attendance_bp.route("/student/<student_id>", methods=["GET"])
@require_role(["teacher", "parent", "admin"])
def attendance_by_student(student_id):
    records = Attendance.query.filter_by(
        student_id=student_id
    ).order_by(Attendance.date.desc()).all()

    return jsonify([
        {"date": str(r.date), "status": r.status}
        for r in records
    ])
