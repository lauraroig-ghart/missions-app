from flask import Blueprint, render_template, session, redirect, url_for
from datetime import datetime

from database import get_user, get_user_missions, count_waiting_validations,  get_waiting_validations

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = get_user(session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    missions = get_user_missions(user["id"])

    pending_missions = [
        m for m in missions
        if m["status"] == "pending"
    ]

    waiting_missions = [
        m for m in missions
        if m["status"] == "waiting_validation"
    ]

    total_missions = len(missions)
    total_points = user["points"]

    waiting_count = 0

    if user["role"] == "admin":
        waiting_count = count_waiting_validations()

    waiting = []

    if user["role"] == "admin":
        waiting = get_waiting_validations()


    for mission in waiting:

        completed = datetime.strptime(
            mission["completed_at"],
            "%Y-%m-%d %H:%M:%S"
        )

        delta = datetime.now() - completed

        if delta.days > 0:
            mission["time_ago"] = f"fa {delta.days} dies"
        elif delta.seconds >= 3600:
            mission["time_ago"] = f"fa {delta.seconds//3600} h"
        elif delta.seconds >= 60:
            mission["time_ago"] = f"fa {delta.seconds//60} min"
        else:
            mission["time_ago"] = "ara mateix"

        mission["completed_date"] = completed.strftime("%d/%m/%Y %H:%M")

    
    completed_missions = [
        m for m in missions
        if m["status"] == "completed"
    ]


    return render_template(
        "dashboard.html",
        user=user,
        missions=missions,
        pending_missions=pending_missions,
        waiting_missions=waiting_missions,
        total_missions=total_missions,
        total_points=total_points,
        waiting_count=waiting_count,
        completed_missions=completed_missions,
        waiting=waiting

    )