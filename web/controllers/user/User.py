# _*_ coding: utf-8 _*_
# @File  : Account.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/17
# @Desc  : 路由分配，/user目录下的各个用户管理页面

from flask import Blueprint, render_template


route_user = Blueprint('user_page', __name__)


@route_user.route('/login')
def login():
    return render_template('user/login.html')


@route_user.route('/edit')
def edit():
    return render_template('user/edit.html')


@route_user.route('/reset-pwd')
def resetPwd():
    return render_template('user/reset_pwd.html')
