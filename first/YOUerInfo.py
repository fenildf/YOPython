# -*- coding:utf-8 -*-
import datetime
from JsonResult import *
from base import BaseHandler
from mysql_deal import *
__author__ = 'striveliu'

class UserInfoData(object):
    def __init__(self):
        self.userId = 0
        self.userNick = "Genius"

    def getCurrentUserInfo(self):
        self.userId = datetime.datetime.now().microsecond
        self.userNick = "YO!YO!"

    def writInfoToDataBase(self, dbconnection):
        sqlOperObj = myqslOperation()
        sqlOperObj.insertUserInfoTabel(self.userId, self.userNick,dbconnection)


class GetUserInfoAPI(BaseHandler):
    def get(self):
        if self.request.arguments:
            str_userid = self.get_argument("user_id")
            sqlOperObj = myqslOperation()
            userinfo_List = sqlOperObj.querySQL(self.db,str_userid)
            jsonRes = ApiCommonResult(userinfo_List)
        else:
            userInfoObj = UserInfoData()
            userInfoObj.getCurrentUserInfo()
            userInfoObj.writInfoToDataBase(self.db)

            UserArry = [{'user_id':userInfoObj.userId,'user_nick':userInfoObj.userNick}]
            jsonRes = ApiCommonResult(UserArry)

        self.write(jsonRes.to_json())

