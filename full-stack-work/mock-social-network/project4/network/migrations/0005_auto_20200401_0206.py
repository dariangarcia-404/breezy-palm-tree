# Generated by Django 3.0.3 on 2020-04-01 02:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20200401_0205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='posts_liked',
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(null=True, related_name='user_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
