# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-03-04 00:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20200205_0826'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article_info_model',
            fields=[
                ('create_time', models.DateField(auto_now_add=True)),
                ('update_time', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=1)),
                ('remarks', models.CharField(blank=True, default='', max_length=50)),
                ('article_id', models.CharField(max_length=25, primary_key=True, serialize=False, verbose_name='唯一id')),
                ('title', models.CharField(max_length=20, verbose_name='标题')),
                ('url', models.CharField(default='', max_length=50, verbose_name='所属模块')),
                ('content', models.CharField(default='', max_length=4000, verbose_name='文章正文')),
                ('author', models.CharField(default='', max_length=32, verbose_name='作者')),
                ('next', models.CharField(default='', max_length=25, verbose_name='下一个')),
            ],
            options={
                'verbose_name': '文章正文表',
                'verbose_name_plural': '文章正文表',
                'db_table': 't_article_info',
            },
        ),
        migrations.CreateModel(
            name='Article_level_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now_add=True)),
                ('update_time', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=1)),
                ('remarks', models.CharField(blank=True, default='', max_length=50)),
                ('lid', models.CharField(max_length=20, verbose_name='分级id')),
                ('title', models.CharField(max_length=20, verbose_name='标题')),
                ('kind', models.CharField(db_index=True, max_length=20, verbose_name='文章类别')),
                ('module', models.CharField(default='', max_length=20, verbose_name='所属模块')),
                ('url', models.CharField(default='', max_length=50, verbose_name='所属模块')),
                ('parent_id', models.CharField(default=0, max_length=20, verbose_name='父级id')),
            ],
            options={
                'verbose_name': '文章分级表',
                'verbose_name_plural': '文章分级表',
                'db_table': 't_article_level',
            },
        ),
        migrations.AddField(
            model_name='article_info_model',
            name='lid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article_level_model'),
        ),
    ]
