# Generated by Django 2.2.10 on 2020-08-23 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='art',
            name='thumbnail',
            field=models.ImageField(default=None, upload_to='art/thumbnails'),
            preserve_default=False,
        ),
    ]
