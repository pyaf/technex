# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-16 09:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ca', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MassNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mass_message', models.TextField()),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='college',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='college_address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
