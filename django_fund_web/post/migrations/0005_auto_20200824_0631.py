# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-08-23 22:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20200824_0628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post_comment_model',
            name='theme_id',
            field=models.CharField(max_length=20, verbose_name='帖子/主题id'),
        ),
    ]