from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    qualification = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.user.username+'(Teacher)'




class Class(models.Model):
    name = models.CharField(max_length=50)
    teachers = models.ManyToManyField(Teacher)

    def __str__(self):
        return self.name

    def add_subject(self, name):
        subject = Subject.objects.create(name=name, class_field=self)
        return subject

    def update_subject(self, subject_id, name):
        try:
            subject = Subject.objects.get(id=subject_id, class_field=self)
            subject.name = name
            subject.save()
            return subject
        except Subject.DoesNotExist:
            return None

    def delete_subject(self, subject_id):
        try:
            subject = Subject.objects.get(id=subject_id, class_field=self)
            subject.delete()
            return True
        except Subject.DoesNotExist:
            return False


class Subject(models.Model):
    name = models.CharField(max_length=50)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name+'(Subject)'
    
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    roll_number = models.CharField(max_length=10)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + '(Student)'
    
    
    