# Generated by Django 2.1.5 on 2019-04-19 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_mymodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='postImg',
            field=models.FileField(blank=True, null=True, upload_to='account'),
        ),
    ]
