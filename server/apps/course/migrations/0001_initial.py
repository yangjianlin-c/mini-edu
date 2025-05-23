# Generated by Django 5.2.1 on 2025-05-21 14:21

import django.db.models.deletion
import mdeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('briefly', models.CharField(max_length=255, verbose_name='简介')),
                ('level', models.IntegerField(choices=[(3, '初级'), (2, '中级'), (1, '高级')], verbose_name='难度')),
                ('study_number', models.IntegerField(default=0, verbose_name='学习人数')),
                ('tell', mdeditor.fields.MDTextField(default='#### 课程须知\n如果有问题及时反馈  \n#### 你能学到什么\nDjango Ninja & React 前后端的使用\n', verbose_name='需要告知的内容')),
                ('image', models.ImageField(upload_to='courses/', verbose_name='图片')),
                ('sort_number', models.IntegerField(default=999, verbose_name='序号')),
            ],
            options={
                'verbose_name': '课程',
                'verbose_name_plural': '课程管理',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user', verbose_name='用户')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.course', verbose_name='课程')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论管理',
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('briefly', models.CharField(max_length=200, verbose_name='简介')),
                ('sort_number', models.IntegerField(default=999, verbose_name='序号')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.course', verbose_name='所属课程')),
            ],
            options={
                'verbose_name': '章节',
                'verbose_name_plural': '章节管理',
            },
        ),
        migrations.CreateModel(
            name='UserHub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('act_type', models.IntegerField(choices=[(1, '学习'), (2, '收藏')])),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.course', verbose_name='课程')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user', verbose_name='用户')),
            ],
            options={
                'verbose_name': '操作记录',
                'verbose_name_plural': '用户操作记录',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('video', models.FileField(upload_to='videos/', verbose_name='视频文件')),
                ('chapter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.chapter', verbose_name='所属章节')),
            ],
            options={
                'verbose_name': '视频',
                'verbose_name_plural': '视频管理',
            },
        ),
    ]
