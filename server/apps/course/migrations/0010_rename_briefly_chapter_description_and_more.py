# Generated by Django 5.2.1 on 2025-06-15 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_rename_briefly_course_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='briefly',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='chapter',
            old_name='name',
            new_name='title',
        ),
    ]
