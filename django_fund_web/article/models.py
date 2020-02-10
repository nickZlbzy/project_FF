from django.db import models

# Create your models here.
from django.db.models import CharField, IntegerField

from base.BaseModel import BaseModel


class Article_model(BaseModel):
    title = CharField("标题",max_length=50)
    url = CharField("路径",max_length=60,blank=True)
    article_type = CharField("类型",max_length=20)
    module_type = CharField("所属板块",max_length=20,default="")
    article_id = CharField("文章id",max_length=20,unique=True)
    parent_id = CharField("父标题id", max_length=20, default=0)
    author = CharField("作者", max_length=32, db_index=True,blank=True,default="")
    content = CharField("正文",max_length=4000,blank=True,default="")
    sort = IntegerField("排序",default=0)

    class Meta:
        db_table = 't_article'
        verbose_name = '文章讯息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "标题:%s ,类型:%s ,板块:%s ,文章id:%s ,父标题id:%s"%(self.title,
            self.article_type,self.module_type,self.article_id,self.parent_id)
