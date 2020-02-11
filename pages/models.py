from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

def user_id():
    return uuid.uuid4().hex[:20]

class School(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    max_student = models.IntegerField(validators=[MinValueValidator(1)])

class Student(models.Model):
    id = models.CharField(max_length=20, default=user_id, primary_key=True, editable=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)])
    nationality = models.CharField(max_length=30)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
