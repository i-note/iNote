from . import inote
from flask import render_template,redirect,url_for,request,jsonify
from app.auth.views import login_required
from flask_login import current_user

@inote.route('/',methods=['GET','POST'])
@inote.route('/index',methods=['GET','POST'])
@login_required
def index():
    print(request.get_json())
    return render_template('inote/inote.html')



from .utils.iNoteCategoryUtils import iNoteCategoryUtil

@inote.route('/category',methods=['GET','POST','PUT','DELETE'])
@login_required
def category():
    ''' inote category ajax api '''
    # src_json = request.get_json()
    # print('print json:',src_json)
    # if not request.is_xhr or src_json == None:
    #     return jsonify([])

    if request.method == 'GET':
        # GET, get data
        return iNoteCategoryUtil.get()

    elif request.method == 'POST':
        #POST, add data
        return iNoteCategoryUtil.post()

    elif request.method == 'PUT':
        #PUT, update data
        return iNoteCategoryUtil.put()

    elif request.method == 'DELETE':
        #DELETE,delete data
        return iNoteCategoryUtil.delete()


from .utils.iNoteNoteUtils import iNoteNoteUtil

@inote.route('/note',methods=['GET','POST','PUT','DELETE'])
@login_required
def note():

    if request.method == 'GET':
        # GET, get data
        return iNoteNoteUtil.get()

    elif request.method == 'POST':
        #POST, add data
        return iNoteNoteUtil.post()

    elif request.method == 'PUT':
        #PUT, update data
        return iNoteNoteUtil.put()

    elif request.method == 'DELETE':
        #DELETE,delete data
        return iNoteNoteUtil.delete()

from .utils.iNoteNoteListUtils import iNoteNoteListUtil

@inote.route('/notelist',methods=['GET'])
@login_required
def note_list():
    if request.method == 'GET':
        return iNoteNoteListUtil.get()
    if request.method == 'POST':
        return iNoteNoteListUtil.post()
    if request.method == 'PUT':
        return iNoteNoteListUtil.put()
    if request.method == 'DELETE':
        return iNoteNoteListUtil.delete()