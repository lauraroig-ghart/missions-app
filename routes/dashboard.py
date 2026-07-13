from flask import Blueprint, render_template, session, redirect, url_for

from database import get_user, get_user_missions

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    # Comprovar si hi ha sessió
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = get_user(session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    missions = get_user_missions(user["id"])

    total_missions = len(missions)
    total_points = user["points"]

    return render_template(
        "dashboard.html",
        user=user,
        missions=missions,
        total_missions=total_missions,
        total_points=total_points
    )