# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-08-23 22:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20200823_1957'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='post_comment_model',
            index_together=set([('theme_id', 'revert_to')]),
        ),
    ]
