# Generated by Django 2.2.10 on 2021-01-18 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('file', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='categories',
        ),
        migrations.AddField(
            model_name='artist',
            name='category',
            field=models.IntegerField(
                choices=[(0, '화가'), (1, '조각가'), (2, '공예가'), (3, '기타')], default=0),
        ),
        migrations.AddField(
            model_name='artist',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='artist',
            name='representative_work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='representative_work', to='file.File'),
        ),
        migrations.AddField(
            model_name='artist',
            name='residence',
            field=models.IntegerField(choices=[(0, '서울특별시'), (1, '부산광역시'), (2, '대구광역시'), (3, '인천광역시'), (4, '광주광역시'), (5, '대전광역시'), (6, '울산광역시'), (7, '세종특별자치시'), (
                8, '경기도'), (9, '강원도'), (10, '충청북도'), (11, '충청남도'), (12, '전라북도'), (13, '전라남도'), (14, '경상북도'), (15, '경상남도'), (16, '제주특별자치도')], default=0),
        ),
        migrations.AddField(
            model_name='artist',
            name='user',
            field=models.OneToOneField(
                default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='artist',
            name='artist_name',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='artist',
            name='thumbnail',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='thumbnail', to='file.File'),
        ),
    ]
