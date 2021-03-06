# Generated by Django 2.0.2 on 2019-06-10 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20190610_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='老师提醒'),
        ),
        migrations.AddField(
            model_name='course',
            name='youneed_known',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='课程须知'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='courses/%Y%m', verbose_name='封面图片'),
        ),
        migrations.AlterField(
            model_name='course',
            name='tag',
            field=models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='关键词'),
        ),
    ]
