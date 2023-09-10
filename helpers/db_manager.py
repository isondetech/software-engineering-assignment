from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# A custom 'username exists' error
class UsernameExists(Exception):
    pass

'''
The EventObject class is designed to store and structure 
event data retrieved from a database. It was created as a
way to store the 'last_updated_by' foreign key (user Id) field 
as a string (username)
'''
class EventObject():
    def __init__(self, id, date, title, last_updated_by):
        self.id = id
        self.date = date
        self.title = title
        self.last_updated_by = last_updated_by

'''
This function creates an SQLAlchemy Model class called "Event"
The "Event" class can be used to interact with the Event table
in the database.
'''
def init_event_table(db):
    class Event(db.Model):
        id =  db.Column(db.Integer, primary_key=True)
        date = db.Column(db.String)
        title = db.Column(db.String(17))
        last_updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
        user = db.relationship("User", backref='user', lazy=True, uselist=False)

    return Event

'''
This function creates an SQLAlchemy Model class called "User"
The "User" class can be used to interact with the User table
in the database.
'''
def init_user_table(db):
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String, unique=True)
        password = db.Column(db.String)
        is_admin = db.Column(db.Boolean)
    
    return User

'''
This function adds a user to the database.
It raises the "UsernameExists" error if a username exists.
'''
def add_user(db, user_table, new_data):
    if username_exists(user_table, new_data["username"]):
        raise UsernameExists(f"The username {new_data['username']} already exists")

    new_user = user_table(
        username=new_data["username"],
        password=generate_password_hash(new_data["password"],method="scrypt"),
        is_admin=False
    )
    db.session.add(new_user)
    db.session.commit()

'''
This function checks if a username exists in the database.
It returns "True" if it does and "False" if it doesn't.
'''
def username_exists(user_table, username):
    user = get_user(user_table, username)
    if user:
        return True
    return False

'''
This function validates login info.
It checks that the login info provided is present 
in the database and matches appropriately.
'''
def login_info_is_valid(user_table, form):
    user = get_user(user_table, form["username"])
    if not user or not check_password_hash(user.password, form["password"]):
        return False
    return True

'''
This function retrieves a user from the database by
the user's username
'''
def get_user(user_table, username):
    return user_table.query.filter_by(username=username).first()

'''
This function retrieves events from the database.
It maps the event records to an 'EventObject' and converts
the user Id to the username of the user
It sorts the events by their date, ensuring the
most recent event appears first
It also formats the date
'''
def get_events(db, event_table, user_table):
    event_records = db.session.execute(db.select(event_table).order_by(event_table.id)).scalars().all()
    serialized_event_records = []
    for record in event_records:
        user = user_table.query.filter_by(id=record.last_updated_by).first()
        event_record = EventObject(
            record.id,
            record.date,
            record.title,
            user.username
        )
        serialized_event_records.append(event_record)
    return sort_fmt_event_records(serialized_event_records)

'''
This function retrieves an event from the database
It formats the date from the format 'YYYY-MM-DD' to 'Day DD Mon YYYY'
'''
def get_event(event_table, event_id, fmt_date=False):
    event = event_table.query.get_or_404(event_id)
    if fmt_date and event_table.date != "":
        event_date = datetime.strptime(event.date, '%Y-%m-%d')
        event.date = event_date.strftime("%a %d %b %Y")
    return event

'''
This function deletes an event from the database
'''
def delete_event(db, event_table, event_id):
    event = get_event(event_table, event_id)
    db.session.delete(event)
    db.session.commit()

'''
This funcion updates an event in the database
'''
def update_event(db, event_table, event_id, new_data, current_user):
    event = get_event(event_table, event_id)
    event.date = new_data["date"]
    event.title = new_data["title"]
    event.last_updated_by = current_user.id
    db.session.commit()

'''
This functiom adds an event to database
'''
def add_event(db, event, new_data, current_user):
    new_event = event(
        date=new_data["date"], 
        title=new_data["title"], 
        last_updated_by = current_user.id
    )  
    db.session.add(new_event)
    db.session.commit()

'''
This function converts an object's date property from
the datatype string to a datetime object
'''    
def get_date(obj):
    return datetime.strptime(obj.date, '%Y-%m-%d')

'''
This function formats the event date 
from 'YYYY-MM-DD' to 'Day DD Mon YYYY'
'''
def fmt_event_records(events):
    for event in events:
        if event.date != "":
            event_date = datetime.strptime(event.date, '%Y-%m-%d')
            event.date = event_date.strftime("%a %d %b %Y")
    return events

'''
This function sorts the events in descending order based on their date, 
ensuring that the most recent events appear first.
'''
def sort_fmt_event_records(events):
    sorted_asc_list = sorted(events, key=get_date, reverse=True)
    return fmt_event_records(sorted_asc_list)
