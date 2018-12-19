# _*_ coding: utf-8 _*_
# @File  : UserService.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/18
# @Desc  : 用于处理user相关的操作

import hashlib,base64

class UserService():
    '''处理User的相关操作'''

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