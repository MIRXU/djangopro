# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-02-26 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20180226_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='\u8001\u5e08\u544a\u8bc9\u4f60'),
        ),
        migrations.AlterField(
            model_name='course',
            name='you_need',
            field=models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='\u8bfe\u7a0b\u987b\u77e5'),
        ),
    ]
