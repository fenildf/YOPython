from JsonResult import ApiCommonResult
from base import BaseHandler
from mysql_deal import myqslOperation

__author__ = 'striveliu'

class ModifyUserInfo(BaseHandler):
    def get(self):
        str_userid=self.get_argument("user_id")
        str_usernick=self.get_argument("user_nick",default="YOYO")
        str_phonenum=self.get_argument("phone_num",default=1234)
        sqlobjc=myqslOperation()
        sqlobjc.update_user_info(self.db,str_userid,str_usernick,str_phonenum)
        resultDict={"result":"ok"}
        json_res=ApiCommonResult(resultDict)
        self.write(json_res.to_json())

    def non(self):
        pass
