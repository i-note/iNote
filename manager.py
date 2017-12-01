#!/usr/bin/env python
import os
from flask_script import Manager, Shell
from app import create_app, db
from app.models import User,Role,NoteCategory

app = create_app(os.getenv('INOTE_CONFIG') or 'lisuke-dev')

manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db,User=User,Role=Role,NoteCategory=NoteCategory)
manager.add_command("shell", Shell(make_context=make_shell_context))



if __name__ == '__main__':
    manager.run()