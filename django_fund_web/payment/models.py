from base.BaseModel import *
from user.models import User_profile_model


class Fund_payment_model(BaseModel):
    order_code = models.CharField("订单号",max_length=32,db_index=True)
    fund_code = models.CharField("基金编号",max_length=20,db_index=True)
    price = models.DecimalField('单价',max_digits=5,decimal_places=2)
    total = models.IntegerField('数量',default=1)
    amount = models.DecimalField('总金额',max_digits=8,decimal_places=2)
    status = models.SmallIntegerField('订单状态',default=1)
    uid = models.ForeignKey(User_profile_model)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_fund_payment'
        verbose_name = '订单管理表'
        verbose_name_plural = verbose_name
        ordering = ['status','-create_time']

    def __str__(self):
        return "订单号:%s ,基金编号:%s ,金额:%s " % (self.order_code,self.fund_code, self.amount)





