from django.db import models

class Registration(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=64)

