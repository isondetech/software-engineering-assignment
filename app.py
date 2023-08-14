from flask import (
    Flask,
    render_template
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events_manager.db"

@app.route("/")
def hello_world():
    return render_template("events.html")

@app.route("/dashboard")
def admin_dashboard():
    return render_template("dashboard.html")

@app.route("/add-event", methods=["GET","POST"])
def add_event():
    return render_template("add_event.html")

@app.route("/delete-event")
def delete_event():
    return render_template("delete_event.html")

@app.route("/update-event")
def update_event():
    return render_template("update_event.html")