# Generated by Django 3.0.6 on 2020-08-01 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_auto_20200801_0730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='coordinators',
        ),
    ]