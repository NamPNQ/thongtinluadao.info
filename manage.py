from flask.ext.script import Manager, Shell

from app import app
import models
from models import db


def _make_context():
    return dict(app=app, db=db, models=models)

manager = Manager(app)
manager.add_command("shell", Shell(make_context=_make_context))

if __name__ == "__main__":
    manager.run()
