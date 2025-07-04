# Generated by Django 5.2.1 on 2025-06-13 14:04

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='加入时间')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.course', verbose_name='课程')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user', verbose_name='用户')),
            ],
            options={
                'verbose_name': '课程记录',
                'verbose_name_plural': '用户课程记录',
            },
        ),
    ]
