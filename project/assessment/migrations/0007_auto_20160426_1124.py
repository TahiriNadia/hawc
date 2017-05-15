# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-26 16:24


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0006_auto_20150724_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='enable_study_quality',
            field=models.BooleanField(default=True, help_text=b'Define criteria for a systematic review of literature, and apply these criteria to references in your literature-review. View details on findings and identify areas with a potential risk of bias.'),
        ),
        migrations.RenameField(
            model_name='assessment',
            old_name='enable_study_quality',
            new_name='enable_risk_of_bias',
        ),
    ]
