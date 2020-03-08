from django.db import models
from base.BaseModel import BaseModel


class Article_model(BaseModel):
    title = models.CharField("标题",max_length=50)
    url = models.CharField("路径",max_length=60,blank=True)
    article_type = models.CharField("类型",max_length=20)
    module_type = models.CharField("所属板块",max_length=20,default="")
    article_id = models.CharField("文章id",max_length=20,unique=True)
    parent_id = models.CharField("父标题id", max_length=20, default=0)
    author = models.CharField("作者", max_length=32, db_index=True,blank=True,default="")
    content = models.CharField("正文",max_length=4000,blank=True,default="")
    sort = models.IntegerField("排序",default=0)

    class Meta:
        db_table = 't_article'
        verbose_name = '文章讯息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "标题:%s ,类型:%s ,板块:%s ,文章id:%s ,父标题id:%s"%(self.title,
            self.article_type,self.module_type,self.article_id,self.parent_id)

class Article_level_model(BaseModel):
    lid = models.CharField("分级id",max_length=20,)
    title = models.CharField("标题",max_length=20)
    kind = models.CharField("文章类别",max_length=20,db_index=True)
    module = models.CharField("所属模块",max_length=20,default="")
    url = models.CharField("所属模块",max_length=50,default="")
    parent_id = models.CharField("父级id",max_length=20,default=0)

    class Meta:
        db_table = 't_article_level'
        verbose_name = '文章分级表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "标题:%s ,文章类别:%s ,所属模块:%s ,父级id:%s" % (self.title,
                 self.kind, self.module, self.parent_id)


class Article_info_model(BaseModel):
    article_id = models.CharField("唯一id",max_length=25,primary_key=True)
    title = models.CharField("标题", max_length=20)
    url = models.CharField("所属模块", max_length=50, default="")
    content = models.CharField("文章正文", max_length=4000, default="")
    author = models.CharField("作者", max_length=32, default="")
    next = models.CharField("下一个", max_length=25, default="")
    lid = models.ForeignKey(Article_level_model)

    class Meta:
        db_table = 't_article_info'
        verbose_name = '文章正文表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "文章id:%s ,标题:%s ,作者:%s ,下一篇:%s" % (self.article_id,self.title,
                  self.author, self.parent_id)

    def get_next_id(self):
        pass