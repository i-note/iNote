# /bin/python

class iNoteContext(dict):
    def __init__(self):
        pass

    def __enter__(self):
        for func in iNoteContext.__funcs__:
            func(ctx=self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self[item]

    @staticmethod
    def ctx_func_init():
        iNoteContext.__funcs__ = list()

    def warp_inote_blog_ctx(name='inote_blog_ctx'):
        def warpper(func):
            def create_ctx(*args, **kwargs):
                context = iNoteContext()
                context.name = name
                with context as ctx:
                    kwargs[name] = ctx
                    func(*args, **kwargs)

            return create_ctx

        return warpper

    def register_enter_event(func):
        iNoteContext.__funcs__.append(func)

        def register(*args, **argv):
            pass

        return register


class iNote(iNoteContext):
    pass


iNote.ctx_func_init()


@iNoteContext.register_enter_event
def a(ctx):
    ctx['a'] = 1


@iNoteContext.register_enter_event
def b(ctx):
    ctx['b'] = 2


@iNoteContext.register_enter_event
def c(ctx):
    ctx['c'] = 3


@iNoteContext.warp_inote_blog_ctx('inote_blog_ctx')
def b(inote_blog_ctx):
    print(inote_blog_ctx['a'])
    print(inote_blog_ctx['b'])
    print(inote_blog_ctx['c'])


b()

#
# print(dir(iNote))
