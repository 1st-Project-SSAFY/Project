# Generated by Django 4.2.14 on 2024-08-06 01:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0006_remove_buildingmanager_check_password_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingManagerToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=40, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='buildings.buildingmanager')),
            ],
        ),
    ]
