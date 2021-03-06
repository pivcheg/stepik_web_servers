import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Модель для создания вопросов.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """
        Проверяет дату публикации статьи и возвращает True если статья не старше 1 дня.

        :return: bool
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def has_choice(self):
        """
        Проверяет есть ли у вопроса варианты ответов.

        :return: bool
        """
        choices = self.choice_set.filter(question=self.id)
        if choices:
            return True
        else:
            return False

    was_published_recently.short_description = "Published recently?"
    was_published_recently.admin_order_field = "pub_date"
    was_published_recently.boolean = True

    has_choice.short_description = "Have choices?"
    # has_choice.admin_order_field = "Published recently?"
    has_choice.boolean = True


class Choice(models.Model):
    """
    Модель для создания вариантов ответов на вопрос.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.choice_text
