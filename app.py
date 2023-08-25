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

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events_manager.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key="Hey"
db = SQLAlchemy(app)

class Event(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    title = db.Column(db.String)

@app.route("/")
def hello_world():
    # select all event records from the Event table
    try:
        event_records = db.session.execute(db.select(Event).order_by(Event.id)).scalars().all()
    except Exception as e:
        app.logger.error("failed to retrieve event records: %s", e)

    for event in event_records:
        if event.date != "":
            event_date = datetime.strptime(event.date, '%Y-%m-%d')
            event.date = event_date.strftime("%a %d %b %Y")
   
    return render_template("events.html", events=event_records)

@app.route("/dashboard")
def admin_dashboard():
    return render_template("dashboard.html")

@app.route("/add-event", methods=["GET","POST"])
def add_event():
    if request.method == 'POST':
        new_event = Event(date=request.form["date"], title=request.form["title"])
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

@app.route("/delete-event")
def delete_event():
    return render_template("delete_event.html")

@app.route("/update-event")
def update_event():
    return render_template("update_event.html")