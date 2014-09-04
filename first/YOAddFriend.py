# -*- coding:utf-8 -*-
from JsonResult import ApiCommonResult
from base import BaseHandler
from mysql_deal import myqslOperation

__author__ = 'striveliu'
#status 0 表示等待对方确认好友关系 1表示双向好友关系 2表示已经添加过好友
#       4
g_resdict = {"result":"ok"}
#添加好友操作
class AddFriendHandler(BaseHandler):
    def get(self):
        strFromUserid = self.get_argument("fromUserid")
        strToUserid = self.get_argument("toUserid")
        sqlObjc = myqslOperation()
        isAddRecord = sqlObjc.get_is_addrecord_relation(self.db,strFromUserid,strToUserid)
        resDict = {"status":0}
        if not isAddRecord:
            to_from_list = sqlObjc.get_friend_relation(self.db,strToUserid)
            if to_from_list:
                for a in to_from_list:
                    if a.to_id == strFromUserid:#同时修改to-from的status值
                        sqlObjc.update_friend_releation(self.db,strToUserid,strFromUserid,1)
                        resDict = {"status":1}
                        break
        else:
            resDict={"status":2}

        if resDict["status"]!=2:
            sqlObjc.insertFriendRelation(strFromUserid,strToUserid,resDict["status"],self.db)
        jsonRes = ApiCommonResult(resDict)
        self.write(jsonRes.to_json())


class IsHaveAddFriMsg(BaseHandler):
    def get(self):
        #判断是否有还有添加我的消息
        str_userid = self.get_argument("user_id")
        sqlObjc = myqslOperation()
        list = sqlObjc.get_is_have_addfriend_msg(self.db,str_userid)
        res_dict = {"result":"ok"}
        if list:
            json_res = ApiCommonResult(res_dict)
            self.write(json_res.to_json())
        else:
            res_dict["result"]="fail"
            json_res = ApiCommonResult(res_dict)
            self.write(json_res.to_json())

# 获取添加好友消息的消息体内容
class GetAddFriednMsgContent(BaseHandler):
    def get(self):
        str_userid = self.get_argument("user_id")
        sqlObjc = myqslOperation()
        list1 = sqlObjc.get_is_have_addfriend_msg(self.db,str_userid)
        res_dict = {"result":None}
        resultList=[]
        if list1:
            for msgDict in list1:
                from_list=sqlObjc.querySQL(self.db,msgDict["from_id"])
                resultDict = {"fromNick":from_list[0]["user_nick"],"fromId":msgDict["from_id"],"toNick":"","toId":msgDict["to_id"]}
                resultList.append(resultDict)
            json_res = ApiCommonResult(resultList)
            self.write(json_res.to_json())
        else:
            json_res = ApiCommonResult(res_dict)
            self.write(json_res.to_json())


class AgreeFriReleationAPI(BaseHandler):
    def get(self):
        #同意添加好友
        str_from_id = self.get_argument("fromId")
        str_to_id = self.get_argument("toId")
        sqlobjc=myqslOperation()
        is_update=sqlobjc.update_friend_releation(self.db,str_from_id,str_to_id,1)
        if is_update:
            self.write(ApiCommonResult(g_resdict).to_json())
        else:
            resultDict = {"result":"false"}
            self.write(ApiCommonResult(resultDict).to_json())

class GetUserFriendContentAPI(BaseHandler):
    def get(self):
        #获取好友
        resultlist = None
        if self.get_argument("userId"):
            str_userid = self.get_argument("userId")
        if self.get_argument("friTime"):
            str_fritime = self.get_argument("friTime")
        if str_userid:
            sqlobjc=myqslOperation()
            friendlist=sqlobjc.get_user_friend(self.db,str_userid, str_fritime)
            packlist = self.packet_friend(friendlist,str_userid,sqlobjc)
        if packlist:
            resultlist = packlist[0]
            currentTime = packlist[1]
        self.write(ApiCommonResult(resultlist, cTime=currentTime).to_json())



    def packet_friend(self,a_friendlist,userid,aSqlobject):
        if a_friendlist:
            resultlist = []
            currentTime = a_friendlist[0]["mt_ct"]
            for friRelDict in a_friendlist:
                str_fromid = friRelDict["from_id"]
                str_toid = friRelDict["to_id"]
                if str_fromid != userid:
                    friInfolist = aSqlobject.querySQL(self.db,str_fromid)
                else:
                    friInfolist=aSqlobject.querySQL(self.db,str_toid)
                if friInfolist:
                    friInfoDict = friInfolist[0]
                    resultDict = {"user_nick":friInfoDict["user_nick"],
                                  "user_id":friInfoDict["user_id"],
                                  "phone_num":friInfoDict["phone_num"]}
                    resultlist.append(resultDict)

            return resultlist,currentTime
