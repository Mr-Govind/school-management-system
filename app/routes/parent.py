from flask import Blueprint

parent_bp = Blueprint("parent", __name__)

@parent_bp.route("/")
def parent_home():
    return "Parent Dashboard Route"
