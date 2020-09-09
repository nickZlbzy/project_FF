from django.db import connection

from user.models import User_profile_model
from tools import contains

class User_mapper:

    @staticmethod
    def check_new(kind,value):
        sql = "select id from user_profile where %s='%s' "%(kind,value)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            re = cursor.fetchall()
        return re

    @staticmethod
    def get_user_nickname(username):
        try:
            userObj = User_profile_model.objects.values_list('nickname').get(username=username)
            return userObj[0] if userObj[0] else username
        except:
            return username

    @staticmethod
    def get_user_info(username):
        """

        :param username:
        :return: userinfo(username,nickname,userImg,userUrl)
        """
        userinfo={}
        try:
            userObj = User_profile_model.objects.values('username','nickname','user_img'
                            ).get(username=username,live_flag=1)
        except Exception as e:
            userinfo['nickname'] = "未知"
            userinfo['userimg'] = contains.DEFAULT_PRE_USER_IMAGE + "userImg/0.jpg"
            userinfo['userurl'] = "#"
            return userinfo
        userinfo['username'] = userObj.get('username')
        userinfo['nickname'] = userObj.get('nickname') if userObj.get('nickname') else userObj.get('username')
        userinfo['userimg'] = contains.DEFAULT_PRE_USER_IMAGE + userObj.get('user_img')
        userinfo['userurl'] = "#"
        return userinfo