from django.db import models

# Create your models here.
from django.db.models import CharField, IntegerField
from base.BaseModel import BaseModel


class Project_dict(BaseModel):
    type = CharField("类型",max_length=20,db_index=True)
    valid = IntegerField("Key",db_index=True)
    value = CharField("Value",max_length=32)
    sort = IntegerField("排序", default=0)
    create_user = CharField("创建人",max_length=32, default=None, blank=True)


    class Meta:
        db_table = 'system_dict'
        verbose_name = '项目字典'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "类别:%s Key:%s Value:%s"%(self.type,self.valid,self.value)


class Title_url_model(BaseModel):
    url = CharField("路径",max_length=80, default="")
    title = CharField("标题", max_length=50)
    type = CharField("类型", max_length=20, db_index=True)
    sort = IntegerField("排序", default=0)
    parent_id = IntegerField("父标题id", default=0)

    class Meta:
        db_table = 't_title_url'
        verbose_name = '标题路径对应表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'title=%s, url=%s, type=%s, parent_id=%s>' \
               % (self.title, self.url, self.type, self.parent_id)