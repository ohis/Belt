# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 21:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('belt_exam', '0003_auto_20170329_1418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='favorite',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='user_submit',
        ),
        migrations.DeleteModel(
            name='Quote',
        ),
    ]
