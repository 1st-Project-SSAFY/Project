# Generated by Django 4.2.14 on 2024-08-12 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0002_remove_robot_charged_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robot',
            name='state',
            field=models.BooleanField(default=True),
        ),
    ]
