# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-08-21 08:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post_bar_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=1)),
                ('remarks', models.CharField(blank=True, default='', max_length=50)),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='名称')),
                ('b_id', models.CharField(blank=True, editable=False, help_text='不可重复，默认不写会自动生成。', max_length=20, unique=True, verbose_name='基金吧id')),
                ('fund_code', models.CharField(blank=True, db_index=True, max_length=20, verbose_name='基金编号')),
                ('url', models.CharField(editable=False, max_length=50, verbose_name='贴吧路径')),
                ('b_type', models.SmallIntegerField(default=1, verbose_name='贴吧类型')),
                ('kind', models.CharField(default=0, max_length=20, verbose_name='板块类型')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('t_sort', models.IntegerField(default=0, verbose_name='置顶排序')),
                ('post_count', models.IntegerField(default=0, editable=False, verbose_name='帖子数量')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_user', models.CharField(editable=False, max_length=32, verbose_name='创建人')),
                ('update_user', models.CharField(default='', editable=False, max_length=32, verbose_name='修改人')),
            ],
            options={
                'verbose_name': '基金吧表',
                'verbose_name_plural': '基金吧表',
                'db_table': 't_post_bar',
                'ordering': ['-t_sort', '-sort', '-id'],
            },
        ),
        migrations.CreateModel(
            name='Post_comment_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=1)),
                ('remarks', models.CharField(blank=True, default='', max_length=50)),
                ('content', models.CharField(max_length=150, verbose_name='评论内容')),
                ('author', models.CharField(db_index=True, max_length=32, verbose_name='作者')),
                ('reply_count', models.IntegerField(default=0, verbose_name='回复数')),
                ('parent_id', models.IntegerField(default=0, verbose_name='父评论id')),
                ('reply_id', models.CharField(default=None, max_length=32, verbose_name='回复id')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('equ_type_id', models.SmallIntegerField(default=1, verbose_name='环境类型')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '贴吧评论表',
                'verbose_name_plural': '贴吧评论表',
                'db_table': 't_post_comment',
                'ordering': ['parent_id', '-sort'],
            },
        ),
        migrations.CreateModel(
            name='Post_title_model',
            fields=[
                ('is_active', models.BooleanField(default=1)),
                ('remarks', models.CharField(blank=True, default='', max_length=50)),
                ('tid', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='唯一id')),
                ('theme', models.CharField(db_index=True, max_length=50, verbose_name='主题')),
                ('t_content', models.CharField(max_length=150, verbose_name='评论内容')),
                ('author', models.CharField(db_index=True, max_length=32, verbose_name='作者')),
                ('bar_id', models.CharField(db_index=True, max_length=20, verbose_name='贴吧id')),
                ('post_type', models.SmallIntegerField(default=1, verbose_name='帖子类型')),
                ('url', models.CharField(max_length=50, verbose_name='路径')),
                ('comment_count', models.IntegerField(default=0, verbose_name='评论数')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('t_sort', models.IntegerField(default=0, verbose_name='置顶排序')),
                ('has_image', models.BooleanField(default=False, verbose_name='图片贴')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '贴吧标题表',
                'verbose_name_plural': '贴吧标题表',
                'db_table': 't_post_title',
                'ordering': ['t_sort', '-sort'],
            },
        ),
        migrations.AddField(
            model_name='post_comment_model',
            name='theme_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='themeinfo', to='post.Post_title_model'),
        ),
    ]
