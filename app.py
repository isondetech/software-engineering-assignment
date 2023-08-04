from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/admin-dashboard")
def admin_dashboard():
    return "<h1>Admin Page</h1>"

@app.route("/add-event")
def add_event():
    pass