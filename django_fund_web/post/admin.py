from django.contrib import admin

from post.models import Post_bar_model, Post_title_model, Post_comment_model
from tools import contains
from tools.utils import Utils
from django.db.models import Max

from user.mappers import User_mapper


@admin.register(Post_bar_model)
class postBarManager(admin.ModelAdmin):
    list_display = ['bid', 'name', 'fund_code', 'b_type', 'kind', 'sort',
                    't_sort', 'post_count', 'create_user']

    list_display_links = ['name']
    list_filter = [ 'b_type','kind',]
    search_fields = ['bid', 'name']
    list_editable = ['sort','t_sort']


    def save_model(self, request, obj, form, change):
        if not change:
            obj.bid = Utils.get_sync("post_bar")
            obj.url = contains.PRE_BAR_URL + obj.bid
            obj.create_user = request.user.username
            if not obj.sort:
                max_num = Post_bar_model.objects.aggregate(max_num=Max('sort'))['max_num']
                obj.sort =  max_num + 10 if max_num or max_num==0  else 0
        else:
            obj.update_user=request.user.username
        obj.save()







@admin.register(Post_title_model)
class postTitleManager(admin.ModelAdmin):
    list_display = ['tid','theme', 'get_authorname', 'get_barname', 'post_type', 'comment_count',
                    'sort', 't_sort', 'has_image','update_time']

    list_display_links = ['theme']
    list_filter = ['theme', 'post_type', ]
    search_fields = ['title']
    list_editable = ['sort', 't_sort','post_type']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.tid = Utils.get_sync("post_theme")
            if not obj.sort:
                max_num = Post_title_model.objects.aggregate(max_num=Max('sort')).filter(
                    bar_id=obj.bar_id)['max_num']
                obj.sort =  max_num + 10 if max_num else 10 #sort字段默认从10开始
        obj.save()


    def get_barname(self, obj):
        # return '%s' % obj.bar
        return '%s' % obj.bar.name if obj.bar else '未知'
    get_barname.short_description = '贴吧名称'

    def get_authorname(self, obj):
        return '%s' % User_mapper.get_user_nickname(obj.author)
    get_authorname.short_description = '作者'

@admin.register(Post_comment_model)
class postCommentManager(admin.ModelAdmin):
    list_display = ['id', 'content', 'get_uname', 'revert_count', 'parent_id', 'sort',
                    'equ_type_id', 'update_time']

    list_display_links = ['id']
    list_filter = ['theme_id', 'equ_type_id', ]
    search_fields = ['id','content', 'get_uname']
    list_editable = ['sort',]

    def get_uname(self, obj):
        return '%s' % User_mapper.get_user_nickname(obj.author)
    get_uname.short_description = '作者'