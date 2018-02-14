#!/bin/python3
class InjectContext(dict):
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class INoteInject(dict):
    def __init__(self):
        self['inject_classes'] = dict()

    def __enter__(self):
        for sub_ctx in self['inject_classes'].keys():
            self['inject_classes'][sub_ctx].__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        for sub_ctx in reversed(list(self['inject_classes'].keys())):
            self['inject_classes'][sub_ctx].__exit__(exc_type, exc_val, exc_tb)

    def inject_ctx_class(self, func):
        ctx_class = func()
        if not issubclass(ctx_class, InjectContext):
            raise "inject_ctx_class: return class must be InjectContext's subclass"
        self['inject_classes'][ctx_class.__name__] = ctx_class()

        def warpper(*args, **kwargs):
            return func()

        return warpper

    def use_ctx(self, func):
        def warpper(*args, **kwargs):
            with self:
                func(*args, **kwargs)

        return warpper
        #
        # home = INoteInject()
        # index = INoteInject()
        # #
        #
        # @home.inject_ctx_class
        # def aaa():
        #     class aaa(InjectContext):
        #         def __enter__(self):
        #             print('enter: aaa')
        #         def __exit__(self, exc_type, exc_val, exc_tb):
        #             print('exit: aaa')
        #
        #     return aaa
        #
        # @index.inject_ctx_class
        # @home.inject_ctx_class
        # def bbb():
        #     class bbb(InjectContext):
        #         def __enter__(self):
        #             print('enter: bbb')
        #         def __exit__(self, exc_type, exc_val, exc_tb):
        #             print('exit: bbb')
        #
        #     return bbb
        #
        # @index.use_ctx
        # def test():
        #     print('test')
        #
        #
        # @home.use_ctx
        # def testb():
        #     print(111)
        # test()
        #
        # testb()
