# _*_ coding: utf-8 _*_
# @File  : Helper.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/20
# @Desc  :

from flask import g, render_template
from datetime import datetime


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


def iPagination( params ):
    '''
    自定义分页函数
    :param params:
    :return:
    '''
    import math

    ret = {
        "is_prev":1, #是否有前一页
        "is_next":1, #是否有后一页
        "from" :0 ,  #开始页数
        "end":0,     #结束页数
        "current":0, #当前页数
        "total_pages":0, #总页数
        "page_size" : 0, #每页大小
        "total" : 0, #
        "url":params['url'] #url地址
    }

    total = int( params['total'] )
    page_size = int( params['page_size'] )
    page = int( params['page'] )
    display = int( params['display'] )
    total_pages = int( math.ceil( total / page_size ) )
    total_pages = total_pages if total_pages > 0 else 1
    if page <= 1:
        ret['is_prev'] = 0

    if page >= total_pages:
        ret['is_next'] = 0

    semi = int( math.ceil( display / 2 ) )

    if page - semi > 0 :
        ret['from'] = page - semi
    else:
        ret['from'] = 1

    if page + semi <= total_pages :
        ret['end'] = page + semi
    else:
        ret['end'] = total_pages

    ret['current'] = page
    ret['total_pages'] = total_pages
    ret['page_size'] = page_size
    ret['total'] = total
    ret['range'] = range( ret['from'],ret['end'] + 1 )
    return ret


def getCurrtentDate( format='%Y-%m-%d %H:%M:%S'):
    '''
    生成当前时间
    :param fromat:
    :return:
    '''
    return datetime.now().strftime(format)