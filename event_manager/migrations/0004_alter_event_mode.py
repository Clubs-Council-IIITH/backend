# Generated by Django 3.2.6 on 2022-07-01 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_manager', '0003_auto_20220701_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='mode',
            field=models.CharField(choices=[['offline', 'offline'], ['online', 'online']], default='offline', max_length=50),
        ),
    ]