# Generated by Django 3.0.7 on 2020-11-02 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0012_club_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='financial_requirements',
            field=models.TextField(default='None.'),
        ),
    ]