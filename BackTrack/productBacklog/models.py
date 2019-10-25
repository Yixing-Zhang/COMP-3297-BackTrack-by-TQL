from django.db import models
from project.models import *


# Create your models here.
class ProductBacklog(models.Model):
    project = models.OneToOneField(Project, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.name


class PBI(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    # Status = "Finished" or "In process" or "Ready"
    status = models.CharField(max_length=10)
    estimated = models.PositiveSmallIntegerField()
    priority = models.PositiveSmallIntegerField()
    sprintNumber = models.PositiveSmallIntegerField(null=True, blank=True)
    productBacklog = models.ForeignKey(ProductBacklog, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
