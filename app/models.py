from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Length


def fill_db():
    pass


class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-upload_date')

    def get_hot(self):
        return self.order_by('-like_count')

    def get_all(self):
        return self.order_by()

    def get_by_id(self, question_id):
        return self.get(id=question_id)

    def get_by_tag(self, tag_title):
        return self.filter(tags__title=tag_title)


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
    like_count = models.IntegerField()
    tags = models.ManyToManyField('Tag', related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.title + ' ' + str(self.id)


class AnswerManager(models.Manager):
    def get_all(self):
        return self

    def get_by_question(self, question_id):
        return self.filter(question_id=question_id)

    def get_answer_count(self, questions):
        answers = {}
        for question in questions:
            answers[question.id] = self.filter(question_id=question.id).count()
        return answers

class Answer(models.Model):
    text = models.TextField()
    isTrue = models.BooleanField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
    like_count = models.IntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)

    objects = AnswerManager()


class TagManager(models.Manager):
    def get_popular(self):
        return self.order_by()[:10]

    def get_by_question(self, question):
        return self.filter(questions = question)



class Tag(models.Model):
    title = models.CharField(max_length=255)

    objects = TagManager()

    def __str__(self):
        return self.title


class Profile(models.Model):
    image = models.ImageField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class QuestionLike(models.Model):
    question = models.ForeignKey('Question', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    is_like = models.BooleanField(default=False)


class AnswerLike(models.Model):
    answer = models.ForeignKey('Answer', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    is_like = models.BooleanField(default=False)