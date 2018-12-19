# _*_ coding: utf-8 _*_
# @File  : Account.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/17
# @Desc  : 路由分配，/user目录下的各个用户管理页面

from flask import Blueprint, render_template, request, jsonify

from application import db, app
from common.models.user import User
from common.libs.user.UserService import UserService

route_user = Blueprint('user_page', __name__)


@route_user.route('/login', methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template('user/login.html')

    # 定义一个返回的值，用于返回错误信息或者其他信息
    resp = {'code': 200, 'msg': '登录成功~~', 'data': {}}
    #获取所有post请求的请求的值
    req = request.values
    # 检查是否有接收到值
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    # -- 判断用户名和密码是否为空的逻辑 --
    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确的登录用户名'
        return jsonify(resp)
    if login_pwd is None or len(login_pwd) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确的登录密码'
        return jsonify(resp)

    # -- 判断数据库中是否已经有该用户存在的逻辑 --
    user_info = User.query.filter_by(login_name=login_name).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名和密码 -1'
        return jsonify(resp)
    # -- 判断数据库中的密码是否正确的逻辑 --
    if user_info.login_pwd != UserService.genePwd( login_pwd, user_info.login_salt ):
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名和密码 -2'

    return jsonify(resp)



@route_user.route('/edit')
def edit():
    return render_template('user/edit.html')


@route_user.route('/reset-pwd')
def resetPwd():
    return render_template('user/reset_pwd.html')


