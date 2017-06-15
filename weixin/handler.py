#coding:utf-8
import hashlib
import tornado.web
import receive

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
        signature = self.get_argument('signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')
        echostr = self.get_argument('echostr', '')
        if signature and timestamp and nonce and echostr:
            if checksignature(signature, timestamp, nonce):
                self.write(echostr)
            else:
                self.write('fail')
        else:
            self.write("hello i failed")

    def post(self):
        body = self.request.body
        receive.parse_xml(body)























