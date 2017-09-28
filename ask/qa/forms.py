from django import forms
# from django.shortcuts import get_object_or_404
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.utils import IntegrityError
from . import models


class AskForm(forms.Form):
    title = forms.CharField(max_length=100, label="Заголовок вопроса")
    text = forms.CharField(widget=forms.Textarea, label="Вопрос")

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(AskForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        print(self.cleaned_data['title'])
        title = self.cleaned_data['title']
        return title

    def clean_text(self):
        print(self.cleaned_data['text'])
        text = self.cleaned_data['text']
        return text

    def save(self):
        print("Save:", self)
        question = models.Question(**self.cleaned_data)
        # question.author, _ = models.User.objects.get_or_create(username='anon')
        question.author = self._user
        question.save()
        return question


class AnswerForm(forms.Form):
    # question = forms.ModelChoiceField(required=True, queryset=None, widget=forms.HiddenInput)
    # question = forms.IntegerField(required=False, widget=forms.HiddenInput, label="QID")
    text = forms.CharField(widget=forms.Textarea, label="Комментарий")

    def __init__(self, user, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self._qid = kwargs.get('initial', None)
        self._user = user

        if self._qid is not None:
            self._qid = self._qid.get('qid', None)

        print("__init__", "self._qid:", self._qid, "args:", args, "kwargs", kwargs)

    def clean_question(self):
        print(self.cleaned_data['question'])
        question = self.cleaned_data['question']
        return question

    def clean_text(self):
        print(self.cleaned_data['text'])
        text = self.cleaned_data['text']
        return text

    def save(self):
        self.cleaned_data['question'] = self._qid
        self.cleaned_data['author'] = self._user
        answer = models.Answer(**self.cleaned_data)
        answer.save()
        print("save:", self)
        return answer


class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=50, required=False)
    email = forms.CharField(widget=forms.EmailInput, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        print("clean_username:", self.cleaned_data['username'])
        username = self.cleaned_data['username']
        return username

    def clean_email(self):
        print("clean_email:", self.cleaned_data['email'])
        email = self.cleaned_data['email']
        return email

    def clean_password(self):
        print("clean_password:", self.cleaned_data['password'])
        password = self.cleaned_data['password']
        return password

    def save(self):
        print("self.cleaned_data:", self.cleaned_data)
        try:
            user = models.User.objects.create_user(username=self.cleaned_data['username'],
                    email=self.cleaned_data['email'], password=self.cleaned_data['password'])
        except IntegrityError:
            print("User exists:", self.cleaned_data['username'])
            user = None
        return user

class AuthUserForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)