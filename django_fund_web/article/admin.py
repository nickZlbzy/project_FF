from django.contrib import admin

# Register your models here.
from article.models import Article_model


class articleManager(admin.ModelAdmin):
    list_display = ['title', 'url', 'article_id', 'article_type', 'parent_id', 'author','sort']
    list_display_links = ['title', 'url']
    list_filter = ['module_type','article_type', 'parent_id', 'author']
    search_fields = ['article_type', 'title', 'author']
    list_editable = ['sort']


admin.site.register(Article_model,articleManager)
