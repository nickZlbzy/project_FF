import hashlib,pymysql,datetime,sys,re
def my_db(sql):
    import pymysql
    coon = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     password='123456',
                     database='test',
                     charset='utf8')
    cur = coon.cursor()#建立游标
    cur.execute(sql)#执行sql
    # if sql.strip()[:].upper() == 'SELECT':
    register = cur.fetchall()
    # else:
    coon.commit()
    # register = 'ok'
    cur.close()
    coon.close()
    return register

# def my_md5(str):
#     import hashlib
#     new_str = str.encode()#吧字符串转成bytes类型
#     m = hashlib.md5()#实例化md5对象
#     m.update(new_str)#加密
#     return m.hexdigest()#获取返回结果

def register():
    username = input("请输入用户名:").strip().lower()
    pwd = input("请输入密码:").strip()
    cpwd = input('请再次输入密码:').strip()
    email = input("请输入邮箱:")
    phone = input("请输入手机号码:")
    if username and email and phone and pwd:
        sql = 'select * from t_user where username = "%s";'%username
        if len(username) not in range(6, 11) or len(pwd) not in range(6, 11) :
            print('账号/密码长度必须在6-10之间')
        res = my_db(sql)
        if res:
            print("该用户已经存在！")

        sql = 'select * from t_user where email = "%s";' %email
        res1 = my_db(sql)
        if res1:
            print("邮箱已经存在!")

        sql = 'select * from t_user where phone = "%s";' %phone
        if len(phone)!= 11:
            print("你输入的号码长度有误")
        res2 = my_db(sql)
        if res2:
            print("电话已经存在!")
        else:
            if pwd == cpwd:
                # md5_pwd = my_md5(pwd)
                insert_sql = 'insert into t_user (username,password,email,phone) values ("%s","%s","%s","%s");'\
                             %(username,pwd,email,phone)
                my_db(insert_sql)
                print("注册成功！")
            else:
                print('两次输入的密码不一致！')
    else:
        print('必填项不能为空！')

def login():
    username = input('请输入用户名:').strip()
    pwd = input('请输入密码:').strip()
    if username and pwd:
        # md5_pwd = my_md5(pwd)
        sql = 'select * from t_user where username = "%s" and pwd = "%s";'%(username,pwd)
        res = my_db(sql)
        if res:
            print("欢迎，登陆成功！今天是%s"%datetime.date.today())
        else:
            print('账号或密码错误')
    else:
        print("必填项不能为空！")
#login()
def main():
    while True:
        print("""
        ============Welcome============
         1. 注册    2. 登录     3. 退出
        ============Welcome============
        """)
        while True:
            opt = input('请输入你的选项:')
            if opt == '1':
                register()
            if opt == '2':
                login()
            if opt == '3':
                print('您已退出登录~!')
                sys.exit()
main()
register()