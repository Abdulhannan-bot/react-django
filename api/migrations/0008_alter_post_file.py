# Generated by Django 3.2.18 on 2023-03-06 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20230306_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='File',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
