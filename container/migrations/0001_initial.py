# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-12-07 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('license', models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='车牌号')),
                ('status', models.CharField(choices=[('working', '正在工作'), ('relaxing', '待命'), ('fixing', '维修'), ('losing', '丢失')], default='relaxing', max_length=10, verbose_name='状态')),
            ],
            options={
                'verbose_name_plural': '押款车',
                'verbose_name': '押款车',
            },
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('number', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='编号')),
                ('location', models.CharField(max_length=20, verbose_name='箱子所在地')),
                ('status', models.CharField(choices=[('working', '正在工作'), ('relaxing', '待命'), ('fixing', '维修'), ('losing', '丢失')], default='relaxing', max_length=20, verbose_name='状态')),
            ],
            options={
                'verbose_name_plural': '货箱',
                'verbose_name': '货箱',
            },
        ),
    ]
