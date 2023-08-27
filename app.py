from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
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
    # retrieve all events from the Event table
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
            flash(f"Failed to add event, try again", "unsuccess")
            app.logger.error("failed to add event: %s", e)
            return redirect(url_for("add_event"))
        else:
            flash("Event added successfully!", "success")
            return redirect(url_for("add_event"))
    return render_template("add_event.html")

@app.route("/delete-event/<int:event_id>", methods=["GET","POST"])
def delete_event(event_id):
    # retrieve event from table
    event_record = db_manager.get_event(event_table, event_id, fmt_date=True)

    # delete event, give feedback to user 
    # if process succeeded or not
    # log any errors
    if request.method == 'POST':
        try:
            db_manager.delete_event(db, event_table, event_id)
        except Exception as e:
            flash(f"Failed to delete event", "unsuccess")
            app.logger.error("failed to delete event: %s", e)
        else:
            flash("Event deleted successfully!", "success")
            return redirect(url_for("admin_dashboard"))

    return render_template("delete_event.html", event=event_record)

@app.route("/update-event/<int:event_id>", methods=["GET","POST"])
def update_event(event_id):
    event_record = db_manager.get_event(event_table, event_id)

    if request.method == 'POST':
        try:
            db_manager.update_event(db, event_table, event_id, request.form)
        except Exception as e:
            flash(f"Failed to update event", "unsuccess")
            app.logger.error("failed to update event: %s", e)
        else:
            flash("Event updated successfully!", "success")
            return redirect(url_for("admin_dashboard"))

    return render_template("update_event.html", event=event_record)