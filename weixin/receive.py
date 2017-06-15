# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

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
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.Event = xmlData.find('Event').text

class Msg(object):
    def __init__(self):
        pass
    def send(self):
        return "success"

class Click(EventMsg):
    def __init__(self, xmlData):
        EventMsg.__init__(self, xmlData)
        self.Eventkey = xmlData.find('EventKey').text
        return self.Eventkey

class View(EventMsg):
    def __init__(self, xmlData):
        EventMsg.__init__(self, xmlData)
        self.Eventkey = xmlData.find('EventKey').text
        return self.Eventkey

class TextMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.Content = xmlData.find('Content').text.encode("utf-8")
        return self.Content

class Subscribe(EventMsg):
    def __init__(self, xmlData):
        EventMsg.__init__(self, xmlData)
        self.Eventkey = xmlData.find('EventKey').text
        return  self.Eventkey