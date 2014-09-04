# -*- coding:utf-8 -*-
import random
import torndb
from JsonResult import ApiCommonResult
from ModifyUserInfo import ModifyUserInfo
from YOAPNFile import UploadTokenHandler
from YOAddFriend import AddFriendHandler, IsHaveAddFriMsg, GetAddFriednMsgContent, AgreeFriReleationAPI, \
    GetUserFriendContentAPI
from YOSearchUser import SearchUserAPI
from YOSendMsg import SendMessageAPI
from YOUerInfo import GetUserInfoAPI

__author__ = 'fangshi'
import os.path

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from tornado.web import RequestHandler

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/api/get_ju_item_list", JuItemAPI),
            (r"/peixun/api",PeixunAPI),
            (r"/api/uploadImg", UploadAPI),
            (r"/api/getUserInfo",GetUserInfoAPI),
            (r"/api/searchuser",SearchUserAPI),
            (r"/api/addfriend",AddFriendHandler),
            (r"/api/modify/personinfo",ModifyUserInfo),
            (r"/api/get/isaddfrimsg",IsHaveAddFriMsg),
            (r"/api/get/addfrimsg", GetAddFriednMsgContent),
            (r"/api/upload/devicetoken",UploadTokenHandler),
            (r"/api/agree/addfri",AgreeFriReleationAPI),
            (r"/api/getFrinend",GetUserFriendContentAPI),
            (r"/api/sendMsg",SendMessageAPI),
        ]

        settings = dict(
            blog_title=u"test",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.dbcn = torndb.Connection(database="mydatabase",user="lc1",password="123",host="127.0.0.1");



class Items(object):
    def __init__(self):
        self.itemId = "1500019881273"
        self.juwlItemType = "0"
        self.longName = "国际知名品牌，值得信赖，你知道拥有！"
        self.shortName = "皮尔卡丹专卖 "
        self.itemCount = "100"
        self.childCategory = "1200001"
        self.originalPrice = "5000"
        self.picUrl = "http://gju4.alicdn.com/bao/uploaded/i4/T1bt_dFgRaXXb1upjX.jpg_360x360.jpg"
        self.picWideUrl = "http://gju4.alicdn.com/bao/uploaded/i4/T1bt_dFgRaXXb1upjX.jpg_360x360.jpg"
        self.activityPrice = "500"
        self.itemStatus = "1"
        self.discount = "1.0"
        self.platformId = "1001"
        self.soldCount = "3"
        self.limitNum = "0"
        self.isLock = "1"
        self.onlineStartTime = "1359331200000"
        self.onlineEndTime = "1391471999000"
        self.discount = 0.0



img1 = "http://gju4.alicdn.com/bao/uploaded/i4/T1bt_dFgRaXXb1upjX.jpg_640x480.jpg"
img2 = "http://gju3.alicdn.com/bao/uploaded/i2/T1TaaSFiXgXXb1upjX.jpg_640x480.jpg"
img3 = "http://gju3.alicdn.com/bao/uploaded/i2/T1yifcFmleXXb1upjX.jpg_640x480.jpg"
img4 = 'http://gju1.alicdn.com/bao/uploaded/i2/T1PG96FnpeXXb1upjX.jpg_640x480.jpg'
img5 = 'http://gju3.alicdn.com/bao/uploaded/i1/T1eKW5FflXXXb1upjX.jpg_640x480.jpg'
img6 = 'http://gju2.alicdn.com/bao/uploaded/i1/T190q1FhJeXXb1upjX.jpg_640x480.jpg'
img = [img1, img2, img3, img4, img5, img6]

pinpai = ["adidas", "Nike", "三叶草", "九牧王", "安踏"]

category = ["上衣","短裤","短裙","手套","性用品","鞋子","长袖","短袖","凉鞋","帽子","眼镜","休闲裤","西裤","裙子"]
cateDict = {'上衣':'http://gju4.alicdn.com/bao/uploaded/i4/T1bt_dFgRaXXb1upjX.jpg_640x480.jpg','裤子':'http://gju4.alicdn.com/bao/uploaded/i4/T1bt_dFgRaXXb1upjX.jpg_640x480.jpg'}
class HomeHandler(RequestHandler):
    def get(self):

        self.write("oklllll1212")

class PeixunAPI(RequestHandler):
    def get(self):
        peixunImg = "http://gju4.alicdn.com/bao/uploaded/i4/T1bt_dFgRaXXb1upjX.jpg_640x480.jpg"
        peixunImg1 = "http://gju2.alicdn.com/bao/uploaded/i1/T190q1FhJeXXb1upjX.jpg_640x480.jpg"
        peixunImgArry = [peixunImg, peixunImg1]
        #res = ApiCommonResult(data=peixunImgArry)
        res = ApiCommonResult(data=category)
        self.set_header("aaaa","peixun")
        self.write(res.to_json())

class UploadAPI(RequestHandler):
    def post(self):
        bodyDict = self.request.files;
        keyArry = bodyDict.keys();
        for key in keyArry:
            dataArry = bodyDict[key]
            dataDict = dataArry[0]
            filename = dataDict['filename']
            data = dataDict['body']
            path1 = os.path.join(os.path.dirname(__file__), 'uploadFile')
            print path1
            filepath = os.path.join(path1, str(filename))
            print filepath
            writePut = open(filepath,'wb')
            writePut.write(data)
        print "upload success"
        #filename = RequestHandler.

class JuItemAPI(RequestHandler):
    def get(self):
        item_list = []
        for i in xrange(1, 10000):
            item = Items()
            item.itemId = i
            item.itemCount = random.randrange(1000, 50000)
            item.activityPrice = random.randrange(30, 500)
            item.originalPrice = item.activityPrice + 200
            dis = (item.activityPrice / item.originalPrice) * 10
            item.discount = '%1.1f' % dis
            item.soldCount = random.randrange(10, 10000)
            item.shortName = random.choice(pinpai) + random.choice(['国际知名品牌,值得信赖', '创造更加监控生活，极致卓越表现', ' 将体育精神融汇于每一步行走、每一次挥手'])
            item.picUrl = random.choice(img)
            item_list.append(item)

        page_no = int(self.get_argument('page_no', 0))
        page_size = int(self.get_argument("page_size", 10))
        msg = ""
        start = page_no * page_size
        end = start + page_size

        if end > len(item_list):
            data = ""
            msg = "item is null"
        else:
            data = item_list[start:end]

        if data:
            res = ApiCommonResult(name="JuItemAPI", data=data, success=True, msg=msg)
        else:
            res = ApiCommonResult(data=data, success=False, name="JuItemAPI", msg=msg)
        return self.write(res.to_json())


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()



