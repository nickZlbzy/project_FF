from base.BaseModel import *
from tools.utils import Utils
from user.models import User_profile_model

class Post_bar_model(BaseModel):
    bid = models.CharField("基金吧id", max_length=20, primary_key=True,editable=False)
    name = models.CharField("名称", max_length=50, db_index=True)
    fund_code = models.CharField("基金编号", max_length=20,db_index=True, blank=True)
    url = models.CharField("贴吧路径", max_length=50,editable=False)
    b_type =  models.SmallIntegerField('贴吧类型',default=1)
    kind = models.CharField('板块类型',max_length=20,default=0)
    sort = models.IntegerField('排序', default=0)
    t_sort = models.IntegerField('置顶排序', default=0)
    post_count = models.IntegerField('帖子数量', default=0,editable=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    create_user = models.CharField("创建人",max_length=32,editable=False)
    update_user = models.CharField("修改人",max_length=32,default="",editable=False)

    class Meta:
        db_table = 't_post_bar'
        verbose_name = '基金吧表'
        verbose_name_plural = verbose_name
        ordering = ['-t_sort', '-sort']

    def __str__(self):
        return "编号:%s ,名称:%s ,帖子数量:%s " % (self.bid, self.name, self.post_count)


class Post_title_model(BaseModel):
    tid = models.CharField("唯一id",max_length=20,primary_key=True,editable=False)
    theme = models.CharField("主题",max_length=50,db_index=True)
    t_content = models.CharField("主题内容", max_length=150)
    author = models.CharField('作者',max_length=32,db_index=True)
    bar = models.ForeignKey('Post_bar_model', related_name='barinfo',null=True,blank=True,
                                 on_delete=models.SET_NULL)
    post_type = models.SmallIntegerField('帖子类型',default=1)
    url = models.CharField("路径", max_length=50,editable=False)
    comment_count = models.IntegerField('评论数',default=0,editable=False)
    sort = models.IntegerField('排序',default=0)
    t_sort = models.IntegerField('置顶排序', default=0)
    has_image = models.BooleanField('图片贴',default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 't_post_title'
        verbose_name = '贴吧标题表'
        verbose_name_plural = verbose_name
        ordering = ['-t_sort','-update_time']

    def __str__(self):
        return "id:%s,主题:%s ,评论数:%s ,作者id:%s " % (self.tid,self.theme,self.comment_count, self.author)

class Post_comment_model(BaseModel):
    theme_id = models.CharField('帖子/主题id',max_length=20)
    content = models.CharField("评论内容",max_length=350)
    author = models.CharField('作者',max_length=32,db_index=True)
    revert_count = models.IntegerField('回复数', default=0)
    parent_id = models.IntegerField('父评论id', default=0)
    revert_to = models.CharField('回复id',max_length=32 ,default=None)
    sort = models.IntegerField('排序', default=0)
    equ_type_id = models.SmallIntegerField('环境类型',default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_post_comment'
        verbose_name = '贴吧评论表'
        verbose_name_plural = verbose_name
        index_together = (
            ('theme_id', 'revert_to')  # 联合索引
        )
        ordering = ['parent_id','sort']

    def __str__(self):
        return "帖子id:%s  ,作者:%s ,父评论id:%s" % (self.id,self.author, self.parent_id)