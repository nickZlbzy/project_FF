# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-03-06 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20200304_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article_info_model',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='article_info_model',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='article_level_model',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='article_level_model',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='article_model',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='article_model',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
