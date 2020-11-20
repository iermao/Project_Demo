# -*- coding:utf-8 -*-
# Author: iermao
# Python 3.6.6

from Server.Web.APIhandler import *
from Server.Web.Commonhandler import *

urls = [
    (r"/", IndexHandler),
    (r"/web/api/.*", apihandler),
]