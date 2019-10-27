from django.db import models


# Create your models here.
class Owner(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Manager(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=15)
    # Number of projects being managed
    status = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    manager = models.ForeignKey(Manager, null=True, blank=True, on_delete=models.SET_NULL)
    # Creation time(set automatically once created)
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Developer(models.Model):
    ROLE_CHOICES = [
        ('Developer', 'Developer'),
        ('Owner', 'Owner'),
        ('None', None)
    ]
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Not available', 'Not available')
    ]
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=15)
    # Role is "Owner" or "Developer" or "NULL" when not involved in any project
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default='N')
    # Status = "Available" or "Not available"
    status = models.CharField(max_length=13, choices=STATUS_CHOICES, default='A')
    # Only has project when involved in a project as developer
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
