from flask import Blueprint, render_template, request, redirect, session
from database import db

general_router = Blueprint(
    "general_router",
    __name__,
    static_folder="../static/",
    template_folder="../templates/",
)


@general_router.get("/")
def index():
   
    specialties = db.execute("SELECT * FROM specialty ORDER BY name DESC LIMIT 10;")
   
    return render_template("user/index.html", specialties=specialties)
