# Generated by Django 4.2.14 on 2024-08-02 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fireissues', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fire_issue',
            name='fire_id',
        ),
        migrations.RemoveField(
            model_name='fire_logs',
            name='log_id',
        ),
    ]
