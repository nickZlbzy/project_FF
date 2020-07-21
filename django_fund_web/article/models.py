from datetime import datetime

from django.db import models
from base.BaseModel import BaseModel


class Article_level_model(BaseModel):
    lid = models.CharField("分级id",max_length=20,primary_key=True)
    title = models.CharField("标题",max_length=36)
    kind = models.CharField("文章类别",max_length=20,db_index=True)
    module = models.CharField("所属模块",max_length=20,default="")
    url = models.CharField("URL",max_length=50,default="")
    parent_id = models.CharField("父id",max_length=20,default=0)
    sort = models.IntegerField("排序", default=None)

    class Meta:
        db_table = 't_article_level'
        verbose_name = '文章分级表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "标题:%s ,文章类别:%s ,所属模块:%s ,父级id:%s" % (self.title,
                 self.kind, self.module, self.parent_id)


class Article_info_model(BaseModel):
    level = models.ForeignKey(Article_level_model,related_name='info',on_delete=models.SET_NULL,null=True)
    article_id = models.CharField("唯一id",max_length=25,primary_key=True)
    title = models.CharField("标题", max_length=36)
    url = models.CharField("路径", max_length=50, default="")
    content = models.CharField("文章正文", max_length=4005, default="")
    author = models.CharField("作者", max_length=32, default="")
    next = models.CharField("下一篇", max_length=36, default="",blank=True)
    next_url = models.CharField("下一url", max_length=50, default="",blank=True)
    sort = models.IntegerField("排序", default=None)

    class Meta:
        db_table = 't_article_info'
        verbose_name = '文章表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "文章id:%s ,标题:%s ,作者:%s " % (self.article_id,self.title,
                  self.author)

    def get_next_id(self):
        pass


class User_like_article(models.Model):
    article_id = models.CharField('文章id',max_length=16)
    username = models.CharField('用户名',max_length=32)
    status = models.BooleanField('点赞状态')
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    update_time = models.DateTimeField('修改时间',auto_now=True)


    class Meta:
        db_table = 't_user_like_article'
        verbose_name = '用户点赞表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "文章id:%s ,用户名:%s ,创建时间:%s " % (self.article_id,self.username,
                  self.ctime)

class Article_like_comment(models.Model):
    article_id = models.CharField('文章id', max_length=16, primary_key=True)
    like_count = models.IntegerField('评论数量',default=0)
    comment_count = models.IntegerField('评论数量',default=0)
    update_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 't_like_count'
        verbose_name = '点赞评论总数'
        verbose_name_plural = verbose_name