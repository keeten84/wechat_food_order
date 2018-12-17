# _*_ coding: utf-8 _*_
# @File  : manager.py
# @Author: Keeten_Qiu
# @Date  : 2018/12/13
# @Desc  : 用于运行项目的运行文件

from application import app, manager
from flask_script import Server
import www

# web server自定义一个命令名，这里是添加运行服务器的命令,通过导入app，使用app下config配置的端口为服务器端口
manager.add_command('runserver', Server( host='0.0.0.0', port=app.config['SERVER_PORT'], use_debugger=True,))


def main():
    manager.run()

if __name__ == '__main__':
    try:
        import sys
        sys.exit(main())
    except Exception as e:
        import traceback
        # 通过main方法去运行，如果运行出错，通过python自带的traceback模块下的print_exc()方法去打印错误
        traceback.print_exc()