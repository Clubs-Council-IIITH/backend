# Generated by Django 3.2.6 on 2022-07-09 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_manager', '0007_auto_20220709_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventfeedback',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
