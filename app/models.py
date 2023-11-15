from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    like = models.IntegerField()
    tags = models.ManyToManyField('Tag')


class Answer(models.Model):
    content = models.TextField()
    valid = models.BooleanField()
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    user_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    like = models.IntegerField()


class Tag(models.Model):
    title = models.CharField(max_length=255)


class Profile(models.Model):
    photo = models.ImageField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Like(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="+")
    answer_id = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name="+")