# Generated by Django 2.2.6 on 2019-11-07 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productBacklog', '0004_pbi_taskhours'),
    ]

    operations = [
        migrations.AddField(
            model_name='pbi',
            name='remainingTaskHours',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]