# crm_app/models.py
from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} ({self.role.name})"

class CustomField(models.Model):
    TEXT = 'text'
    CHECKBOX = 'checkbox'
    SELECT = 'select'

    FIELD_TYPE_CHOICES = (
        (TEXT, 'Text'),
        (CHECKBOX, 'Checkbox'),
        (SELECT, 'Select'),
        # Add more field types as needed
    )

    label = models.CharField(max_length=50)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES)
    
    def __str__(self):
        return self.label
