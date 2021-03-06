# Generated by Django 2.2.10 on 2021-02-03 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210118_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='category',
            field=models.PositiveIntegerField(choices=[(0, '화가'), (1, '조각가'), (2, '공예가'), (3, '기타')], default=0),
        ),
        migrations.AlterField(
            model_name='artist',
            name='representative_work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='artist_of_representative_work', to='file.File'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='residence',
            field=models.PositiveIntegerField(choices=[(0, '서울특별시'), (1, '부산광역시'), (2, '대구광역시'), (3, '인천광역시'), (4, '광주광역시'), (5, '대전광역시'), (6, '울산광역시'), (7, '세종특별자치시'), (8, '경기도'), (9, '강원도'), (10, '충청북도'), (11, '충청남도'), (12, '전라북도'), (13, '전라남도'), (14, '경상북도'), (15, '경상남도'), (16, '제주특별자치도')], default=0),
        ),
        migrations.AlterField(
            model_name='artist',
            name='thumbnail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='artist_of_thumbnail', to='file.File'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='artist', to=settings.AUTH_USER_MODEL),
        ),
    ]
