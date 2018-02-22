from app.iNoteContext import INoteInject, InjectContext
from flask import request

blogIndex = INoteInject()

class userInfo(InjectContext):
    def __enter__(self):
        print('construct userInfo')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('destruct userInfo')

@blogIndex.inject_ctx_class
def ctx():
    return userInfo
