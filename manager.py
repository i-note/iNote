#!/usr/bin/env python
import os
from flask_script import Manager, Shell, Server
from app import create_app, db
from app.models import User, Role, NoteCategory, Note, Tag
from config import config

__config__ = os.getenv('INOTE_CONFIG') or 'lisuke-dev'
app = create_app(__config__)

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, NoteCategory=NoteCategory, Note=Note, Tag=Tag)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver", Server(host=config[__config__].host, port=config[__config__].port))

if __name__ == '__main__':
    manager.run()
