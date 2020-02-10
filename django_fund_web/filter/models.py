from django.db import models

# Create your models here.
from base.BaseModel import BaseModel


class Fund_filter_model(BaseModel):
    f_code = models.CharField("编号",max_length=20)
    f_name = models.CharField("基金名称",max_length=50,db_index=True)
    company_id = models.IntegerField("公司id", db_index=True)
    is_oc = models.IntegerField("is_开闭", default=1)
    is_eq = models.IntegerField("is_EQ",default=0)
    f_type_id = models.IntegerField("基金类型id", default=None)
    five_year_level=models.FloatField("五年评级", default=0)
    three_year_level=models.FloatField("三年评级", default=0)
    unit_price = models.CharField("单位净值",max_length=30,default=None)
    day_change = models.DecimalField("日变动",max_digits=5,decimal_places=4,default=None)
    interest=models.DecimalField("今年来回报",max_digits=6,decimal_places=2,default=None)

    class Meta:
        db_table = 't_fund_filter'
        verbose_name = '基金筛选表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "编号:%s ,名称:%s ,类型:%s ,if_开闭:%s"%(self.f_code,
            self.f_name,self.f_type_id,self.is_oc)


class Fund_type(BaseModel):
    t_id = models.AutoField("类型id", primary_key=True, auto_created=True, serialize=False)
    type_name = models.CharField("基金类型",max_length=128)
    sort = models.IntegerField("排序",default=None)

    class Meta:
        db_table = 't_fund_type'
        verbose_name = '基金类型表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "类型id:%s ,名称:%s"%(self.t_id,self.type_name)

class Fund_company(BaseModel):
    c_id = models.AutoField("公司id", primary_key=True, auto_created=True, serialize=False)
    c_name = models.CharField("名称",max_length=60)
    sort = models.IntegerField("排序", default=None)
    create_user = models.CharField("创建人",max_length=32, default=None,blank=True)


    class Meta:
        db_table = 't_fund_company'
        verbose_name = '基金公司表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "公司id:%s ,名称:%s"%(self.c_id,self.c_name)




