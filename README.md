## 睿选基金网

***

### 数据库设计 (表)
1. t_user	                      用户管理表

2. t_risk_evalution     会员风险评估表

3. t_article_level            投资文章,资讯层级管理表     
4.  t_article_info           投资文章,资讯表  

4. t_comment               有问题，找专家(用户评论)表

5. t_fund_filter             基金信息简(筛选)表

6. t_fund_type              基金类别表：与基金信息表type字段一对一关系。

7. t_fund_company    基金公司信息表 ：与基金信息表company_id字段一对                

   ​                                        一关系。

8. system_dict                            项目字典表：可用于前端下拉菜单组件，存储项目中为键值                 					                    对结构的数据

9. t_log                             操作日志记录表：记录增删改相关操作

10. t_fund_payment        基金交易订单管理表

    

### 后台API
1. base   基础类

1. user   	用户模块

2. filter      基金筛选模块

3. article         资讯与点赞模块

4. system          系统管理模块

5. index      首页模块

   

### 前端功能

- 资讯，基金净值动态更新
- 后台管理
- 注册登录
- 模糊查询等表单提交
- 风险测评

### 模块负责人

- self,缺省

重要：1.项目环境：

- Dajngo,

-  redis,

-  celery ：项目根路径下执行，创建worker                                   

  ```she
  celery -A django_fund_web worker -l info   
  ```

- 基金历史净值数据爬虫

  ```html
  天天基金网历史净值数据的页面地址是
  http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=519702&sdate=2010-02-22&edate=2020-08-06&per=65535
  参数说明如下：
  
  type 类型，历史净值用lsjz表示
  code 基金代码，六位数字
  sdate 开始日期，格式是yyyy-mm-dd
  edate 结束日期，格式是yyyy-mm-dd
  per 一页显示多少条记录
  为了便于分析页面数据，要保证所选择日期范围内的净值在一个页面全部显示，可以把per设成很大的值，比如65535。
  
  
  export RABBIT_HOME=/usr/local/Cellar/rabbitmq/3.8.8
  export PATH=$PATH:$RABBIT_HOME/sbin
  
  ```

- 服务器地址

  ```shell
  $ ssh root@120.79.178.190
  ```

  
