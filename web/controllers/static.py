# _*_ coding: utf-8 _*_
# @File  : static.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/17
# @Desc  :

from flask import Blueprint, send_from_directory
from application import app


route_static = Blueprint('static', __name__)

@route_static.route('/<path:filename>')
def index(filename):
    return send_from_directory(app.root_path + '/web/static/',filename )