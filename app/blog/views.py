from . import blog
from flask import render_template, redirect
from jinja2 import TemplateNotFound
from .inject.BlogInject import blogIndex


@blog.errorhandler(404)
def not_found():
    try:
        return render_template(username + '/404.html', username=username)
    except TemplateNotFound:
        return render_template('default' + '/404.html', username=username)


@blog.route('/', methods=['get'], subdomain='<sub_url>.blog')
@blog.route('/<string:sub_url>', methods=['get'], subdomain='blog')
@blog.route('/', methods=['get'], subdomain='blog')
def prefix(sub_url='default'):
    return homepage(username=sub_url)


@blog.route('/', methods=['get'])
@blog.route('/<string:sub_url>', methods=['get'])
def suffix(sub_url='default'):
    return homepage(username=sub_url)

def homepage(username='default'):
    with blogIndex:
        try:
            return render_template(username + '/404.html', username=username)
        except TemplateNotFound:
            return render_template('default' + '/404.html', username=username)
