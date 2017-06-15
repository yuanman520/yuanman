#coding:utf-8
import os
from menu import *
from basic import *
from handler import *

settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "../templates"),
            static_path=os.path.join(os.path.dirname(__file__), "../static"),
            debug=True,
            cookie_secret='MuG7xxacQdGPR7Svny1OfY6AymHPb0H/t02+I8rIHHE=',
        )

application = tornado.web.Application([
    (r"/weixin_api", MainHandler),
], **settings)

if __name__ == '__main__':
    application.listen(8001)
    myMenu = Menu()
    postJson = """
        {
            "button":
            [
                {
                    "type": "view",
                    "name": "绑定微信",
                    "url":  "http://www.baidu.com"
                },
                {
                    "name": "查询信息",
                    "sub_button":
                    [
                        {
                            "type": "view",
                            "name": "IP查询",
                            "url": "http://www.baidu.com"
                        },
                        {
                            "type": "view",
                            "name": "租户查询",
                            "url": "http://www.baidu.com"
                        },
                    ]
                },
                {
                    "type": "view",
                    "name": "关于我们",
                    "url": "http://www.baidu.com"
                }
              ]
        }
        """
    accessToken = Basic().get_access_token()
    myMenu.create(postJson, accessToken)
    tornado.ioloop.IOLoop.instance().start()
