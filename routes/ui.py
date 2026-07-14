from flask import Blueprint, render_template

ui_bp = Blueprint("ui", __name__)


@ui_bp.route("/ui")
def ui():

    return render_template("ui.html")