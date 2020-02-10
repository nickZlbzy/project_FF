from django.contrib import admin

# Register your models here.
from filter.models import Fund_filter_model, Fund_company, Fund_type


class fundFilterManager(admin.ModelAdmin):
    list_display = ['f_code', 'f_name', 'is_oc', 'interest']
    list_display_links = ['f_code', 'f_name']
    list_filter = ['is_oc']
    search_fields = ['f_code', 'f_name']
    list_editable = []

admin.site.register(Fund_filter_model,fundFilterManager)
admin.site.register(Fund_type)
admin.site.register(Fund_company)