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


def weather(city):
    r = requests.get('http://wthrcdn.etouch.cn/weather_mini?city='+city)
    data=r.json().get("data").get("forecast")
    
    forecast=map(lambda x :(x.get("date").encode("utf-8"),
                x.get("high").encode("utf-8"), x.get("low").encode("utf-8"),
                x.get("type").encode("utf-8")),data)
    
    
    forecast=map(lambda x: str(x[0])+":"+str(x[1])+"  "+
                str(x[2])+ "  "+str(x[3]),forecast)
    res=forecast[0]        
    res=city+":\n" +reduce(lambda x,y: x+"\n"+y,forecast)
    return res
    
class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr = data.echostr
        #自己的token
        token="wxpytest" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        #content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        #picurl = xml.find('PicUrl').text
        #return self.render.reply_text(fromUser,toUser,int(time.time()), content)
        if msgType == 'image':
            try:
                picurl = xml.find('PicUrl').text
                datas = imgtest(picurl)
                return self.render.reply_text(fromUser, toUser, int(time.time()), '图中人物性别为'+datas[0]+'\n'+'年龄为'+datas[1])
            except:
                return self.render.reply_text(fromUser, toUser, int(time.time()),  '识别失败，换张图片试试吧')
        else:
            content = xml.find("Content").text  # 获得用户所输入的内容
            if content[0:2] == u"天气":
                city = str(content[2:].encode("utf-8")) 
                city=filter(lambda x: x!=" ",city) 
                try:
                    res=weather(city)             
                    return self.render.reply_text(fromUser,toUser,int(time.time()), res)
                except :
                    return self.render.reply_text(fromUser, toUser, int(time.time()),  '换个城市？')
                    

   