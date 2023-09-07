from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class UsernameExists(Exception):
    pass

'''
initialise an event table obj
'''
def init_event_table(db):
    class Event(db.Model):
        id =  db.Column(db.Integer, primary_key=True)
        date = db.Column(db.String)
        title = db.Column(db.String)
    
    return Event

def init_user_table(db):
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String, unique=True)
        password = db.Column(db.String)
        is_admin = db.Column(db.Boolean)
    
    return User

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

def username_exists(user_table, username):
    user = get_user(user_table, username)
    if user:
        print(user.username)
        return True
    return False

def login_info_is_valid(user_table, form):
    user = get_user(user_table, form["username"])
    if not user or not check_password_hash(user.password, form["password"]):
        return False
    return True

def get_user(user_table, username):
    return user_table.query.filter_by(username=username).first()

'''
retrieve events from database
sort and format the data too
'''
def get_events(db, event_table):
    event_records = db.session.execute(db.select(event_table).order_by(event_table.id)).scalars().all()
    return sort_fmt_event_records(event_records)

'''
retrieve event from database
'''
def get_event(event_table, event_id, fmt_date=False):
    event = event_table.query.get_or_404(event_id)
    if fmt_date and event_table.date != "":
        event_date = datetime.strptime(event.date, '%Y-%m-%d')
        event.date = event_date.strftime("%a %d %b %Y")
    return event

'''
delete event from database
'''
def delete_event(db, event_table, event_id):
    event = get_event(event_table, event_id)
    db.session.delete(event)
    db.session.commit()

'''
update an event
'''
def update_event(db, event_table, event_id, new_data):
    event = get_event(event_table, event_id)
    event.date = new_data["date"]
    event.title = new_data["title"]
    db.session.commit()

'''
add event to database
'''
def add_event(db, event, new_data):
    new_event = event(date=new_data["date"], title=new_data["title"])  
    db.session.add(new_event)
    db.session.commit()

'''
convert string to datetime object
'''    
def get_date(obj):
    return datetime.strptime(obj.date, '%Y-%m-%d')

'''
format event date e.g. "Fri 11 Aug 2023"
'''
def fmt_event_records(events):
    for event in events:
        if event.date != "":
            event_date = datetime.strptime(event.date, '%Y-%m-%d')
            event.date = event_date.strftime("%a %d %b %Y")
    return events

'''
sort events by most recent event
'''
def sort_fmt_event_records(events):
    sorted_asc_list = sorted(events, key=get_date, reverse=True)
    return fmt_event_records(sorted_asc_list)