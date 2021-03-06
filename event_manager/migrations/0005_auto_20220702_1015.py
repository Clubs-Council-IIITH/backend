# Generated by Django 3.2.6 on 2022-07-02 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event_manager', '0004_alter_event_mode'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.IntegerField(choices=[[0, 'cc_pending'], [1, 'fc_pending'], [2, 'gad_pending'], [3, 'slc_pending'], [4, 'slo_pending'], [5, 'approved'], [6, 'completed'], [7, 'deleted']], default=0)),
                ('remarks', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_manager.eventstate'),
        ),
    ]
