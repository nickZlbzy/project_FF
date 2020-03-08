from django.contrib import admin

# Register your models here.
from article.models import *

@admin.register(Article_info_model)
class ArticleInfoManager(admin.ModelAdmin):
    pass
    # list_display = ['title', 'url', 'article_id', 'article_type', 'parent_id', 'author','sort']
    # list_display_links = ['title', 'url']
    # list_filter = ['module_type','article_type', 'parent_id', 'author']
    # search_fields = ['article_type', 'title', 'author']
    # list_editable = ['sort']

@admin.register(Article_level_model)
class ArticleLevelManager(admin.ModelAdmin):
    pass



admin.site.register(Article_model)