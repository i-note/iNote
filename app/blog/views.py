from . import blog
from flask import render_template,render_template_string
from jinja2 import TemplateNotFound





@blog.errorhandler(404)
def not_found():
    return 'not found'

@blog.route('/',methods=['get'],subdomain='<subdomain>.blog')
def default(subdomain='default'):

    try:
        return render_template(subdomain+'/index.html',username=subdomain)
    except TemplateNotFound:
        return render_template('default' + '/index.html', username=subdomain)

@blog.route('/',methods=['get'],subdomain='blog')
@blog.route('/<string:sub_url>',methods=['get'])
def index(sub_url='default'):

    try:
        return render_template(sub_url+'/index.html',username=sub_url)
    except TemplateNotFound:
        return render_template('default' + '/index.html', username=sub_url)
