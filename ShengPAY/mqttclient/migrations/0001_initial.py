# Generated by Django 5.0.7 on 2024-08-11 02:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MqttServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='TopicMsg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.JSONField()),
                ('rastime', models.DateTimeField(auto_now_add=True)),
                ('msgtype', models.IntegerField()),
                ('server', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mqttclient.mqttserver')),
            ],
        ),
    ]
