# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-12 04:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ca', '0004_auto_20160912_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='massnotification',
            name='mark_read',
            field=models.ManyToManyField(related_name='mark_read', to='ca.CAProfile'),
        ),
    ]