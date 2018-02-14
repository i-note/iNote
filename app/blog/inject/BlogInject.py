from app.iNoteContext import INoteInject, InjectContext
from flask import request

blogIndex = INoteInject()


@blogIndex.inject_ctx_class
def ctx():
    class userInfo(InjectContext):
        def __enter__(self):
            print('test')

        def __exit__(self, exc_type, exc_val, exc_tb):
            print('test')

    return userInfo


@blogIndex.use_ctx
def use():
    pass


use()
