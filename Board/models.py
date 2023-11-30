from django.contrib.auth.models import User
from django.db import models


class AppUser(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)


class Vacancy(models.Model):
    employer = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=20)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    requirements = models.TextField()
    status = models.CharField(max_length=20, default='active')


class Application(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
