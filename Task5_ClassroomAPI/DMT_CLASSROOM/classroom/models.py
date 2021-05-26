from django.db import models

from  User.models import User

class Course(models.Model):
    name = models.CharField(max_length=64, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    students = models.ManyToManyField(User, related_name='Students', blank=True)
    teachers = models.ManyToManyField(User, related_name='Teachers', blank=True)
    REQUIRED_FIELDS = ['name', ]

    def __str__(self):
        return f'Course #{self.pk}'

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.FileField(upload_to='uploads/', blank=True)
    homework = models.TextField()

    def __str__(self):
        return f'Lecture #{self.pk}'

class Homework(models.Model):
    pass