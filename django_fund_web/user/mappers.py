from django.db import connection


class User_mapper:

    @staticmethod
    def check_new(kind,value):
        sql = "select id from user_profile where %s='%s' "%(kind,value)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            re = cursor.fetchall()
        return re
