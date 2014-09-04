# -*- coding:utf-8 -*-
__author__ = 'striveliu'
import torndb

class myqslOperation(object):
    """
    根据user_id 获取用户信息
    """
    def querySQL(self,dbConnection,userId):
        sql=u"select * from user_info where user_id=%s"
        pars = [userId]
        list = dbConnection.query(sql,*pars)
        return list

    def get_friend_relation(self,dbConnection,userId):
        """
        获取对方有没有添加自己为好友
        :param dbConnection:
        :param userId:
        :return:
        """
        sql=u"select * from user_friend_releation  where from_id=%s and status=1"
        pars = [userId]
        list = dbConnection.query(sql,*pars)
        return list

    def get_is_have_addfriend_msg(self,dbConnection,userid):
        """
        获取是否有别人添加自己
        :param dbConnection:
        :param userid:
        :return:
        """
        sql=u"select * from user_friend_releation where to_id=%s and status=0"
        pars=[userid]
        list=dbConnection.query(sql,*pars)
        return list

    def get_user_friend(self,dbConnection,userid,afriTime):
        """
        获取用户的好友
        :return:
        """
        result_list = None
        if userid:
            if afriTime == 0:
                sql = u"select * from user_friend_releation where (from_id=%s or to_id=%s) and status=1 order by mt_ct desc"
                pars = [userid,userid]
            else :
                sql = u"select * from user_friend_releation where (from_id=%s or to_id=%s) and status=1 and mt_ct>%s order by mt_ct desc"
                pars = [userid,userid,afriTime]
            result_list = dbConnection.query(sql, *pars)
        return result_list

    def get_is_addrecord_relation(self,dbConnection,fromdid, toid):
        """
        查找是否有添加好友的记录
        :param dbConnection:
        :param userId:
        :return:
        """
        sql=u"select * from user_friend_releation  where from_id=%s and to_id=%s"
        pars = [fromdid,toid]
        list = dbConnection.query(sql,*pars)
        if list:
            return True
        return False

    def update_friend_releation(self,dbConnection,fromid,toid,status):
        if fromid and toid:
            sql=u"update user_friend_releation set status=%s,mt_ct=now() where from_id=%s and to_id=%s"
            pars=(status,fromid,toid)
            try:
                dbConnection.execute(sql,*pars)
            except Exception,e:
                print e
                return False
            return True
        return False

    def update_user_info(self,dbConnection,userid,usernikc,userphonenum):
        """
        更新个人信息
        :param dbConnection:
        :param userid:
        :param usernikc:
        :param userphonenum:
        :return:
        """
        if userid:
            if userphonenum!=1234:
                sql=u"update user_info set user_nick=%s,phone_num=%s,gm_ct=now() where user_id=%s"
                pars=(usernikc,userphonenum,userid)
            else:
                sql=u"update user_info set user_nick=%s,gm_ct=now() where user_id=%s"
                pars=(usernikc,userid)
            try:
                dbConnection.execute(sql,*pars)
            except Exception,e:
                print e
                return False
            return True
        return False


    def insert(self,dbConnection):
        sql = u"insert into my_user_address(address,gmt_created,gmt_modified) value('zhejiang',now(),now())"
        dbConnection.execute(sql)

    def insertUserInfoTabel(self,userId,userNick,dbConnection):
        if userId and userNick:
            sql = u"insert into user_info(user_id,user_nick,tm_ct) value(%s,%s,now())"
            pars=[userId, userNick]
            dbConnection.execute(sql, *pars)

    def insertFriendRelation(self,from_userid,to_userid,status,dbConnection):
        """
         插入好友关系
        :param userId:
        :param userNick:
        :param dbConnection:
        :return:
        """
        if from_userid and to_userid:
            sql = u"insert into user_friend_releation(from_id,to_id,status,tm_ct,mt_ct) value(%s,%s,%s,now(),now())"
            pars=[from_userid, to_userid, status]
            dbConnection.execute(sql, *pars)

    def inser_user_deviceToken(self,dbConnection,userid,deviceToken):
        """
        插入用户的device token  给push用的
        :param dbConnection:
        :param userid:
        :param deviceToken:
        :return:
        """
        sql=u"insert into user_device_token(user_id,user_token,token_ct) value(%s,%s,now())"
        pars=[userid,deviceToken]
        dbConnection.execute(sql, *pars)

    def getUserToken(self,dbConnection,userid):
        """
        获取当前用户的token
        :param dbConnection:
        :param userid:
        :return:
        """
        if userid:
            sql=u"select user_token from user_device_token where user_id=%s order by token_ct Desc limit 1"
            pars=[userid]
            list=dbConnection.query(sql, *pars)
        return list
