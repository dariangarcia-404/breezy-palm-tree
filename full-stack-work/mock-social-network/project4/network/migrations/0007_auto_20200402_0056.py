# Generated by Django 3.0.3 on 2020-04-02 00:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20200401_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='user_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
