# _*_ coding: utf-8 _*_
# @File  : index.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/13
# @Desc  : 实现flask的blueprint蓝图功能

from flask import Blueprint, g
from common.libs.Helper import ops_render

route_index = Blueprint('index_page', __name__)

#配置/为根目录访问路径
@route_index.route('/')
def index():
    current_user = g.current_user
    return ops_render('index/index.html')