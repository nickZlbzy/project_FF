from django.contrib import admin

# Register your models here.
from system.models import Project_dict, Title_url_model


class dictManager(admin.ModelAdmin):
    list_display = ['type','valid','value','sort']
    # 列表页用于跳转详情的字段
    list_display_links = ['value']
    list_filter = ['type']
    search_fields = ['type','value']
    list_editable = ['sort']


class cateManager(admin.ModelAdmin):
    list_display = ['title','url','type','parent_id','sort']
    list_display_links = ['title','url']
    list_filter = ['type','parent_id']
    search_fields = ['type', 'title']
    list_editable = ['sort']



admin.site.register(Project_dict, dictManager)
admin.site.register(Title_url_model, cateManager)