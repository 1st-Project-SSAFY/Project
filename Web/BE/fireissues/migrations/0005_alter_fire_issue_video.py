# Generated by Django 4.2.14 on 2024-08-13 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fireissues', '0004_remove_fire_logs_firefighter_connect_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fire_issue',
            name='video',
            field=models.TextField(null=True),
        ),
    ]
