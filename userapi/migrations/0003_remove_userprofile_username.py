# Generated by Django 2.2 on 2021-07-23 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapi', '0002_userprofile_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='username',
        ),
    ]