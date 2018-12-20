# _*_ coding: utf-8 _*_
# @File  : UserService.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/18
# @Desc  : 用于处理user相关的操作

import hashlib,base64
import random
import string


class UserService():
    '''处理User的相关操作'''
    @staticmethod
    def geneAuthCode(user_info):
        '''
        :param user_info: 数据库中登录后查询到的用户记录对象
        :return: 产生授权码，用于加密cookie
        '''
        m = hashlib.md5()
        # 加密字符串由以下4部分组成
        str = '%s-%s-%s-%s'%(user_info.uid, user_info.login_name, user_info.login_pwd, user_info.login_salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def genePwd(pwd, salt):
        '''
        加密密码算法
        :param pwd: 获取前端输入的密码
        :param salt:自定义加密的密钥
        :return: 加密处理后的密码
        '''
        m = hashlib.md5()
        str = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length=16):
        '''
        随机产生一个16位的salt
        :param length:
        :return:
        '''
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return ("".join(keylist))
