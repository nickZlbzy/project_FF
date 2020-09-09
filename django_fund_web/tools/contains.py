"""
    项目常量配置类
"""

#用户系统头像默认路径前缀
DEFAULT_PRE_USER_IMAGE = "/static/images/"

# cookies存储7天
COOKIES_KEEP_TIME = 60*60*24*7

# 首页过期时间
INDEX_KEEP_TIME = 60*60*12

#短信验证码过期时间
MOBILE_KEEP_TIME = 60

# 点赞状态 1,赞 2，取消
LIKE_STATUS = 1
LIKE_CANCEL_STATUS = 0

# 基金吧路径前缀
PRE_BAR_URL = "/post/bars/"
PRE_COMMENT_URL = "/post/themes/"

# 分页栏最大页码数
DEFAULT_MAX_PAGE = 8
# diy分页，默认双边页数
DEFAULT_BOTH_PAGE = 5