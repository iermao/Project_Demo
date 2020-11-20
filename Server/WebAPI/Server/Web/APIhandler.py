# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

import os
import threading

import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornado.web import RequestHandler
from tornado import httpclient
from Server.Utils import dbhelper

import json


class BaseHandler(RequestHandler):
    #  允许跨域访问的地址
    def allowMyOrigin(self):
        self.set_header('Access-Control-Allow-Origin', 'http://localhost:9527')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE, OPTIONS")
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        #


class apihandler(BaseHandler):
    def set_default_headers(self):
        pass
        # self.allowMyOrigin()

    async def get(self, *args, **kwargs):
        print("get")

        _id = dbhelper.Seluid('13')
        # self.write(self.request.uri + "get  " + str(_id))

        self.write('{"code":20000,"data":{"roles":["admin"],"introduction":"I am a super administrator","avatar":"https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif","name":"Super Admin"}}')

    async def post(self, *args, **kwargs):
        _data = self.request.body
        _id = await dbhelper.Seluid('13')
        # self.write(self.request.uri + "post  " + str(_id))

        self.write('{"code":20000,"data":{"roles":["admin"],"introduction":"I am a super administrator","avatar":"https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif","name":"Super Admin"}}')
        # msg = await self.acc.Reg(_data, self)

        # msgjson = json.loads(msg)
        # print(self.request.method)
        # print(self.request.uri)
        # print(self.request.path)
        # print(self.request.query)
        # print(self.request.version)
        # print(self.request.headers)
        # print(self.request.body)
        # print(self.request.remote_ip)
        # print(self.request.protocol)
        # print(self.request.host)
        # print(self.request.arguments)
        # print(self.request.query_arguments)
        # print(self.request.body_arguments)
        # print(self.request.files)
        # print(self.request.connection)
        # print(self.request.cookies)
        # print(self.request.full_url())
        # print(self.request.request_time())

        # self.write(msgjson)

        self.finish()

    # def check_origin(self, origin):
    #     return True  # 允许WebSocket的跨域请求
