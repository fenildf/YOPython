# -*- coding:utf-8 -*-
import threading

__author__ = 'striveliu'
from base import BaseHandler
from mysql_deal import myqslOperation
from YOAPNFile import  APN_SendMessage
import base64

class SendMessageAPI(BaseHandler):
    def get(self):
        if self.get_argument("fromId"):
            fromid = self.get_argument("fromId")
        if self.get_argument("toId"):
            toid = self.get_argument("toId")
        if self.get_argument("msgContent"):
            base_msg = self.get_argument("msgContent")
            msg = base64.standard_b64decode(base_msg)
        if fromid and toid and msg:
            thread = threading.Thread(target=self.sendMsg(fromid,toid,msg),name="apn_sendmsg_thread")
            thread.start()


    def getToIdToken(self,aToId):
        sqlObject = myqslOperation()
        utlist = sqlObject.getUserToken(self.db, aToId)
        strToken = None
        if utlist:
            strToken = utlist[0]["user_token"]

        return strToken

    def composeSendMsg(self,fromId,msg):
        sqlObject = myqslOperation()
        if fromId:
            fromlist = sqlObject.querySQL(self.db,fromId)
            fromNick = fromlist[0]["user_nick"]

        msgContent = "您的YO友"+fromNick+"说:"+msg
        return msgContent

    def sendMsg(self,fromid,toid,msg):
        str_token = self.getToIdToken(toid)
        str_msg = self.composeSendMsg(fromid,msg)
        sendHandler = APN_SendMessage()
        sendHandler.send_APNS_Notify(str_token,str_msg,1)

