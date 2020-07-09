import time

import pymysql
import redis


r = redis.Redis(host="127.0.0.1",port=6379,db=14)

def update_user_like_article(conn,cursor):

    hash_ua = r.hgetall('user_like_article')
    cursor = conn.cursor()

    sql1 = "select id,status from t_user_like_article where article_id = '{}' " \
           "and username = '{}'"
    sql_insert = "insert into t_user_like_article(article_id,username,status) values" \
                 "('{}','{}','{}')"
    sql_update = "update t_user_like_article set status = {} where id = {}"
    for k,v in hash_ua.items():
        info = k.decode().split('::')
        cursor.execute(sql1.format(info[0],info[1]))
        s1 = cursor.fetchone()

        if s1 is None:
            cursor.execute(sql_insert.format(info[0], info[1],1))

        elif s1[1] != v.decode():
            cursor.execute(sql_update.format(v.decode(),s1[0]))




def update_article_like_count(conn,cursor):
    hash_ac = r.hgetall('all_like_count')
    sql1 = "select article_id,like_count from t_like_count where article_id = %s"
    sql_insert = "insert into t_like_count(article_id,like_count,update_time) values" \
                 "(%s,%s,%s)"
    sql_update = "update t_like_count set like_count = %s,update_time = %s where article_id = %s"
    for k,v in hash_ac.items():
        artId = k.decode()
        count = v.decode()

        cursor.execute(sql1,artId)
        s1 = cursor.fetchone()

        if not s1:
            cursor.execute(sql_insert,(artId,count,time.gmtime()))
        elif s1[1] != int(count):
            print(s1)
            print(type(s1[1]))
            cursor.execute(sql_update.format(count, time.gmtime(), artId))




if __name__ == '__main__':
    connect = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                           passwd='123456', db='fund_web')
    cursor = connect.cursor()
    try:
        update_user_like_article(conn=connect, cursor=cursor)
        update_article_like_count(conn=connect,cursor=cursor)

    except Exception as e:
        print(e)
        connect.rollback()
    else:
        connect.commit()
        print('更新完成!')
    finally:
        cursor.close()
        connect.close()







