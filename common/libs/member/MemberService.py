# _*_ coding: utf-8 _*_
# @File  : MemberService
# @Author: Keeten_Qiu
# @Date  : 2018/12/25
# @Desc  :

import hashlib,requests,random,string,json
from application import app
class MemberService():

    @staticmethod
    def geneAuthCode( member_info = None ):
        m = hashlib.md5()
        str = "%s-%s-%s" % ( member_info.id, member_info.salt,member_info.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def geneSalt( length = 16 ):
        keylist = [ random.choice( ( string.ascii_letters + string.digits ) ) for i in range( length ) ]
        return ( "".join( keylist ) )

    @staticmethod
    def getWeChatOpenId( code ):
        '''
        获取openID的方法，参照小程序开发文档
        :param code:
        :return: openid
        '''
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format(app.config['MINI_APP']['appid'], app.config['MINI_APP']['appkey'], code)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = None
        if 'openid' in res:
            openid = res['openid']
        return openid
