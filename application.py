# _*_ coding: utf-8 _*_
# @File  : application.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/3
# @Desc  :

import os
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy


class Application(Flask):
    def __init__(self, import_name,template_folder = None, root_path=None,static_folder=None):
        super(Application, self).__init__(import_name,template_folder=template_folder, root_path=None,static_folder=None)
        # 初始化配置文件，用from_pyfile()方法去配置，更具不同的使用环境去自动配置不同的初始化配置文件
        self.config.from_pyfile('config/base_settings.py')
        # 通过终端输入 export ops_config='xxxxx'去配置需要使用不同开发环境的配置文件
        # 例如 export ops_config=local就会使用 local_settings.py这个配置文件
        if 'ops_config' in os.environ:
            self.config.from_pyfile('config/%s_settings.py'%os.environ['ops_config'])

        # self.config.from_pyfile('config/production_setting.py')
        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__, template_folder= os.getcwd()+'/web/templates/',root_path= os.getcwd(),static_folder=None)
manager = Manager(app)



# 函数模版：将python的方法注入到html里面使用
from common.libs.UrlManager import UrlManager
app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')
app.add_template_global(UrlManager.buildImageUrl, 'buildImageUrl')