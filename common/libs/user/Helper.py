# _*_ coding: utf-8 _*_
# @File  : Helper.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/20
# @Desc  :

from flask import g, render_template

def ops_render( templete, context={}):
    '''
    统一渲染方法
    :param templete: 需要渲染的模板
    :param context:  上下文的变量
    :return:
    '''
    if 'current_user' in g:
        context['current_user'] = g.current_user
    return render_template( templete, **context)