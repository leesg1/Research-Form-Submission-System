from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
	user = models.OneToOneField(User, unique = True)
	is_verified = models.BooleanField(defaul = False)