# Generated by Django 2.2.6 on 2019-10-24 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productBacklog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PBI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=10)),
                ('estimated', models.PositiveSmallIntegerField()),
                ('priority', models.PositiveSmallIntegerField()),
                ('sprintNumber', models.PositiveSmallIntegerField()),
                ('productBacklog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productBacklog.ProductBacklog')),
            ],
        ),
    ]