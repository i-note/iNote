from . import inote
from flask import render_template,redirect,url_for



@inote.route('/',methods=['GET','POST'])
@inote.route('/index',methods=['GET','POST'])
def index():
    return render_template('index.html')