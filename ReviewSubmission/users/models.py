from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
	user = models.OneToOneField(User, unique=True)
	is_verified = models.BooleanField(default=False)

User.profile = property(lambda u: Student.objects.get_or_create(user=u)[0])