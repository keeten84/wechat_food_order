# _*_ coding: utf-8 _*_
# @File  : __init__.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/24
# @Desc  :

from flask import Blueprint
from web.controllers.api import *


route_api = Blueprint('api_page',__name__)

@route_api.route('/')


def index():
    return 'Mina api V1.0'