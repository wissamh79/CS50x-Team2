from flask import Flask
from flask_session import Session
from routers.general import general_router
from routers.specialty import specialty_router
from routers.users import user_router
from routers.doctor import doctor_router
from routers.admin_panel import admin_router
from routers.account import account_router

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

app.register_blueprint(general_router, url_prefix="")
app.register_blueprint(account_router, url_prefix="")
app.register_blueprint(user_router, url_prefix="")
app.register_blueprint(specialty_router, url_prefix="")
app.register_blueprint(doctor_router, url_prefix="")
app.register_blueprint(admin_router, url_prefix="/admin")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5500)
