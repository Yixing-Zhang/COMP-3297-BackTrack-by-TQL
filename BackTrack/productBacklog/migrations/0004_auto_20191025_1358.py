# Generated by Django 2.2.6 on 2019-10-25 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productBacklog', '0003_auto_20191024_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='manager',
        ),
        migrations.AlterField(
            model_name='productbacklog',
            name='project',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
        migrations.DeleteModel(
            name='Developer',
        ),
        migrations.DeleteModel(
            name='Manager',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]