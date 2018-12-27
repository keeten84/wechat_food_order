# -*- coding: utf-8 -*-
import time
from application import app

class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl( path ):
        return path

    @staticmethod
    def buildStaticUrl(path):

        release_version = app.config.get('RELEASE_VERSION')
        ver = "%s"%(int(time.time())) if not release_version else release_version
        path =  "/static" + path + "?ver=" + ver
        return UrlManager.buildUrl( path )

    @staticmethod
    def buildImageUrl(path):
        app_config = app.config['APP']
        # url = 域名 + 图片前缀 + key
        #  'http://0.0.0.0:8999/' + 'static/upload/' + path
        url = app_config['domain'] + app.config['UPLOAD']['perfix_url'] + path
        return url