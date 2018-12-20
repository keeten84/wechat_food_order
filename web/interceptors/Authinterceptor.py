# _*_ coding: utf-8 _*_
# @File  : Authinterceptor.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/20
# @Desc  : 自定义的拦截器

from application import app
from flask import request, redirect, g
from common.models.user import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
import re


@app.before_request
def before_request():
    # 通过设置自定义过滤url，是程序跳过对指定对url进行查询
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']

    #当前需要检查访问地址
    path = request.path

    pattern = re.compile('%s' % '|'.join( ignore_check_login_urls))
    if pattern.match(path):
        return

    user_info = check_login()
    # 通过g变量获取用户的信息
    g.current_user = None
    if user_info:
        g.current_user = user_info


    pattern = re.compile('%s' % '|'.join(ignore_urls))
    if pattern.match(path):
        return

    if not user_info:
        return redirect(UrlManager.buildUrl('/user/login'))
    return


def check_login():
    '''
    判断用户是否已经登录
    :return:
    '''
    cookies = request.cookies
    auth_cookies = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None
    # 如果没有cookies返回false
    if auth_cookies is None:
        return False
    #如果cookies不全页返回false
    auth_info = auth_cookies.split('#')
    if len(auth_info) !=2:
        return False

    #如果通过上面步骤cookie分割出来uid之后对数据进行查询，数组的形式是从'%s#%s'分割为['%s','%s']
    try:
        # 所以从第二个%s为uid去进行查询
        user_info = User.query.filter_by(uid = auth_info[1]).first()
    except Exception:
        return False
    # 如果uid没有找到用户数据（可能是伪造uid）也返回False
    if user_info is None:
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):
        return False

    return user_info
