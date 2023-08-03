from django.db import models

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length = 20)
    user_email = models.EmailField(unique=True)
    user_password = models.CharField(max_length = 100)
    user_validate = models.BooleanField(default=False)

'''
class GradeCalculation(models.Model):
    grade = models.IntegerField()
    min = models.FloatField()
    max = models.FloatField()
    avg = models.FloatField()

class EmailDomain(models.Model):
    domain = models.CharField(max_length=255)
    count = models.IntegerField()
'''