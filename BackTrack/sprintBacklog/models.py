from django.db import models
from project.models import *
from productBacklog.models import *


# Create your models here.
class SprintBacklog(models.Model):
    STATUS_CHOICES = [
        ('Finished', 'Finished'),
        ('In process', 'In process')
    ]

    project = models.OneToOneField(Project, null=False, on_delete=models.CASCADE)
    sprintNumber = models.PositiveSmallIntegerField(null=False, blank=False)
    capacity = models.PositiveSmallIntegerField(null=False, blank=False)
    # Status = "Finished" or "In process"
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='In process')
    ddl = models.DateTimeField()
    time = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.project.name + " sprint" + str(self.sprintNumber)


class Task(models.Model):
    STATUS_CHOICES = [
        ('Finished', 'Finished'),
        ('In process', 'In process')
    ]

    pbi = models.ForeignKey(PBI, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    # Status = "Finished" or "In process"
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='In process')
    owner = models.ForeignKey(BackTrackUser, null=True, blank=True, related_name='task_owner', on_delete=models.SET_NULL)
    estimated = models.PositiveSmallIntegerField()
    effortsDone = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name
