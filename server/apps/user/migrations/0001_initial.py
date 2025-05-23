# Generated by Django 5.2.1 on 2025-05-21 14:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='banners/', verbose_name='轮播图')),
                ('to_id', models.IntegerField(blank=True, null=True, verbose_name='跳转ID')),
                ('sort_number', models.IntegerField(default=999, verbose_name='序号')),
            ],
            options={
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图管理',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=50, verbose_name='密码')),
                ('nickname', models.CharField(blank=True, max_length=30, null=True, verbose_name='昵称')),
                ('avatar', models.ImageField(default='avatars/default.jpg', upload_to='avatars/', verbose_name='头像')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户管理',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='内容')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='联系电话')),
                ('status', models.IntegerField(choices=[(1, '已回复'), (2, '待回复')], default=2, verbose_name='是否回复')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='用户')),
            ],
            options={
                'verbose_name': '反馈',
                'verbose_name_plural': '反馈管理',
            },
        ),
    ]
