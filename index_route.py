# _*_ coding: utf-8 _*_
# @File  : index_route.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/3
# @Desc  :

from flask import Blueprint

index_route = Blueprint('index_page', __name__)

@index_route.route('/')
def index():
    return '<h1>welcome to food_order index page</h1>'

@index_route.route('/hello')
def userInfo():
    return 'food_order say hello to you'