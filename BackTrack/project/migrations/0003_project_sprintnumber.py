# Generated by Django 2.2.6 on 2019-11-09 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_project_activesprint'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='sprintNumber',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
