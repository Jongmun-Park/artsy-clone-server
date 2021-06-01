# Generated by Django 2.2.10 on 2021-05-31 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='art',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='art.Art'),
        ),
        migrations.AlterField(
            model_name='order',
            name='artist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='user.Artist'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, '취소'), (1, '대기'), (2, '실패'), (3, '성공'), (4, '배송 준비중'), (5, '배송 중'), (6, '배송 완료'), (7, '환불 요청'), (8, '환불 완료'), (9, '구매 확정')], default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='userinfo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='user.UserInfo'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='user.Order'),
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reason', models.PositiveIntegerField(choices=[(0, '단순 변심'), (1, '실제 작품의 내용이 작품 상세 정보에 표기된 내용과 상이한 경우'), (2, '배송 중 파손되었을 경우'), (3, '위작 또는 명시되지 않은 모작의 경우'), (4, '기타')], default=0)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='refunds', to='user.Order')),
            ],
        ),
    ]