# Generated by Django 2.2.6 on 2019-11-07 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sprintBacklog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprintbacklog',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
    ]
