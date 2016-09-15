# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-13 11:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ca', '0012_auto_20160912_1938'),
    ]

    operations = [
        migrations.CreateModel(
            name='FbConnect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accessToken', models.CharField(blank=True, max_length=150, null=True)),
                ('uid', models.CharField(blank=True, max_length=150, null=True)),
                ('ca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ca.CAProfile')),
            ],
        ),
    ]