from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from helpers import db_manager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events_manager.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key="Hey"
db = SQLAlchemy(app)

event_table = db_manager.init_event_table(db)


@app.route("/")
def hello_world():
    # select all event records from the Event table
    # log any error if they occur
    try:
        event_records = db_manager.get_events(db, event_table)
    except Exception as e:
        app.logger.error("failed to retrieve event records: %s", e)
   
    return render_template("events.html", events=event_records)

@app.route("/dashboard")
def admin_dashboard():
    # select all event records from the Event table
    # log any error if they occur
    try:
        event_records = db_manager.get_events(db, event_table)
    except Exception as e:
        app.logger.error("failed to retrieve event records: %s", e)
    
    return render_template("dashboard.html", events=event_records)

@app.route("/add-event", methods=["GET","POST"])
def add_event():
    if request.method == 'POST':
        new_event = event_table(date=request.form["date"], title=request.form["title"])
        try:
            db.session.add(new_event)
            db.session.commit()
        except Exception as e:
            flash(f"Couldn't add event, try again", "unsuccess")
            app.logger.error("failed to add event: %s", e)
        else:
            flash("Event added successfully!", "success")
            return redirect(url_for("add_event"))
    return render_template("add_event.html")

@app.route("/delete-event/<int:id>")
def delete_event(id):
    return render_template("delete_event.html")

@app.route("/update-event")
def update_event():
    return render_template("update_event.html")