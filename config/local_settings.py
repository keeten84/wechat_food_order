# _*_ coding: utf-8 _*_
# @File  : local_settings.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/3
# @Desc  : 用于配置本地开发环境的服务器端配置

SERVER_PORT = 8999

DEBUG = True

SQLALCHEMY_ECHO = True
# 出现 UserWarning: Neither SQLALCHEMY_DATABASE_URI nor SQLALCHEMY_BINDS is set错误的解决方法
SQLALCHEMY_DATABASE_URI = 'mysql://root:andy1984@127.0.0.1/food_order?charset=utf8mb4'
# 出现 FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS错误提示的解决方法
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 将所有的sql语句打印处理的设置
SQLALCHEM_ENCODING = 'utf-8'

RELEASE_VERSION = '20181224001'