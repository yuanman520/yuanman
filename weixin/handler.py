#coding:utf-8
import tornado.ioloop
import hashlib
import tornado.web
import xml.etree.ElementTree as ET
import time

def checksignature(signature, timestamp, nonce):
    args = []
    args.append('geehoo')
    args.append(timestamp)
    args.append(nonce)
    args.sort()
    mysig = hashlib.sha1(''.join(args)).hexdigest()
    return mysig == signature

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')
        if checksignature(signature, timestamp, nonce):
            self.write(echostr)
        else:
            self.write('fail')

    def post(self):
        body = self.request.body
        data = ET.fromstring(body)
        tousername = data.find('ToUserName').text
        fromusername = data.find('FromUserName').text
        createtime = data.find('CreateTime').text
        msgtype = data.find('MsgType').text
        event = None
        content = None
        eventkey = None
        if data.find('Event'):
            event = data.find('Event')
        if data.find('Content'):
            content = data.find('Content').text
        if data.find('EventKey'):
            eventkey = data.find('EventKey').text
        textTpl = """<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[%s]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            </xml>"""
        if event and event == 'subscribe'and msgtype == 'event':
            result = '感谢您关注西安极互云网络科技公众号，我们会竭力为您服务。'
            out = textTpl % (fromusername, tousername, str(int(time.time())), 'text', result)
            self.write(out)
        elif content and content == '我是谁':
            result = '我是您的小助手，您有问题就问我吧'
            out = textTpl % (fromusername, tousername, str(int(time.time())), 'text', result)
            self.write(out)
        elif eventkey and eventkey == 'bind_weixin' and event == 'view':
            self.redirect('/bind_weixin')
        elif eventkey and eventkey == 'query_ip' and event == 'view':
            self.redirect('/query_ip')
        elif eventkey and eventkey == 'query_tenant' and event == 'view':
            self.redirect('/query_tenant')
        elif eventkey and eventkey == 'about_us' and event == 'view':
            self.redirect('/about_us')

class Bind_handler(tornado.web.RequestHandler):
    def get(self):
        self.render('bind_weixin_page.html')

class Query_ip_handler(tornado.web.RequestHandler):
    def get(self):
        self.render('query_ip_page.html')

class Query_tenant_handler(tornado.web.RequestHandler):
    def get(self):
        self.render('query_ip_page.html')

class About_us_handler(tornado.web.RequestHandler):
    def get(self):
        self.render('query_ip_page.html')

class Bind_success_handler(tornado.web.RequestHandler):
    def get(self):
        self.write("绑定成功")

application = tornado.web.Application([
    (r"/weixin_api", MainHandler),
    (r"/bind_weixin", Bind_handler),
    (r"/query_ip", Query_ip_handler),
    (r"/query_tenant", Query_tenant_handler),
    (r"/about_us", About_us_handler),
    (r"bind_success", Bind_success_handler)
])
if __name__ == '__main__':
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()



















