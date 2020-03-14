## 睿选基金网

***

### 数据库设计 (表)
1. t_user	                      用户管理表

2. t_risk_evalution     会员风险评估表

3. t_article            投资文章,资讯管理表               

4. t_comment               有问题，找专家(用户评论表)

5. t_fund_filter             基金信息筛选表

6. t_fund_type              基金类别表：与基金信息表type字段为一对一关系。

7. t_fund_company    基金公司信息表 ：会与基金信息表company_id字段为一对                

   ​                                        一关系。

8. system_dict                            项目字典表：可用于前端下拉菜单组件，存储项目中为键值                 					                    对结构的数据

9. t_log                             操作日志记录表：记录增删改相关操作

10. t_fund_payment        基金订单交易管理表

    

### 后台API
1. base   基础类

1. user   	用户模块

2. filter      基金筛选模块

3. article         资讯与点赞模块

4. system          系统管理模块

5. index      首页模块

   

### 前端功能

- 资讯，基金信息动态更新
- 后台管理
- 注册登录
- 模糊查询等表单提交
- 风险测评

### 模块负责人

- 首页：石镏金，钟超 ;          		用户管理模块：肖睿，余胜豪 ;          风险评估：陈胜;  
- 基金筛选模块：花花，钟超，肖睿;  								
- 美工，样式：缺省

重要：1.项目环境：

- Dajngo,

-  redis,

-  celery ：项目根路径下执行，创建worker                                   

  ```she
  celery -A django_fund_web worker -l info   
  ```

  