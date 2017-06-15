# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

textTpl = """<xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[%s]]></MsgType>
                    <Content><![CDATA[%s]]></Content>
                    </xml>"""

def parse_xml(data):
    if len(data) == 0:
        return None
    xmlData = ET.fromstring(data)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'event':
        event_type = xmlData.find('Event').text
        if event_type == 'click':
            return Click(xmlData)
        elif event_type in ('subscribe', 'unsubscribe'):
            return Subscribe(xmlData)
        elif event_type == 'view':
            return View(xmlData)
    elif msg_type == 'text':
        return TextMsg(xmlData)

class EventMsg(object):
    def __init__(self, xmlData):
        self.msg = textTpl
        self.tousername = xmlData.find('ToUserName').text
        self.fromusername = xmlData.find('FromUserName').text
        self.createtime = xmlData.find('CreateTime').text
        self.msgtype = xmlData.find('MsgType').text
        self.event = xmlData.find('Event').text

class Msg(object):
    def __init__(self, data):
        self.msg = textTpl
        self.tousername = data.find('ToUserName').text
        self.fromusername = data.find('FromUserName').text
        self.createtime = data.find('CreateTime').text
        self.msgtype = data.find('MsgType').text
        self.content = data.find('Content').text

    def send(self):
        return "success"

class Click(EventMsg):
    def __init__(self, xmlData):
        EventMsg.__init__(self, xmlData)
        self.Eventkey = xmlData.find('EventKey').text
        self.return_msg()

    def return_msg(self):
        out = textTpl % (self.fromusername, self.tousername, str(int(self.createtime)), self.msgtype, self.Eventkey)
        return out

class View(EventMsg):
    def __init__(self, xmlData):
        EventMsg.__init__(self, xmlData)
        self.Eventkey = xmlData.find('EventKey').text
        self.return_msg()

    def return_msg(self):
        out = textTpl % (self.fromusername, self.tousername, str(int(self.createtime)), self.msgtype, self.Eventkey)
        return out

class TextMsg(Msg):
    def __init__(self, data):
        Msg.__init__(self,data)
        self.Content = data.find('Content').text.encode("utf-8")
        self.return_msg()

    def return_msg(self):
        out = textTpl % (self.fromusername, self.tousername, str(int(self.createtime)), self.msgtype, self.Content)
        return out

class Subscribe(EventMsg):
    def __init__(self, xmlData):
        EventMsg.__init__(self, xmlData)
        self.Eventkey = xmlData.find('EventKey').text
        self.return_msg()

    def return_msg(self):
        out = textTpl % (self.fromusername, self.tousername, str(int(self.createtime)), self.msgtype, self.Eventkey)
        return out