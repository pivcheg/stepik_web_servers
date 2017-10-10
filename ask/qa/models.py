from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=False)
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User)
    likes = models.ManyToManyField(User, related_name='question_like_user', blank=True)

    def __str__(self):
        return self.title

    def get_url(self):
        # return "/question/%d/" % self.id
        return reverse('qa:question_details', kwargs={'qid': self.id})


class AnswerManager(models.Manager):
    pass


class Answer(models.Model):
    text = models.TextField(blank=False)
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, blank=False, on_delete=models.PROTECT)
    author = models.ForeignKey(User)
    objects = AnswerManager()

    def get_url(self):
        # return "/question/%d/" % self.question.id
        return reverse('qa:question_details', kwargs={'qid': self.question.id})
