# -*- coding:utf-8 -*-
import socket
import ssl
import binascii
import threading
from JsonResult import ApiCommonResult
from base import BaseHandler
from APNSWrapper import *
from mysql_deal import myqslOperation

__author__ = 'striveliu'


class UploadTokenHandler(BaseHandler):
    def get(self):
        str_device_token = self.get_argument("device_token")
        str_userid = self.get_argument("user_id")
        str_device_token = str_device_token.replace(" ","")
        str_device_token = str_device_token.replace("<","")
        str_device_token = str_device_token.replace(">","")

        #保存token
        sql_object = myqslOperation()
        sql_object.inser_user_deviceToken(self.db,str_userid,str_device_token)
        self.write('ok')
        """
        device_token = binascii.unhexlify(str_device_token)
        thread = threading.Thread(target=self.send_APNS_Notify(device_token,str_pushMesg,1),name="apn_thread")
        thread.start()
        resultDict={"reuslt":"ok"}
        json_res=ApiCommonResult(resultDict)
        self.write(json_res.to_json())
        """
class APN_SendMessage(object):

    def send_APNS_Notify(self,a_token, a_message,a_badge):
        notification = APNSNotification()
        notification.token(a_token)
        notification.alert(a_message)
        notification.badge(a_badge)
        notification.sound()

        filePath = os.path.dirname(__file__)
        cerPath = os.path.join(filePath,"cer")
        pushPath = os.path.join(cerPath,"push_cert.pem")
        #is_exit = os.path.exists(pushPath)
        wrapper = APNSNotificationWrapper(pushPath,True,False,True)
        wrapper.append(notification)
        wrapper.notify()
        self.write("ok")
        print "push_send"


