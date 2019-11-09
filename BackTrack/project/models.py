from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class BackTrackUser(AbstractUser):
    pass

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Not available', 'Not available')
    ]

    status = models.CharField(max_length=13, choices=STATUS_CHOICES, default='Available')
    project = models.ForeignKey("Project", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.username


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    manager = models.ForeignKey(BackTrackUser, related_name='manager', null=True, blank=True, on_delete=models.SET_NULL)
    # Creation time(set automatically once created)
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    activeSprint = models.ForeignKey('sprintBacklog.SprintBacklog', related_name='active_sprint', null=True, blank=True, on_delete=models.SET_NULL)
    sprintNumber = models.PositiveSmallIntegerField(null=False, blank=False, default=0)
    owner = models.OneToOneField(BackTrackUser, related_name='owner', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
