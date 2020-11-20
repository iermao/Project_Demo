# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

import os
import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornado.web import RequestHandler
from tornado import httpclient

import json


class BaseHandler(RequestHandler):
    #  允许跨域访问的地址
    def allowMyOrigin(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')


class IndexHandler(BaseHandler):
    def get_current_user(self):
        '''
        重写RequestHandler类中的get_current_user方法，用来判断当前是否是登录状态，请求中所有被@tornado.web.authenticated 装饰的方法，都需要此方法返回值不为None，否则给与403拒绝
        :return: 用户名或者None . 为None判断为非法请求，POST 时Tornado进行403 禁止访问 ；GET 时 302 重定向到/login  123213213
        '''
        user = self.get_argument(name='username', default='None')
        if user and user != 'None':
            print('IndexHandler类 get_current_user获取到用户:', user)
            return user

    # 确认请求合法 依赖于get_current_user(self):函数的返回值作为判断请求是否合法
    async def get(self):
        print("Commonhandler  get")
        self.write(self.request.uri + "get")

    async def post(self, *args, **kwargs):
        print("Commonhandler  post")
        self.write(self.request.uri + "post")
