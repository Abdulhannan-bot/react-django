# Generated by Django 3.2.18 on 2023-03-10 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20230310_0504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user_name',
        ),
    ]
