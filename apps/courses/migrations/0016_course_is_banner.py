# Generated by Django 2.0.2 on 2019-06-20 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_auto_20190613_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否轮播图'),
        ),
    ]
