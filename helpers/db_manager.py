from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

'''
initialise an event table obj
'''
def init_event_table(db):
    class Event(db.Model):
        id =  db.Column(db.Integer, primary_key=True)
        date = db.Column(db.String)
        title = db.Column(db.String)
    
    return Event

'''
retrieve events from database
sort and format the data too
'''
def get_events(db, event_table) -> list:
    event_records = db.session.execute(db.select(event_table).order_by(event_table.id)).scalars().all()
    return sort_fmt_event_records(event_records)

def get_event(event_table, id, fmt=False):
    event = event_table.query.get_or_404(id)
    if fmt and event_table.date != "":
        event_date = datetime.strptime(event.date, '%Y-%m-%d')
        event.date = event_date.strftime("%a %d %b %Y")
    return event

def delete_event(db, event_table, id):
    event = get_event(event_table, id)
    db.session.delete(event)
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