#
# 字节跳动登录相关
#
import json
import time
import hashlib

from Server import logging

import tornado.web
from tornado import gen

from . import dbhelper
from . import CFun

from tornado import httpclient


class bytedanceHandler():
    def __init__(self):
        self.appid = "ttc478b2c55b42c2f9"
        self.secret = "0a882c0ceecf7fdae334ac888fcdaf2c43e2f4e9"
        self.grant_type = "client_credential"
        self.access_token_gettime = 0
        self.access_token = ""
        self.expires_in = 0

        self.access_token_url = "https://developer.toutiao.com/api/apps/token?appid={0}&secret={1}&grant_type={2}"
        self.login_url = "https://developer.toutiao.com/api/apps/jscode2session?appid={0}&secret={1}&code={2}&anonymous_code={3}"

        self.pay_get_balance = "https://developer.toutiao.com/api/apps/game/wallet/get_balance"
        pass

    async def GET(self, headler):
        pass

    async def POST(self, headler):
        _data = headler.request.body
        _json = json.loads(_data)
        _type = _json["type"]
        if (_type == "login"):
            await self.login(headler, _json)
        elif (_type == "order"):
            await self.Set_order(headler, _json)
        elif (_type == "pay"):
            await self.PaySuc(headler, _json)
        elif (_type == ""):
            pass

    # 定时校验 access_token 是否过期，如果过期则需要获取 access_token
    async def check_accesstoken(self):
        if self.access_token_gettime == 0:
            # 校验回话秘钥
            await self.get_access_token()
        elif self.access_token_gettime > 0:
            _time = self.access_token_gettime + 3600
            _now = time.time()
            if _time < _now:
                await self.get_access_token()

    # 获取access_token
    async def get_access_token(self):
        http = httpclient.AsyncHTTPClient()
        http_get = await http.fetch(self.access_token_url.format(self.appid, self.secret, self.grant_type))
        _data = http_get.body.decode('utf-8')
        _dict_data = json.loads(_data)

        logging.info(str(_dict_data))

        try:
            self.access_token = _dict_data["access_token"]
            self.expires_in = _dict_data["expires_in"]
            self.access_token_gettime = time.time()
        except:
            pass

        return True

    # 登录
    async def login(self, headler, _json):
        code = CFun.filter_url(_json["code"])
        anonymous_code = CFun.filter_url(_json["anonymousCode"])
        pttype = CFun.filter_url(_json["pttype"])
        ptid = CFun.filter_url(_json["ptid"])
        channel = CFun.filter_url(_json["channel"])
        devicetype = CFun.filter_url(_json["devicetype"])

        # 验证access Token
        await self.get_access_token()

        http = httpclient.AsyncHTTPClient()
        http_get = await http.fetch(self.login_url.format(self.appid, self.secret, code, anonymous_code))
        _data = http_get.body.decode('utf-8')
        _dict_data = json.loads(_data)

        # print(_dict_data)

        msg = {'code': -1, 'msg': '', 'uid': '', 'pwd': '', 'keys': ''}

        if _dict_data["error"] == 0:
            # 判断是否首次进入注册角色
            session_key = _dict_data["session_key"]
            openid = _dict_data["openid"]
            anonymous_openid = _dict_data["anonymous_openid"]

            _pwdmd5 = hashlib.md5(openid.encode(encoding='UTF-8')).hexdigest()
            _tmpstr = (openid + "wowadmin+=-09").encode(encoding='UTF-8')
            _key = hashlib.md5(_tmpstr).hexdigest()

            _name = openid
            _seluid = await dbhelper.SelUser(_name, _pwdmd5)

            print("_seluid1", _seluid)
            if (_seluid > 0):
                msg['code'] = 0
            else:
                _seluid = await dbhelper.RegUser_pt(_name, _pwdmd5, pttype, ptid, channel, anonymous_openid, openid, devicetype)
                print("_seluid2", _seluid)
                if (_seluid > 0):
                    msg['code'] = 0
                else:
                    msg['code'] = 1
            # 记录登录log
            if msg['code'] == 0:
                await dbhelper.login_log(_name, _pwdmd5, pttype, ptid, channel, anonymous_openid, openid, devicetype)

            msg["uid"] = str(openid)
            msg["pwd"] = str(_pwdmd5)
            msg["keys"] = str(_key)
            msg = json.dumps(msg)

        headler.write(msg)

    #登录获取数据
    def GetMsg(self, code, errmsg):
        pass

    #  生成订单---
    def Set_order(self, headler, _json):
        pass

    # 充值成功
    def PaySuc(self, headler, _json):

        pass

    def Get_balance(self, openid):
        _ts = int(time.time())
        _postdata = {"openid": openid, "appid": self.appid, "zone_id": "1", "mp_sig": "d1f0a41272f9b85618361323e1b19cd8cb0213f2", "access_token": self.access_token, "ts": _ts, "pf": "android"}
