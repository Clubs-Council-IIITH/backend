# Generated by Django 3.0.6 on 2020-08-13 19:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0002_remove_budgetproposal_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetproposal',
            name='datetime',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]