# _*_ coding: utf-8 _*_
# @File  : __init__.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/24
# @Desc  : 所有连接小程序api的接口

from flask import Blueprint


route_api = Blueprint('api_page',__name__)
from web.controllers.api.Member import *


@route_api.route('/', methods = ["GET","POST"])
def index():
    return 'Mina api V1.0'