# Generated by Django 4.2.14 on 2024-08-08 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='robot',
            name='charged_state',
        ),
    ]
