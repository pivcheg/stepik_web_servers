import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Модель для создания вопросов.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now())

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """
        Проверяет дату публикации статьи и возвращает True если статья не старше 1 дня.

        :return: bool
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """
    Модель для создания вариантов ответов на вопрос.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.choice_text
