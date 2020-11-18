# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

from Server.Web.Handler.APIhandler import *

urls = [
    (r"/web/api/.*", apihandler),
]