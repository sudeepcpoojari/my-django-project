from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class user(AbstractUser):
    ROLE_CHOICES=(
        ('admin','Admin'),
        ('teacher','Teacher'),
        ('student','Student'),
        ('parent','Parent'),
    )
    role=models.CharField(max_length=20,choices=ROLE_CHOICES)


class Classroom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    teacher = models.ForeignKey(user, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(user, blank=True, related_name='classrooms')

    def str(self):
        return self.name