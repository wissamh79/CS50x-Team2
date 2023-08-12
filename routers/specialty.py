from flask import Blueprint, session, request, render_template, flash, redirect
from database import db

specialty_router = Blueprint(
    "specialty_router",
    __name__,
    static_folder="../static/",
    template_folder="../templates",
)



@specialty_router.route("/specialty/<specialty_name>")
def specialty_details(specialty_name):
    try:
        specialty = db.execute("SELECT * FROM specialty WHERE name=?;", specialty_name)[0]
    except:
        return render_template("404.html")
    doctor = db.execute(
        "SELECT name, phone, specialty, years_of_practice, description FROM Doctor JOIN doctors ON doctors_specialties.id = specialty.id WHERE specialty_name = ?;",
        specialty_name,
    )
   
    return render_template(
        "specialty.html", specialty=specialty, doctor=doctor
    )
