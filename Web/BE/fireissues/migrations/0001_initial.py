# Generated by Django 4.2.14 on 2024-08-01 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('robots', '0001_initial'),
        ('buildings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fire_Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fire_id', models.IntegerField(unique=True)),
                ('fire_dt', models.DateTimeField(auto_now_add=True)),
                ('end_dt', models.DateTimeField(null=True)),
                ('fire_scale', models.IntegerField(null=True)),
                ('detail', models.TextField(null=True)),
                ('video', models.FileField(null=True, upload_to='fire_video/')),
                ('fire_floor', models.IntegerField()),
                ('fire_x', models.IntegerField()),
                ('fire_y', models.IntegerField()),
                ('building_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fire_building', to='buildings.building')),
            ],
        ),
        migrations.CreateModel(
            name='Fire_Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_id', models.IntegerField(unique=True)),
                ('state_dt', models.DateTimeField(auto_now_add=True)),
                ('battery', models.IntegerField()),
                ('guide_liquid', models.IntegerField()),
                ('guide_light', models.BooleanField()),
                ('firefighter_connect', models.BooleanField()),
                ('mission', models.IntegerField(choices=[(0, '대기'), (1, '이동중'), (2, '완료'), (3, '실패')])),
                ('location_x', models.IntegerField()),
                ('location_y', models.IntegerField()),
                ('block_x', models.IntegerField(null=True)),
                ('block_y', models.IntegerField(null=True)),
                ('fire_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fireissue', to='fireissues.fire_issue')),
                ('robot_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='move_robot', to='robots.robot')),
            ],
        ),
    ]
