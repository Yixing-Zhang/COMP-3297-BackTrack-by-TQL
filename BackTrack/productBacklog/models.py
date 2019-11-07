from django.db import models
from project.models import *


# Create your models here.
class ProductBacklog(models.Model):
    project = models.OneToOneField(Project, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.name


class PBI(models.Model):
    STATUS_CHOICES = [
        ('Finished', 'Finished'),
        ('In process', 'In process'),
        ('Ready', 'Ready')
    ]
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    # Status = "Finished" or "In process" or "Ready"
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ready')
    taskHours = models.PositiveSmallIntegerField(null=True, blank=True)
    estimated = models.PositiveSmallIntegerField()
    priority = models.PositiveSmallIntegerField()
    cumulative = models.PositiveIntegerField(null=True, blank=True)
    productBacklog = models.ForeignKey(ProductBacklog, null=False, on_delete=models.CASCADE)
    sprintBacklog = models.ForeignKey('sprintBacklog.SprintBacklog', null=True, blank=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
