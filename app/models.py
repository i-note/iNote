from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user,AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

class Permission:
    #关注其他用户
    FOLLOW = 0x01
    #在他人的文章中发布评论
    COMMENT=0x02
    #写原创文章
    WRITE_ARTICLES = 0x04
    #审查他人发表的不当评论
    MODERATE_COMMENTS = 0x08
    #管理网站
    ADMINISTER = 0x80

    @staticmethod
    def get_administer_perm():
        return Permission.ADMINISTER

    @staticmethod
    def get_user_perm():
        return Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES

    @staticmethod
    def get_moderator_perm():
        return Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENTS

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permission =db.Column(db.Integer)
    users = db.relationship('User',backref='role',lazy='dynamic')

    @staticmethod
    def init_roles():
    # init roles
        roles = {
            #具有发布文章、发表评论和关注其他用户的权限。这是新用户的默认角色
            'User': (Permission.get_user_perm(), True),
            #增加审查不当评论的权限
            'Moderator': (Permission.get_moderator_perm(), False),
            #具有所有权限，包括修改其他用户所属角色的权限
            'Administrator': (Permission.get_administer_perm(), False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

user_use_tags_relation = db.Table('user_use_tags_relation'
                         ,db.Column('user_id',db.Integer,db.ForeignKey('users.id'))
                         ,db.Column('tags_id',db.Integer,db.ForeignKey('tags.id')))

class User(UserMixin,db.Model):
    #
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    confirmed = db.Column(db.Boolean,default=False)

    def generate_confirmation_token(self,expiration=300):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'auth_token_confirm':self.id})

    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            print('auth_token error 0')
            return False
        if data.get('auth_token_confirm') != self.id:
            print('auth_token error 0')
            return False
        print('auth_token success')
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        current_user.confirmed = True
        return True

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            #
            if self.email == current_app.config['INOTE_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            #
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    # 外键关联
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    notes = db.relationship('Note', backref='users', lazy='dynamic')
    friendlinks = db.relationship('Friendlink', backref='users', lazy='dynamic')

    tags = db.relationship('Tag',
                           secondary=user_use_tags_relation,
                           backref=db.backref('users',lazy='dynamic'),
                           lazy='dynamic')


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True,index=True)

class NoteCategory(db.Model):
    __tablename__ = 'note_categories'
    id = db.Column(db.Integer,primary_key=True,index=True)
    name = db.Column(db.String(64),index=True)
    children_id = db.Column(db.Integer, db.ForeignKey('note_categories.id'),index=True)
    shared_status = db.Column(db.Integer)
    children = db.relationship('NoteCategory',backref='parent',remote_side='NoteCategory.id',lazy='dynamic',uselist=True)

    notes = db.relationship('Note',backref='category',lazy='dynamic')

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(128),index=True)
    edit_type = db.Column(db.Integer,nullable=False)
    content = db.Column(db.Text(),index=True)
    create_date = db.Column(db.DateTime,default=datetime.utcnow())
    last_modify_date = db.Column(db.DateTime,default=datetime.utcnow())
    note_category_id= db.Column(db.Integer, db.ForeignKey('note_categories.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer,primary_key=True)
    external = db.Column(db.Boolean,default=False)
    source = db.Column(db.Text(),index=True)

class Friendlink(db.Model):
    __tablename__ = 'friendlinks'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(32))
    url = db.Column(db.String(128))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
