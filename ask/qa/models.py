from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=False)
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, blank=False, default="x")
    likes = models.ManyToManyField(User, related_name='question_like_user', blank=True)

class QuestionManager(Question):
    def new(self):
        return self.ordering('-added_at')

    def popular(self):
        return self.ordering('-rating')

class Answer(models.Model):
    text = models.TextField(blank=False)
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, blank=False, on_delete=models.PROTECT)
    author = models.ForeignKey(User, blank=False)
