from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for
)
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    logout_user,
    login_required
)
from flask_sqlalchemy import SQLAlchemy
from helpers import db_manager
from helpers.db_manager import UsernameExists

# App configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events_manager.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key="Hey"
db = SQLAlchemy(app, session_options={"autoflush": False})
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = "unsuccess"
login_manager.init_app(app)

event_table = db_manager.init_event_table(db)
user_table = db_manager.init_user_table(db)

@login_manager.user_loader
def load_user(user_id):
    return user_table.query.get(int(user_id))

'''
Passes the user's data to all the html templates
'''
@app.context_processor
def inject_user():
    return dict(user=current_user)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        try:
            db_manager.add_user(db, user_table, request.form)
        except UsernameExists as e:
            flash(f"{e}", "unsuccess")
            app.logger.error(f"failed to add user: {e}")
            return redirect(url_for("register"))
        except Exception as e:
            flash("Failed to register", "unsuccess")
            app.logger.error(f"failed to add user: {e}")
            return redirect(url_for("register"))
        else:
            flash("Registration successful!", "success")
            return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        if not db_manager.login_info_is_valid(user_table, request.form):
            flash("Please check your login details and try again", "unsuccess")
            app.logger.info("failed to login user")
            return redirect(url_for("login"))

        login_user(db_manager.get_user(user_table, request.form["username"]))
        return redirect(url_for("events"))
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/")
@login_required
def events():
    # select all event records from the Event table
    # log any error if they occur
    try:
        event_records = db_manager.get_events(db, event_table)
    except Exception as e:
        app.logger.error(f"failed to retrieve event records: {e}")
   
    return render_template("events.html", events=event_records)

@app.route("/dashboard")
@login_required
def admin_dashboard():
    # Retrieve all events from the Event table
    try:
        event_records = db_manager.get_events(db, event_table)
    except Exception as e:
        app.logger.error(f"failed to retrieve event records: {e}")
    
    return render_template("dashboard.html", events=event_records)

@app.route("/add-event", methods=["GET","POST"])
@login_required
def add_event():
    # Add new event
    # If process succeeded, feedback to user, vice versa
    if request.method == 'POST':
        try:
            db_manager.add_event(db, event_table, request.form)
        except Exception as e:
            flash(f"Failed to add event, try again", "unsuccess")
            app.logger.error(f"failed to add event: {e}")
            return redirect(url_for("add_event"))
        else:
            flash("Event added successfully!", "success")
            return redirect(url_for("add_event"))
    return render_template("add_event.html")

@app.route("/delete-event/<int:event_id>", methods=["GET","POST"])
@login_required
def delete_event(event_id):
    # retrieve event from table
    event_record = db_manager.get_event(event_table, event_id, fmt_date=True)

    # delete event, give feedback to user 
    # if process succeeded or not.
    # Log any errors
    if request.method == 'POST':
        try:
            db_manager.delete_event(db, event_table, event_id)
        except Exception as e:
            flash(f"Failed to delete event", "unsuccess")
            app.logger.error(f"failed to delete event: {e}")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Event deleted successfully!", "success")
            return redirect(url_for("admin_dashboard"))

    return render_template("delete_event.html", event=event_record)

@app.route("/update-event/<int:event_id>", methods=["GET","POST"])
@login_required
def update_event(event_id):
    # retrieve event from table
    # used for rendering event data
    event_record = db_manager.get_event(event_table, event_id)

    # update event, give feedback to user 
    # if process succeeded or not.
    # Log any errors
    if request.method == 'POST':
        try:
            db_manager.update_event(db, event_table, event_id, request.form)
        except Exception as e:
            flash(f"Failed to update event", "unsuccess")
            app.logger.error(f"failed to update event: {e}")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Event updated successfully!", "success")
            return redirect(url_for("admin_dashboard"))

    return render_template("update_event.html", event=event_record)