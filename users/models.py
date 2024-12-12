from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
class DisciplinaryIncident(models.Model):
    incident_id = models.AutoField(primary_key=True)
    student = models.TextField(max_length=50)
    description = models.TextField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    severity_level = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled')
    ], default='PENDING')
    sanction = models.CharField(max_length=20, choices=[
        ('MINOR', 'Minor'),
        ('MODERATE', 'Moderate'),
        ('SEVERE', 'Severe')
    ], default='Minor')
    reported_by = models.TextField(max_length=200)
 


