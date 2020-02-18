from django.db import models

# Create your models here.
from base.BaseModel import BaseModel


class User_profile_model(BaseModel):
    username=models.CharField("用户名",max_length=32,unique=True)
    password=models.CharField("密码",max_length=128)
    email=models.EmailField("邮箱",db_index=True)
    phone=models.CharField("手机号码",max_length=25,db_index=True)
    gender=models.CharField("性别", max_length=3,default="",blank=True)
    nickname = models.CharField("昵称", max_length=16,default="",blank=True)
    age=models.IntegerField("年龄",default=0,blank=True)
    ability = models.IntegerField("风险能力",default=0,blank=True)
    preference = models.IntegerField("风险偏好",default=0,blank=True)
    uid=models.CharField('第三方id',max_length=32,default="",blank=True)
    is_active = models.BooleanField(default=0)

    class Meta:
        db_table="user_profile"
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name
        ordering = ('-id',)

    def __str__(self):
        return "用户名:%s 邮箱:%s 昵称:%s 性别:%s 年龄:%s"%(self.username,self.email,self.nickname
                 ,self.gender,self.age,)



