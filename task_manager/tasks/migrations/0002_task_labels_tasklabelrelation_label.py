# Generated by Django 5.1.1 on 2024-09-29 13:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, related_name='labels', through='tasks.TaskLabelRelation', to='labels.label', verbose_name='Labels'),
        ),
        migrations.AddField(
            model_name='tasklabelrelation',
            name='label',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='labels.label'),
            preserve_default=False,
        ),
    ]
