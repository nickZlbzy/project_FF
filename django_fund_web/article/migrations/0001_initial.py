# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-04-13 02:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now_add=True)),
                ('update_time', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=1)),
                ('remarks', models.CharField(blank=True, default='', max_length=50)),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('url', models.CharField(blank=True, max_length=60, verbose_name='路径')),
                ('article_type', models.CharField(max_length=20, verbose_name='类型')),
                ('module_type', models.CharField(default='', max_length=20, verbose_name='所属板块')),
                ('article_id', models.CharField(max_length=20, unique=True, verbose_name='文章id')),
                ('parent_id', models.CharField(default=0, max_length=20, verbose_name='父标题id')),
                ('author', models.CharField(blank=True, db_index=True, default='', max_length=32, verbose_name='作者')),
                ('content', models.CharField(blank=True, default='', max_length=4000, verbose_name='正文')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
            ],
            options={
                'verbose_name': '文章讯息',
                'verbose_name_plural': '文章讯息',
                'db_table': 't_article',
            },
        ),

    ]
