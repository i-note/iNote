from . import main
from flask import render_template
from flask_babel import gettext as _
from flask_login import login_required


@main.route('/', methods=['get', 'post'])
@main.route('/index', methods=['get', 'post'])
def index():
    return render_template('index.html')


@main.route('/secret')
@login_required
def secret():
    return _('Only authenticated users are allowed!')
