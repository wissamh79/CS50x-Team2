pytfrom flask import Blueprint, request, render_template
from flask_session import Session 
from database import db

doctor_router = Blueprint(
    "doctor_router",
    __name__,
    static_folder="../static/",
    template_folder="../templates",
)


@doctor_router.route("/doctor")
def doctor_details(page_number=1, page_size=20):
    page_number = int(request.args.get("page_number", 1))
    page_size = int(request.args.get("page_size", 20))
    offset = (page_number - 1) * page_size
    result = db.execute(
        "SELECT * FROM Doctor ORDER BY name  ;"
    )
    print(result)
    return render_template("doctors.html", doctor=result)


@doctor_router.route("/doctor/<doctor_details>")
def doctor_detail(doctor_details):
    try:
        doctor = db.execute("SELECT * FROM Doctor WHERE id=?;", doctor_details)[0]
    except:
        return render_template("404.html")
    doctors_info = db.execute(
        "SELECT name, phone, specialty, years_of_practice, description FROM Doctor JOIN doctors ON doctors_specialties.id = specialty.id WHERE doctor_details = ?;",
        doctor_details,
    )
    return render_template(
        "doctors.html", doctor=doctor, doctors_info=doctors_info
    )