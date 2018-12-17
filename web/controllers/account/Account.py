# _*_ coding: utf-8 _*_
# @File  : Account.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/17
# @Desc  : 路由分配，/account目录下的各个用户管理页面

from flask import Blueprint, render_template


route_account = Blueprint('account_page', __name__)


@route_account.route('/index')
def login():
    return render_template('account/index.html')


@route_account.route('/info')
def edit():
    return render_template('account/info.html')


@route_account.route('/set')
def resetPwd():
    return render_template('account/set.html')
