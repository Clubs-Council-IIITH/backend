# Generated by Django 3.0.6 on 2020-06-02 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20200602_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='audience',
        ),
    ]
