from django.contrib import admin

from post.models import Post_bar_model, Post_title_model, Post_comment_model


@admin.register(Post_bar_model)
class postBarManager(admin.ModelAdmin):
    list_display = ['b_code', 'name', 'b_type', 'kind', 'sort',
                    't_sort', 'post_count', 'create_user']

    list_display_links = ['name']
    list_filter = [ 'b_type','kind',]
    search_fields = ['b_code', 'name']
    list_editable = ['sort','t_sort']

@admin.register(Post_title_model)
class postTitleManager(admin.ModelAdmin):
    list_display = ['theme', 'get_authorname', 'post_type', 'comment_count',
                    'sort', 't_sort', 'has_image']

    list_display_links = ['theme']
    list_filter = ['theme', 'post_type', ]
    search_fields = ['title']
    list_editable = ['sort', 't_sort','post_type']

    def get_bname(self, obj):
        return '%s' % obj.b_id.name
    get_bname.short_description = '贴吧名称'

    def get_authorname(self, obj):
        return '%s' % obj.author.name
    get_authorname.short_description = '作者'

@admin.register(Post_comment_model)
class postCommentManager(admin.ModelAdmin):
    list_display = ['p_id', 'content', 'get_uname', 'reply_count', 'parent_id', 'sort',
                    'equ_type_id', 'update_time']

    list_display_links = ['p_id']
    list_filter = ['p_id', 'equ_type_id', ]
    search_fields = ['p_id','content', 'get_uname']
    list_editable = ['sort',]

    def get_uname(self, obj):
        return '%s' % obj.author.name
    get_uname.short_description = '作者'