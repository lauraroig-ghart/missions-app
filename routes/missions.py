from flask import Blueprint

missions_bp = Blueprint("missions", __name__)


@missions_bp.route("/missions")
def missions():
    return "Pantalla de missions"