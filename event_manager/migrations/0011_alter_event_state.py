# Generated by Django 3.2.6 on 2022-07-21 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_manager', '0010_rename_from_user_eventfeedback_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='state',
            field=models.IntegerField(choices=[[0, 'cc_pending'], [1, 'fc_pending'], [2, 'slo_pending'], [3, 'slc_pending'], [4, 'gad_pending'], [5, 'approved'], [6, 'completed'], [7, 'deleted']], default=0),
        ),
    ]