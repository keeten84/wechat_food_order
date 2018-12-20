# _*_ coding: utf-8 _*_
# @File  : Account.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/17
# @Desc  : 路由分配，/user目录下的各个用户管理页面

import json
from flask import Blueprint, request, jsonify, make_response, redirect, g
from application import db, app
from common.models.user import User
from common.libs.user.Helper import ops_render
from common.libs.user.UserService import UserService
from application import app
from common.libs.UrlManager import UrlManager

route_user = Blueprint('user_page', __name__)


@route_user.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return ops_render('user/login.html')

    # 定义一个返回的值，用于返回错误信息或者其他信息
    resp = {'code': 200, 'msg': '登录成功~~', 'data': {}}
    # 获取所有post请求的请求的值
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
    if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名和密码 -2'

    # 添加cookie
    response = make_response(json.dumps(resp))
    # cookie由于可以模拟，所有第一个%s需要实现加密逻辑
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '%s#%s' %
                        (UserService.geneAuthCode(user_info), user_info.uid),60 * 60 * 24 * 120)
    # 登录成功返回带有cookie的成功登录信息
    return response


@route_user.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'GET':
        return ops_render('user/edit.html',{'current':'edit'})

    # 定义一个返回的值，用于返回错误信息或者其他信息
    resp = {'code': 200, 'msg': '修改成功~~', 'data': {}}
    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的姓名'
        return jsonify(resp)

    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的邮箱'
        return jsonify(resp)

    # 更新数据库
    user_info = g.current_user
    user_info.nickname = nickname
    user_info.email = email

    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)


@route_user.route('/reset-pwd',methods=['GET', 'POST'])
def resetPwd():
    if request.method == 'GET':
        return ops_render('user/reset_pwd.html',{'current':'reset-pwd'})

    # 定义一个默认返回值
    resp = {'code': 200, 'msg': '修改成功~~', 'data': {}}
    # 获取页面输入的值
    req = request.values

    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''

    if old_password is None or len(old_password) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的原密码~~"
        return jsonify(resp)

    if new_password is None or len(new_password) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的新密码~~"
        return jsonify(resp)

    if old_password == new_password:
        resp['code'] = -1
        resp['msg'] = "请重新输入一个吧，新密码和原密码不能相同哦~~"
        return jsonify(resp)

    # 检查原密码是否正确
    user_info = g.current_user
    old_password = UserService.genePwd(old_password, user_info.login_salt)
    if old_password != user_info.login_pwd:
        resp['code'] = -1
        resp['msg'] = "密码错误，请输入正确的原密码"
        return jsonify(resp)

    # 更新数据库
    user_info.login_pwd = UserService.genePwd(new_password, user_info.login_salt)
    db.session.add(user_info)
    db.session.commit()
    #commit之后由于密码改变，会退出返回到登录页面
    #cookie字符串生成的时候需要使用到user.pwd，所以如果想保存后不跳到重新登录，只需要重新刷新cookie就可以
    response = make_response(json.dumps(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '%s#%s' %
                        (UserService.geneAuthCode(user_info), user_info.uid), 60 * 60 * 24 * 120)
    return response



@route_user.route('logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl('/user/login')))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response
