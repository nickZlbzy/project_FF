# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-02-12 06:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fund_company',
            name='c_id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='公司id'),
        ),
        migrations.AlterField(
            model_name='fund_type',
            name='t_id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='类型id'),
        ),
    ]