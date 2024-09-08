from django.db import models
# from user.models import User
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.4
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='user')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions'
    )

class Threat(models.Model):
    source_ip = models.GenericIPAddressField()
    attack_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()


    def __str__(self):
        return f"{self.attack_type} from {self.source_ip}"
    

class SystemHealth(models.Model):
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    disk_usage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Health report at {self.timestamp}"
    
class Incident(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    reported_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    status = models.CharField(max_length=50,choices=[
        ("open","Open"),("close","Close")
    ])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class IncidentReport(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    incident_type = models.CharField(max_length=255)
    description = models.TextField()
    occurrence_time = models.DateTimeField(auto_created=True)
    severity = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.incident_type} - {self.severity}"


