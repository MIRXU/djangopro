# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-02-26 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20180223_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', upload_to='teachers/%Y/%m', verbose_name='\u8bb2\u5e08\u56fe\u50cf'),
        ),
    ]
