# _*_ coding: utf-8 _*_
# @File  : UpLoadService.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/26
# @Desc  :
# -*- coding: utf-8 -*-
import datetime
import os, stat, uuid
from werkzeug.utils import secure_filename
from application import app, db
from common.models.Image import Image
from common.libs.Helper import getCurrtentDate


class UploadService():
    @staticmethod
    def uploadByFile(file):
        '''
        以文件类型去上传到方法
        :param file:
        :return:
        '''
        # 获取到UPLOAD里面自定义的配置
        config_upload = app.config['UPLOAD']
        # 自定义返回信息
        resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
        # 通过方法获取安全的文件名
        filename = secure_filename(file.filename)
        # 获取文件名中的扩展名，比如 11.jpg
        ext = filename.rsplit('.', 1)[1]
        if ext not in config_upload['ext']:
            resp['code'] = -1
            resp['msg'] = "不允许的扩展类型文件"
            return resp

        # 设定保存路径，可以获取到web/static/upload这个目录
        root_path = app.root_path + config_upload['perfix_path']
        # 不使用getCurrentDate创建目录，为了保证其他写的可以用，这里改掉，服务器上好像对时间不兼容
        file_dir = datetime.datetime.now().strftime("%Y%m%d")
        # 定义保存路径 ， 可以获取到web/static/upload/日期 这个目录
        save_dir = root_path + file_dir
        # 如果保存到路径不存在
        if not os.path.exists(save_dir):
            # 创建目录
            os.mkdir(save_dir)
            # 设置目录权限
            os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)

        file_name = str(uuid.uuid4()).replace("-", "") + "." + ext
        # 路径+文件名去保存
        file.save("{0}/{1}".format(save_dir, file_name))

        # 保存到数据库
        model_image = Image()
        model_image.file_key = file_dir + '/' + file_name
        model_image.created_time = getCurrtentDate()
        db.session.add(model_image)
        db.session.commit()

        resp['data'] = {
            'file_key': model_image.file_key
        }
        return resp
