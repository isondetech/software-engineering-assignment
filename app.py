from flask import (
    Flask,
    render_template
)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("events.html")

@app.route("/admin-dashboard")
def admin_dashboard():
    return "<h1>Admin Page</h1>"

@app.route("/add-event")
def add_event():
    return render_template("add_event.html")