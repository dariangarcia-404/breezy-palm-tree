# Generated by Django 3.0.3 on 2020-04-02 01:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_auto_20200402_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, null=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='likes', to='network.Post'),
        ),
    ]
