from django.db import models
import uuid

def user_id():
    return uuid.uuid4().hex[:20]

class School(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    max_student = models.IntegerField()

class Student(models.Model):
    id = models.CharField(max_length=20, default=user_id, primary_key=True, editable=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField()
    nationality = models.CharField(max_length=30)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
