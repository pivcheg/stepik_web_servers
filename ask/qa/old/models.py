from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


# def do_login(login, password):
#     try:
#         user = MyUser.objects.get(login=login)
#     except MyUser.DoesNotExist:
#         return None
#     hashed_pass = salt_and_hash(password)
#     if user.password != hashed_pass:
#         return None
#     session = Session()
#     session.key = generate_long_random_key()
#     session.user = user
#     session.expires = datetime.now() + timedelta(days=5)
#     session.save()
#     return session.key


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
    author = models.ForeignKey(User, default=1)
    likes = models.ManyToManyField(User, related_name='question_like_user', blank=True)

    def __str__(self):
        return self.title


    def get_url(self):
        return "/question/%d/" % self.id
        #return reverse("question", kwargs={'qid': self.id})


class AnswerManager(models.Manager):
    pass

class Answer(models.Model):
    text = models.TextField(blank=False)
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, blank=False, on_delete=models.PROTECT)
    author = models.ForeignKey(User)
    objects = AnswerManager()


class MyUsers(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=100)


class Session(models.Model):
    key = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(MyUsers)
    expires = models.DateTimeField()