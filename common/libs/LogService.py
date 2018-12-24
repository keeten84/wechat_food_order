# _*_ coding: utf-8 _*_
# @File  : LogService.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/24
# @Desc  :
import json

from flask import request, g
from common.models.log.AppAccessLog import AppAccessLog
from common.models.log.AppErrorLog import AppErrorLog
from common.libs.Helper import getCurrtentDate
from application import db


class LogService():
    @staticmethod
    def addAccessLog():
        '''
        添加浏览记录
        :return:
        '''
        target = AppAccessLog()
        target.target_url = request.url
        target.referer_url = request.referrer
        target.ip = request.remote_addr
        target.query_params = json.dumps(request.values.to_dict())
        if 'current_user' in g and g.current_user is not None:
            target.uid = g.current_user.uid
        target.ua = request.headers.get('User-Agent')
        target.created_time = getCurrtentDate()
        db.session.add(target)
        db.session.commit()
        return True

    @staticmethod
    def addErrorLog(content):
        '''
        添加错误记录
        :return:
        '''
        target = AppErrorLog()
        target.target_url = request.url
        target.referer_url = request.referrer
        target.query_params = json.dumps(request.values.to_dict())
        target.content = content
        target.created_time = getCurrtentDate()
        db.session.add(target)
        db.session.commit()
        return True