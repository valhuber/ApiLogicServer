from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import safrs
import logging

app_logger = logging.getLogger("api_logic_server_app")

db = safrs.DB

Base: declarative_base = db.Model

session: Session = db.session

app_logger.debug("database/db.py - got session: " + str(session))


def remove_session():
    db.session.remove()
