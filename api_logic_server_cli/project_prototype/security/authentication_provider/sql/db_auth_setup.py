import sqlalchemy as sqlalchemy
import models as models
from flask import Flask
import safrs

def create_app(config_filename=None, host="localhost"):
    app = Flask("demo_app")
    app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///" + 'authentication_db.sqlite',
                      SESSION_COOKIE_SAMESITE="Lax",  # <<--- Strict
                      SQLALCHEMY_BINDS={'admin': "sqlite:///" + 'authentication_db.sqlite'},
                      SECRET_KEY="Change me !!",
                      SQLALCHEMY_TRACK_MODIFICATIONS=False,
                      FLASK_DEBUG=True)
    db = safrs.DB
    db.init_app(app)
    with app.app_context():
        # db.create_all()
        # db.create_all(bind='admin')
        # create_admin_api(app, port=port, host=host)
        admin = db.session.query(models.User).filter_by(name="admin").one_or_none()
        if not admin:
            admin = models.User(name="admin")
            db.session.add(admin)
            sam = models.User(name='Sam')
            db.session.add(sam)
            c1 = models.User(name='Client1')
            db.session.add(c1)
            c2 = models.User(name='Client2')
            db.session.add(c2)
            tenant = models.Role(name='tenant')
            db.session.add(tenant)
            manager = models.Role(name='manager')
            db.session.add(manager)
            sa = models.Role(name='sa')
            db.session.add(sa)
            dev = models.Role(name='dev')
            db.session.add(dev)

            sam_dev = models.UserRole()
            sam_dev.user_id = sam.id
            sam_dev.role_id = dev.id
            db.session.add(sam_dev)

            db.session.commit()

            read_sam = db.session.query(models.User).filter(models.User.name == "Sam").one()
            print(f'Read Sam: {read_sam}')

        # db.session.commit()

    return app

host = "localhost"
port = 5656
app = create_app(host=host)

if __name__ == "__main__":
    app.run(host=host)

