# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-05 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20180105_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
