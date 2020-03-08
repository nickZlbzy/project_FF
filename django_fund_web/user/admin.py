from django.contrib import admin

# Register your models here.

from user.models import User_profile_model


class userProfileManager(admin.ModelAdmin):

    list_display = ['username','email','phone','nickname','age']
    # 列表页用于跳转详情的字段
    list_display_links = ['username']
    list_filter = ['gender']
    search_fields = ['username','nickname','phone']
    list_editable = []


admin.site.register(User_profile_model,userProfileManager)