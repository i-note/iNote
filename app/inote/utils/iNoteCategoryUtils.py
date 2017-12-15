from flask_login import current_user
from flask import jsonify,request,abort
from app.models import User,NoteCategory,db
from flask_babel import gettext as _

class iNoteCategoryUtil:

    @staticmethod
    def getCategoriesFromRoot(cate):
        # {"title": "Folder 2", "key": 2, "children": [
        ret = {"title":cate.name,"key":cate.id }
        if cate.name == 'crash' or cate.name == 'root':
            ret['title'] = _(cate.name)
        children = cate.children.all()
        if len(children) > 0:
            children_list = []
            for item in children:
                list = iNoteCategoryUtil.getCategoriesFromRoot(item)
                children_list.append(list)
            ret['children']=children_list
        return ret

    @staticmethod
    def getCategoryFromParent(cate):
        children_list = []
        children = cate.children.all()
        if len(children) > 0:
            for item in children:
                node = {'title':item.name,'key':item.id}
                list = iNoteCategoryUtil.getCategoryFromParent(item)
                if list != []:
                    node['children'] = list
                children_list.append(node)
        return children_list

    @staticmethod
    def init():
        root_cate = NoteCategory(name='root')
        root_cate.user = current_user
        db.session.add(root_cate)

        crash_cate = NoteCategory(name='crash')
        crash_cate.user = current_user
        db.session.add(crash_cate)

        db.session.commit()

    @staticmethod
    def post():
        ''' post format
        request:
        {
            int(parent_cate_id):description('parent_cate_id'),
            str(new_cate_title):description('node new_cate_title')
        }
        response:
        {
            id:int()
        }
        '''

        json = request.get_json()
        parent = NoteCategory.query.filter_by(id=int(json['parent_cate_id'])).first()

        child = NoteCategory(name=json['new_cate_title'])
        child.parent = parent
        child.user = current_user
        db.session.add(child)
        db.session.commit()
        return jsonify({'id':child.id})
    @staticmethod
    def delete():
        pass
    @staticmethod
    def get():
        id = int(request.args.get('id'))
        if int(id) == -1:
            categories = NoteCategory.query.filter_by(user_id=current_user.id,parent_id=None).all()
            root = []
            for x in categories:
                root.append(iNoteCategoryUtil.getCategoriesFromRoot(x))
            return jsonify(root)
        else:
            cate = NoteCategory.query.filter_by(id=id).first()
            if current_user.id == cate.user.id:
                return jsonify(iNoteCategoryUtil.getCategoryFromParent(cate))
            else:
                return jsonify([{'status':'permission denied'}])

    @staticmethod
    def put():
        json = request.get_json()
        if json['type'] == 'rename':
            cate = NoteCategory.query.filter_by(id=int(json['id'])).first()
            if cate is None:
                return jsonify({'status': 'resource not found'})
            if cate.user_id != current_user.id:
                return jsonify({'status':'permission denied'})
            elif cate.name == 'crash' or cate.name == 'root':
                return jsonify({'status': 'cannot changed'})
            else:
                cate.name = json['new_cate_title']
                db.session.commit()
                return jsonify({'status':'success'})

        if json['type'] == 'move to':
            current_cate_id = int(json['current_cate_id']);
            dest_parent_cate_id = int(json['dest_parent_cate_id']);
            current_cate = NoteCategory.query.filter_by(id=current_cate_id).first()
            dest_parent_cate = NoteCategory.query.filter_by(id=dest_parent_cate_id).first()

            if current_cate is None or (dest_parent_cate is None and dest_parent_cate_id != -1):
                #未找到节点
                return jsonify({'status': 'resource not found'})
            if current_cate.user_id != current_user.id or ( dest_parent_cate_id != -1 and dest_parent_cate.user_id != current_user.id):
                #跨用户操作
                return jsonify({'status':'permission denied'})
            if current_cate.name == 'crash' or  (dest_parent_cate_id != -1 and current_cate.name == 'root'):
                #回收站和默认根不能动
                return jsonify({'status': 'cannot changed'})
            if  dest_parent_cate_id != -1 and iNoteCategoryUtil.findCateHasOnProtoChains(dest_parent_cate,current_cate):
                #根节点移动到自身
                return jsonify({'status': 'cannot changed'})
            if  dest_parent_cate_id != -1 and current_cate == dest_parent_cate:
                #已就位
                return jsonify({'status': 'already on this pos'})
            if dest_parent_cate_id == -1:
                dest_parent_cate = None
            current_cate.parent = dest_parent_cate
            db.session.commit()
            return jsonify({'status':'success'})




    @staticmethod
    def findCateHasOnProtoChains(cate,protoChains):
        if cate is None or protoChains is None:
            return False
        if cate == protoChains:
            return True
        return iNoteCategoryUtil.findCateHasOnProtoChains(cate.parent,protoChains)