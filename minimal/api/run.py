#!/usr/bin/env python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SAFRSAPI
from logic_bank.logic_bank import LogicBank, Rule
from logic_bank.rule_bank.rule_bank import RuleBank

import sqlalchemy

db = SQLAlchemy()


class User(SAFRSBase, db.Model):
    """
        description: User description
    """

    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)


def create_api(app, HOST="localhost", PORT=5000, API_PREFIX=""):
    api = SAFRSAPI(app, host=HOST, port=PORT, prefix=API_PREFIX)
    api.expose_object(User)
    user = User(name="test", email="email@x.org")
    print("Starting API: http://{}:{}/{}".format(HOST, PORT, API_PREFIX))


def create_app(config_filename=None, host="localhost", port=5000):
    app = Flask("demo_app")
    app.config.update(SQLALCHEMY_DATABASE_URI="sqlite://", FLASK_DEBUG=True)

    rb = RuleBank()
    my_rules = rb.__str__()

    db.init_app(app)

    with app.app_context():
        db.create_all()
        create_api(app, host, port)

    import safrs
    from sqlalchemy.orm import Session, scoped_session

    approach = "Achim"  # https://stackoverflow.com/questions/21322158/event-listener-on-scoped-session
    if approach == "Achim":  # worked!
        # session: Session = safrs.DB.session
        session = safrs.DB.session
        db_session = db.session
        pass
    elif approach == "Thomas":
        session = db.session
    elif approach == "simple":
        from sqlalchemy.orm import scoped_session, sessionmaker
        session = scoped_session(sessionmaker())
    else:
        class SessionMakerAndBind(sqlalchemy.orm.sessionmaker):
            def __call__(self, **kw):
                if not metadata.is_bound():
                    bind_metadata()
                return super(SessionMakerAndBind, self).__call__(**kw)

        sessionmaker = SessionMakerAndBind(autoflush=False,
                                           autocommit=True, expire_on_commit=False)
        session = sqlalchemy.orm.scoped_session(sessionmaker)

    LogicBank.activate(session=session, activator=declare_logic)
    return app


def declare_logic():
    def test(row, old_row, logic_row):
        print('xx' * 2000)
        return False  # means we always fail

    Rule.constraint(validate=User,
                    error_msg="can't change user",
                    calling=test)


# LogicBank.activate(session=db.session, activator=declare_logic)

host = "localhost"
port = 5000
app = create_app(host=host, port=port)

if __name__ == "__main__":
    app.run(host=host, port=port)