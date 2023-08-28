from flask import Blueprint, request, render_template, flash, redirect
from flask_session import Session
from database import db

user_router = Blueprint(
    "user_router",
    __name__,
    static_folder="../static/",
    template_folder="../templates",
)

@user_router.route("/user/<user_id>")
def user_profile(user_id):
    try:
        user = db.execute("SELECT * FROM users WHERE id = ?;", (user_id,)).fetchone()
        if user:
            return render_template("user_profile.html", user=user)
        else:
            flash("User not found", "error")
            return redirect("/")
    except:
        flash("Error retrieving user information", "error")
        return redirect("/")
    

