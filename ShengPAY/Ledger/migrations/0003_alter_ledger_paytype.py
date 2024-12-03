# Generated by Django 5.0.7 on 2024-08-11 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ledger', '0002_alter_ledger_paytime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger',
            name='paytype',
            field=models.IntegerField(choices=[(1, '运动'), (2, '吃饭'), (3, '娱乐'), (4, '学习'), (5, '借钱')], default=4),
        ),
    ]