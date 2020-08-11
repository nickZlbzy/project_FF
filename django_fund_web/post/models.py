from base.BaseModel import *
from user.models import User_profile_model

class Post_bar_model(BaseModel):
    b_code = models.CharField("基金吧编号",max_length=20,primary_key=True)
    name = models.CharField("名称", max_length=50, db_index=True)
    url = models.CharField("贴吧路径", max_length=50)
    b_type =  models.SmallIntegerField('贴吧类型',default=1)
    kind = models.CharField('板块类型',max_length=20,default=0)
    sort = models.IntegerField('排序', default=0)
    t_sort = models.IntegerField('置顶排序', default=0)
    post_count = models.IntegerField('帖子数量', default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    create_user = models.CharField("创建人",max_length=32)
    update_user = models.CharField("修改人",max_length=32)

    class Meta:
        db_table = 't_post_bar'
        verbose_name = '基金吧表'
        verbose_name_plural = verbose_name
        ordering = ['t_sort', 'sort']

    def __str__(self):
        return "编号:%s ,名称:%s ,帖子数量:%s " % (self.b_code, self.name, self.post_count)


class Post_title_model(BaseModel):
    theme = models.CharField("主题",max_length=50,db_index=True)
    author = models.OneToOneField(User_profile_model)
    b_id = models.IntegerField('贴吧id')
    post_type = models.SmallIntegerField('帖子类型')
    url = models.CharField("路径", max_length=50)
    comment_count = models.IntegerField('评论数',default=0)
    sort = models.IntegerField('排序',default=0)
    t_sort = models.IntegerField('置顶排序', default=0)
    has_image = models.SmallIntegerField('图片贴',default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 't_post_title'
        verbose_name = '贴吧标题表'
        verbose_name_plural = verbose_name
        ordering = ['t_sort','-sort']

    def __str__(self):
        return "主题:%s ,基金编号:%s ,作者:%s " % (self.theme,self.bar_code, self.author)

class Post_comment_model(BaseModel):
    p_id = models.ForeignKey(Post_title_model, related_name='pid')
    content = models.CharField("评论内容",max_length=150,db_index=True)
    author = models.OneToOneField(User_profile_model)
    reply_count = models.IntegerField('回复数', default=0)
    parent_id = models.IntegerField('父评论id', default=0)
    reply_id = models.CharField('回复id',max_length=32 ,default=None)
    sort = models.IntegerField('排序', default=0)
    equ_type_id = models.SmallIntegerField('环境类型',default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_post_comment'
        verbose_name = '贴吧评论表'
        verbose_name_plural = verbose_name
        ordering = ['parent_id','-sort']

    def __str__(self):
        return "帖子id:%s  ,作者:%s ,父评论id:%s" % (self.p_id,self.author, self.parent_id)