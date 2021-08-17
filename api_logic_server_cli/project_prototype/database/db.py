from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import safrs

db = safrs.DB

Base: declarative_base = db.Model

session: Session = db.session

print("got session: " + str(session))


def remove_session():
    db.session.remove()
