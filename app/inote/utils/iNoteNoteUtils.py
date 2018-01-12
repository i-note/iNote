from flask_login import current_user
from flask import jsonify,request,abort
from app.models import User,NoteCategory,db,Note,Tag
from flask_babel import gettext as _
from datetime import datetime

class iNoteNoteUtil:


    @staticmethod
    def put():
        ''' post format
        request:
        {
            int(cate_id):description(''),
            str(note_title):description('')
            str(note_content):description('')
            list(note_tags):description('dict("id","name")')
            str(note_editor)
        }
        response:
        {
            id:int()
        }
        '''
        json = request.get_json()
        cate = NoteCategory.query.filter_by(id=int(json['cate_id'])).first()

        note = Note(title=json['note_title'],content=json['note_content'],edit_type=json["note_editor"],last_modify_datetime=datetime.utcnow())
        note.category = cate
        note.user = current_user
        db.session.add(note)

        json_tags = json['note_use_tags']
        for t_name in json_tags:
            if t_name == '':
                continue
            tag = Tag.query.filter_by(name=t_name).first()
            if tag is not None:
                note.tags.append(tag)
            else:
                tag = Tag(name=t_name)
                db.session.add(tag)
                current_user.tags.append(tag)
                note.tags.append(tag)

        db.session.commit()
        return jsonify({'note_id':note.id})

    @staticmethod
    def delete():
        json = request.get_json()
        note = Note.query.filter_by(id=int(json['note_id'])).first()
        if note is not None:
            if note.user_id != current_user.id:
                return jsonify({'status': 'permission denied'})
            db.session.delete(note)
            db.session.commit()
            return jsonify({'status':'success'})
        return jsonify({'status':'resource not found'})

    @staticmethod
    def note2json(note):
        json = {'note_id':note.id,'note_title':note.title,'note_edit_type':note.edit_type,'note_content':note.content,'note_createtime':note.create_datetime,'note_modifytime':note.last_modify_datetime}
        tags = note.tags.all()
        tags_json = []
        for tag in tags:
            tags_json.append({'tag_id':tag.id,'tag_name':tag.name})
        json['tags'] = tags_json
        return json

    @staticmethod
    def get():
        id = int(request.args.get('note_id'))

        note = Note.query.filter_by(id=id).first()
        if current_user.id == note.user.id:
            ret_json = iNoteNoteUtil.note2json(note)
            return jsonify(ret_json)
        else:
            return jsonify([{'status':'permission denied'}])

    @staticmethod
    def post():
        json = request.get_json()

        if json['type'] == 'modify title':
            note = Note.query.filter_by(id=int(json['note_id'])).first()
            if note is None:
                return jsonify({'status': 'resource not found'})
            if note.user_id != current_user.id:
                return jsonify({'status':'permission denied'})
            else:
                note.name = json['new_note_title']
                db.session.commit()
                return jsonify({'status':'success'})

        if json['type'] == 'modify content':
            note = Note.query.filter_by(id=int(json['note_id'])).first()
            if note is None:
                return jsonify({'status': 'resource not found'})
            if note.user_id != current_user.id:
                return jsonify({'status':'permission denied'})
            else:
                note.name = json['new_note_content']
                db.session.commit()
                return jsonify({'status':'success'})

        if json['type'] == 'modify tags':
            note = Note.query.filter_by(id=int(json['note_id'])).first()
            json_tags = json['new_note_tags']

            if note is None:
                return jsonify({'status': 'resource not found'})
            if note.user_id != current_user.id:
                return jsonify({'status':'permission denied'})
            else:
                for t_name in json_tags:
                    tag = Tag.query.filter_by(name=t_name).first()
                    if tag is not None:
                        note.tags.append(tag)
                    else:
                        tag = Tag(name=t_name)
                        db.session.add(tag)
                        current_user.tags.append(tag)
                        note.tags.append(tag)
                db.session.commit()
                return jsonify({'status':'success'})

        if json['type'] == 'del tag':
            note = Note.query.filter_by(id=int(json['note_id'])).first()
            tag = Tag.query.filter_by(id=int(json['tag_id'])).first()
            if note is None or tag is None:
                return jsonify({'status': 'resource not found'})
            if note.user_id != current_user.id:
                return jsonify({'status':'permission denied'})
            else:
                note.tags.remove(tag)
                db.session.commit()
                return jsonify({'status':'success'})

        if json['type'] == 'query tags':
            note = Note.query.filter_by(id=int(json['note_id'])).first()
            if note is None:
                return jsonify({'status': 'resource not found'})
            if note.user_id != current_user.id:
                return jsonify({'status':'permission denied'})
            else:
                tags = note.tags.all()
                tags_json = []
                for tag in tags:
                    tags_json.append({'tag_id': tag.id, 'tag_name': tag.name})
                return jsonify(tags_json)

        if json['type'] == 'move to':
            cate_id = int(json['cate_id'])
            note_id = int(json['note_id'])
            current_cate = NoteCategory.query.filter_by(id=cate_id).first()
            note = Note.query.filter_by(id=note_id).first()

            if current_cate is None or (note is None ):
                #未找到节点
                return jsonify({'status': 'resource not found'})
            if current_cate.user_id != current_user.id or ( note.user_id != current_user.id):
                #跨用户操作
                return jsonify({'status':'permission denied'})

            if  note.category == current_cate:
                #已就位
                return jsonify({'status': 'already on this pos'})

            note.category = current_cate
            db.session.commit()
            return jsonify({'status':'success'})

