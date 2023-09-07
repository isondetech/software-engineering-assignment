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

# Database configuration
db = SQLAlchemy(app, session_options={"autoflush": False})

# Login manager configuration
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = "unsuccess"
login_manager.init_app(app)

# Database tables
event_table = db_manager.init_event_table(db)
user_table = db_manager.init_user_table(db)

# Load user
@login_manager.user_loader
def load_user(user_id):
    return user_table.query.get(int(user_id))

# Passes the user's data to all the html templates
@app.context_processor
def inject_user():
    return dict(user=current_user)

'''
This route handles user registration.
It attempts to add a user to the database and logs any error that occur
during the process. If the registration process is successful or unsuccessful
it alerts the user.
'''
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

'''
This route handles user login.
It validates the user login info from the database and logs the user in,
it logs any error that occur during the process. If the login process
is unsuccessful it alerts the user.
'''
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

'''
This route handles user logout.
It logs out a user and redirects them to the login page
'''
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

'''
This route handles the main events page.
Only authenticated users can access this page. It attempts to retrieve event
records from the database. If an error occurs during the retrieval, it logs
the error message.
'''
@app.route("/")
@login_required
def events():
    try:
        event_records = db_manager.get_events(db, event_table)
    except Exception as e:
        app.logger.error(f"failed to retrieve event records: {e}")
   
    return render_template("events.html", events=event_records)

'''
This route handles the dashboard page.
Only authenticated users can access this page. It attempts to retrieve event
records from the database. If an error occurs during the retrieval, it logs
the error message.
'''
@app.route("/dashboard")
@login_required
def dashboard():
    try:
        event_records = db_manager.get_events(db, event_table)
    except Exception as e:
        app.logger.error(f"failed to retrieve event records: {e}")
    
    return render_template("dashboard.html", events=event_records)

'''
This route handles the adding of events.
Only authenticated users can access this page. It attempts to add an event
to the database. If an error occurs during the process, it logs
the error message and alerts the user. If the additon is successful it also
alerts the user.
'''
@app.route("/add-event", methods=["GET","POST"])
@login_required
def add_event():
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

'''
This route handles the deleting of events.
Only authenticated and privileged (admin) users can access this page. 
It redirects any non-admin users back and informs the they're not 
authorised to access the page. 
It attempts to delete an event from the database. If an error occurs
during the deletion, it logs the error message and alerts the user.
If the deletion is successful it also alerts the user.
'''
@app.route("/delete-event/<int:event_id>", methods=["GET","POST"])
@login_required
def delete_event(event_id):
    if not current_user.is_admin:
        flash(f"You're not authorized to delete", "unsuccess")
        app.logger.error(f"User {current_user.username} attempted to delete event")
        return redirect(url_for("dashboard"))

    event_record = db_manager.get_event(event_table, event_id, fmt_date=True)

    if request.method == 'POST':
        try:
            db_manager.delete_event(db, event_table, event_id)
        except Exception as e:
            flash(f"Failed to delete event", "unsuccess")
            app.logger.error(f"failed to delete event: {e}")
            return redirect(url_for("dashboard"))
        else:
            flash("Event deleted successfully!", "success")
            return redirect(url_for("dashboard"))

    return render_template("delete_event.html", event=event_record)

'''
This route handles the updatinf of events.
Only authenticated users can access this page. It attempts to update an event
to the database. If an error occurs during the process, it logs the error 
message and alerts the user. If the process is successful it also
alerts the user.
'''
@app.route("/update-event/<int:event_id>", methods=["GET","POST"])
@login_required
def update_event(event_id):
    event_record = db_manager.get_event(event_table, event_id)

    if request.method == 'POST':
        try:
            db_manager.update_event(db, event_table, event_id, request.form)
        except Exception as e:
            flash(f"Failed to update event", "unsuccess")
            app.logger.error(f"failed to update event: {e}")
            return redirect(url_for("dashboard"))
        else:
            flash("Event updated successfully!", "success")
            return redirect(url_for("dashboard"))

    return render_template("update_event.html", event=event_record)