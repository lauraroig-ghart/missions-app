from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for,
)

from database import (
    get_user,
    get_user_missions,
    complete_mission,
    approve_mission, 
    reject_mission
)

missions_bp = Blueprint("missions", __name__)



@missions_bp.get("/missions")
def missions():
    print ("Sessió actual:", session)
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = get_user(session["user_id"])

    missions = get_user_missions(user["id"])

    return render_template(
        "missions.html",
        user=user,
        missions=missions
    )


@missions_bp.post("/mission/<int:assignment_id>/complete")
def complete(assignment_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    complete_mission(
        assignment_id,
        session["user_id"]
    )

    return redirect(url_for("dashboard.dashboard"))

@missions_bp.post("/admin/mission/<int:assignment_id>/approve")
def approve(assignment_id):
    
    # Aquí crides a la funció que fa el canvi a la BD (aprovar)
    approve_mission(assignment_id)
    
    return redirect(url_for("admin.admin")) # Torna a la pàgina d'admin

@missions_bp.post("/admin/mission/<int:assignment_id>/reject")
def reject(assignment_id):
     
    # Aquí crides a la funció que fa el canvi a la BD (rebutjar)
    reject_mission(assignment_id)
    
    return redirect(url_for("admin.admin"))