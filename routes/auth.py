from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

from flask import Blueprint, render_template, redirect, session, url_for

from database import query_one

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login")
def login():

    users = query_one("""
        SELECT COUNT(*) AS total
        FROM users
    """)

    if not users or users["total"] == 0:
        return "No hi ha usuaris a la base de dades."

    from database import query

    users = query("""
        SELECT *
        FROM users
        ORDER BY role,name
    """)

    return render_template(
        "login.html",
        users=users
    )


@auth_bp.route("/login/<username>")
def login_user(username):

    user = query_one("""
        SELECT *
        FROM users
        WHERE LOWER(name)=LOWER(?)
    """, (username,))

    if not user:
        return redirect(url_for("auth.login"))

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["role"] = user["role"]

    return redirect(url_for("dashboard.dashboard"))


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))