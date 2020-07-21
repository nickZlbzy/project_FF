from django.contrib import admin

# Register your models here.
from django_redis import get_redis_connection

from system.models import Project_dict, Title_url_model, Sync_code
redis_conn = get_redis_connection('project_dict')

@admin.register(Project_dict)
class dictManager(admin.ModelAdmin):
    list_display = ['type','valid','value','sort','remarks']
    # 列表页用于跳转详情的字段
    list_display_links = ['type','value']
    list_filter = ['type','remarks']
    search_fields = ['type','value']
    list_editable = ['sort']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # 删除项目字典缓存
        redis_conn.flushdb()
        print("删除字典缓存")

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        redis_conn.flushdb()
        # 删除项目字典缓存
        print("删除字典缓存")



@admin.register(Title_url_model)
class cateManager(admin.ModelAdmin):
    list_display = ['id','title','url','type','module','parent_id','sort']
    list_display_links = ['title','url']
    list_filter = ['type','module','parent_id']
    search_fields = ['type', 'title']
    list_editable = ['parent_id','sort']


@admin.register(Sync_code)
class syncManager(admin.ModelAdmin):
    pass

