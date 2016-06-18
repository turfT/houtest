# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import requests
import os
import urllib2
import json
from lxml import etree
import cookielib
import re
import random
import cxkd
from imgtest import *

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

def POST(self): 
    str_xml = web.data() #获得post来的数据 
    xml = etree.fromstring(str_xml)#进行XML解析 
    msgType=xml.find("MsgType").text 
    fromUser=xml.find("FromUserName").text 
    toUser=xml.find("ToUserName").text 
    if msgType == 'text':
        content=xml.find("Content").text
        return self.render.reply_text(fromUser,toUser,int(time.time()), content)
    elif msgType == 'image':
        pass
    else:
        pass
