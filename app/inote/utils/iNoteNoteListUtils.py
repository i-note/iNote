from flask_login import current_user
from flask import jsonify,request,abort
from app.models import User,NoteCategory,db,Note
from flask_babel import gettext as _
from .iNoteNoteUtils import iNoteNoteUtil
class iNoteNoteListUtil:

    @staticmethod
    def getNoteListFromCategory(cate):
        children_list = []
        children = cate.children.all()
        if len(children) > 0:
            for item in children:
                node = {'title':item.name,'key':item.id}
                list = iNoteNoteListUtil.getNoteListFromCategory(item)
                if list != []:
                    node['children'] = list
                children_list.append(node)
        return children_list


    @staticmethod
    def get():
        cate_id = int(request.args.get('cate_id'))

        ret_json = []
        if cate_id == -1:
            # -1 news
            newsNotes = Note.query.filter_by(user_id=current_user.id).order_by(Note.last_modify_datetime.desc()).limit(10).all()

            for note in newsNotes:
                ret_json.append(iNoteNoteUtil.note2json(note))
            return jsonify(ret_json)
        else:
            cate = NoteCategory.query.filter_by(id=cate_id).first()
            if current_user.id == cate.user.id:
                notes = cate.notes.all()
                for note in notes:
                    ret_json.append(iNoteNoteUtil.note2json(note))
                return jsonify(ret_json)
            else:
                return jsonify([{'status':'permission denied'}])


    @staticmethod
    def post():
        pass

    @staticmethod
    def delete():
        pass

    @staticmethod
    def put():
        pass
