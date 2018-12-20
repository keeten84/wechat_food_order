# _*_ coding: utf-8 _*_
# @File  : Account.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/17
# @Desc  : 路由分配，/account目录下的各个用户管理页面

from flask import Blueprint
from common.libs.user.Helper import ops_render


route_account = Blueprint('account_page', __name__)


@route_account.route('/index')
def login():
    return ops_render('account/index.html')


@route_account.route('/info')
def edit():
    return ops_render('account/info.html')


@route_account.route('/set')
def resetPwd():
    return ops_render('account/set.html')
