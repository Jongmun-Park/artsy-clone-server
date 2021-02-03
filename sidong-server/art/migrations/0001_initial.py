# Generated by Django 2.2.10 on 2021-02-03 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0003_auto_20210203_0711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Art',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True)),
                ('medium', models.PositiveIntegerField(choices=[(0, '회화'), (1, '조각'), (2, '소묘'), (3, '판화'), (4, '종이'), (5, '섬유'), (6, '기타 매체')], default=0)),
                ('sale_status', models.PositiveIntegerField(choices=[(0, '비매품'), (1, '판매품'), (2, '판매 완료')], default=0)),
                ('is_framed', models.BooleanField(default=False)),
                ('price', models.PositiveIntegerField(default=None, null=True)),
                ('orientation', models.PositiveIntegerField(choices=[(0, '가로로 긴 배치'), (1, '세로가 긴 배치'), (2, '정사각형'), (3, '기타')], default=0)),
                ('size', models.CharField(choices=[('small', 'small'), ('medium', 'medium'), ('large', 'large')], max_length=8)),
                ('width', models.PositiveIntegerField(default=0)),
                ('height', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('medium', models.PositiveIntegerField(choices=[(0, '회화'), (1, '조각'), (2, '소묘'), (3, '판화'), (4, '종이'), (5, '섬유'), (6, '기타 매체')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Technique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('medium', models.PositiveIntegerField(choices=[(0, '회화'), (1, '조각'), (2, '소묘'), (3, '판화'), (4, '종이'), (5, '섬유'), (6, '기타 매체')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('medium', models.PositiveIntegerField(choices=[(0, '회화'), (1, '조각'), (2, '소묘'), (3, '판화'), (4, '종이'), (5, '섬유'), (6, '기타 매체')], default=0)),
            ],
        ),
        migrations.AddConstraint(
            model_name='theme',
            constraint=models.UniqueConstraint(fields=('name', 'medium'), name='unique_theme'),
        ),
        migrations.AddConstraint(
            model_name='technique',
            constraint=models.UniqueConstraint(fields=('name', 'medium'), name='unique_technique'),
        ),
        migrations.AddConstraint(
            model_name='style',
            constraint=models.UniqueConstraint(fields=('name', 'medium'), name='unique_style'),
        ),
        migrations.AddField(
            model_name='art',
            name='artist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='arts', to='user.Artist'),
        ),
        migrations.AddField(
            model_name='art',
            name='style',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='arts', to='art.Style'),
        ),
        migrations.AddField(
            model_name='art',
            name='technique',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='arts', to='art.Technique'),
        ),
        migrations.AddField(
            model_name='art',
            name='theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='arts', to='art.Theme'),
        ),
    ]
