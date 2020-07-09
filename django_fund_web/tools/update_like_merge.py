"""
 合并redis中的点赞到数据库
"""
import time

import redis
import pymysql

r = redis.Redis(host="127.0.0.1",port=6379,db=14)

def insert_article_like():






    articles = alu = {}
    artIds = r.smembers('art_set')
    while artId:
        artId = artId.decode()
        print(artId)
        if artId not in articles:
            articles[artId] = []
        alu_name = 'art_user_like_set_'+artId
        uname = r.spop(alu_name)
        while uname:
            uname = uname.decode()
            print(uname)
            aulau = 'art_user_like_{}_{}'.format(artId, uname)
            alu = r.hgetall(aulau)
            articles[artId].append(alu)
            uname = r.spop(alu_name)
        artId = r.spop('art_set')
    records = []
    for v in articles.values():
        for record in v:
            records.append((record[b'article_id'].decode(),
                            record[b'uname'].decode(),
                            time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(record[b'ctime'].decode())))
                            ))

    save_like_records(records)

def save_like_records(records):
    """
    将记录批量if len(records) == 1:
        records = 存入mysql
    :param records:  记录s
    :return:
    """
    if not records:
        return

    cursor = conn.cursor()

    print(records)
    try:
        sql = "insert into t_user_like_article(article_id,username,ctime) values(%s,%s,%s)"
        cursor.executemany(sql, records)  # 执行插入数据


        print('insert ok')
    except Exception as e:
        conn.rollback()
        print(e)
    else:
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def insert_like_count():
    sql_sel= 'select article_id,like_count from t_article_count'







if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                           passwd='123456', db='fund_web')
    insert_article_like()



