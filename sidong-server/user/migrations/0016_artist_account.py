# Generated by Django 2.2.10 on 2021-06-14 06:43

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20210603_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='account',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
