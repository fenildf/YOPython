from JsonResult import ApiCommonResult
from base import BaseHandler
from mysql_deal import myqslOperation

__author__ = 'striveliu'

class SearchUserAPI(BaseHandler):
    def get(self):
        strUserid = self.get_argument("userid")
        mysql = myqslOperation()
        list = mysql.querySQL(self.db,strUserid)
        if list:
            jsonRes = ApiCommonResult(list)
            self.write(jsonRes.to_json())
        else:
            jsonRes = ApiCommonResult(list)
            jsonRes.success=False
            self.write(jsonRes.to_json())

