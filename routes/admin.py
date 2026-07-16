
from flask import Blueprint, render_template, session, redirect, url_for, request
from config import Config

ADMIN_PIN = Config.ADMIN_PIN

from database import get_user, get_waiting_validations, approve_mission, reject_mission


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin", methods=["GET", "POST"])
def admin():
    print("ENTRO ADMIN")
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = get_user(session["user_id"])

    print("USER:", user)

    # Només administradors
    if user["role"] != "admin":
        return redirect(url_for("dashboard.dashboard"))


    # Demanar PIN si encara no està validat
    if not session.get("admin_verified"):

        print("HA D'ENSENYAR PIN")
        if request.method == "POST":

            pin = request.form.get("pin")

            if pin == Config.ADMIN_PIN:

                session["admin_verified"] = True

                return redirect(url_for("admin.admin"))


        return render_template("admin_pin.html")


    waiting = get_waiting_validations()


    return render_template(
        "admin.html",
        user=user,
        waiting=waiting
    )

@admin_bp.post("/admin/mission/<int:assignment_id>/approve")
def approve(assignment_id):
    if "user_id" not in session:
            return redirect(url_for("auth.login"))

    user = get_user(session["user_id"])

    if user["role"] != "admin":
        return redirect(url_for("dashboard.dashboard"))
    
    approve_mission(assignment_id, session["user_id"])

    return redirect(url_for("admin.admin"))



@admin_bp.post("/admin/mission/<int:assignment_id>/reject")
def reject(assignment_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = get_user(session["user_id"])

    if user["role"] != "admin":
        return redirect(url_for("dashboard.dashboard"))

    reject_mission(assignment_id)

    return redirect(url_for("admin.admin"))