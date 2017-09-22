from django import forms
from django.shortcuts import get_object_or_404
from . import models


class AskForm(forms.Form):
    title = forms.CharField(max_length=100, label="Заголовок вопроса")
    text = forms.CharField(widget=forms.Textarea, label="Вопрос")

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
        question.author, _ = models.User.objects.get_or_create(username='anon')
        print(models.User.objects.get_or_create(username='anon'))
        question.save()
        return question


class AnswerForm(forms.Form):
    # question = forms.ModelChoiceField(required=True, queryset=None, widget=forms.HiddenInput)
    question = forms.IntegerField(required=False, widget=forms.HiddenInput, label="QID")
    text = forms.CharField(widget=forms.Textarea, label="Комментарий")

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self._qid = kwargs.get('initial', None)

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
        self.cleaned_data['author'], _ = models.User.objects.get_or_create(username='anon')
        answer = models.Answer(**self.cleaned_data)
        answer.save()
        print("save:", self)
        return answer
