# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-14 18:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0011_create_time_spent_editing'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ChangeLog',
        ),
    ]