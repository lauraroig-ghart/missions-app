from flask import Blueprint, render_template, session, redirect, url_for

from database import get_user, get_waiting_validations

admin_bp = Blueprint("admin", __name__)


@admin_bp.get("/admin")
def admin():

    #if "user_id" not in session:
    #    return redirect(url_for("auth.login"))

    #user = get_user(session["user_id"])

    waiting = get_waiting_validations()

    return render_template(
        "admin.html",
        #user=user,
        waiting=waiting
    )