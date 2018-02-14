from . import blog
from flask import render_template
from jinja2 import TemplateNotFound
from .inject.iNoteBlogContext import iNoteBlogContext


@blog.errorhandler(404)
def not_found():
    return 'not found'


@iNoteBlogContext.register_enter_event
def test(ctx):
    ctx['test'] = 1


@blog.route('/', methods=['get'], subdomain='<subdomain>.blog')
@blog.route('/', methods=['get'], subdomain='blog')
@iNoteBlogContext.warp_inote_blog_ctx('inote_blog_ctx')
def default(inote_blog_ctx, subdomain='default'):
    # print(inote_blog_context)
    try:
        return render_template(subdomain + '/index.html', username=subdomain, inote_blog_ctx=inote_blog_ctx)
    except TemplateNotFound:
        return render_template('default' + '/index.html', username=subdomain)


@iNoteBlogContext.warp_inote_blog_ctx('inote_blog_ctx')
@blog.route('/', methods=['get'], subdomain='blog')
@blog.route('/<string:sub_url>', methods=['get'])
def index(inote_blog_ctx, sub_url='default'):
    try:
        return render_template(sub_url + '/index.html', username=sub_url)
    except TemplateNotFound:
        return render_template('default' + '/index.html', username=sub_url)
