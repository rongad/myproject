from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='No description')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now) 

    def __str__(self):
        return self.title

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=[('POD', 'Prefect of Discipline'), ('ADMIN', 'Administrator')])
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} ({self.role})"

class Student(models.Model):
    student_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    grade_level = models.IntegerField(validators=[MinValueValidator(7), MaxValueValidator(12)])
    section = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - Grade {self.grade_level}{self.section}"

class SeverityLevel(models.Model):
    level_id = models.AutoField(primary_key=True)
    level_description = models.CharField(max_length=20, choices=[
        ('MINOR', 'Minor'),
        ('MODERATE', 'Moderate'),
        ('SEVERE', 'Severe')
    ])

    def __str__(self):
        return self.level_description

class DisciplinaryIncident(models.Model):
    incident_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    severity_level = models.ForeignKey(SeverityLevel, on_delete=models.PROTECT)
    reported_by = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='reported_incidents')

    def __str__(self):
        return f"Incident {self.incident_id} - {self.student.name}"

class Sanction(models.Model):
    sanction_id = models.AutoField(primary_key=True)
    incident = models.ForeignKey(DisciplinaryIncident, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in days")
    severity_level = models.ForeignKey(SeverityLevel, on_delete=models.PROTECT)
    issued_by = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='issued_sanctions')
    date_issued = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled')
    ], default='PENDING')

    def __str__(self):
        return f"Sanction {self.sanction_id} - {self.student.name}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Validate sanction duration based on severity level
        if self.severity_level.level_description == 'MINOR' and (self.duration < 1 or self.duration > 2):
            raise ValidationError('Minor sanctions must have duration between 1-2 days')
        elif self.severity_level.level_description == 'MODERATE' and (self.duration < 3 or self.duration > 5):
            raise ValidationError('Moderate sanctions must have duration between 3-5 days')
