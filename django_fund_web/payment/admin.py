from django.contrib import admin

# Register your models here.
from payment.models import Fund_payment_model
from system.models import Project_dict
from tools import pro_dict


@admin.register(Fund_payment_model)
class fundPaymentManager(admin.ModelAdmin):
    list_display = ['get_uname', 'order_code', 'fund_code', 'price', 'total',
                    'amount', 'status', 'get_status_name']

    list_display_links = ['order_code']
    list_filter = [ 'status','uid__username',]
    search_fields = ['order_code', 'uid__username']
    list_editable = ['status',]

    def get_uname(self, obj):
        return '%s' % obj.uid.username
    get_uname.short_description = '用户名'

    def get_status_name(self,obj):
        s_name = pro_dict.get_from_dict('pay_status', obj.status,"abc")
        return s_name
    get_status_name.short_description = '订单状态'