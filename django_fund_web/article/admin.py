from django.contrib import admin

# Register your models here.
from article.models import *

@admin.register(Article_info_model)
class ArticleInfoManager(admin.ModelAdmin):
    list_display = ['title', 'url', 'article_id', 'get_lname', 'author','sort','next']
    list_display_links = ['title', 'url']
    list_filter = ['level__title', 'author']
    search_fields = [ 'title', 'author']
    list_editable = ['sort']

    def get_lname(self, obj):
        return '%s' % obj.level.title
    get_lname.short_description = '分类名'

@admin.register(Article_level_model)
class ArticleLevelManager(admin.ModelAdmin):
    list_display = ['lid','title','kind','module', 'url', 'parent_id' , 'sort']
    list_display_links = ['title']
    list_filter = ['module', 'kind','parent_id']
    search_fields = ['lid', 'title']
    list_editable = ['sort']

