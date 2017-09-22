from django import forms
from django.shortcuts import get_object_or_404
from . import models


class AskForm(forms.Form):
    title = forms.CharField(max_length=100, label="Заголовок вопроса")
    text = forms.CharField(widget=forms.Textarea, label="Вопрос")

    def clean_text(self):
        text = self.cleaned_data['text']
        return text

    def save(self):
        question = models.Question(**self.cleaned_data)
        question.author, _ = models.User.objects.get_or_create(username='anon')
        print(models.User.objects.get_or_create(username='anon'))
        question.save()
        return question


class AnswerForm(forms.Form):
    # question = forms.ModelChoiceField(required=True, queryset=None, widget=forms.HiddenInput)
    question = forms.IntegerField(required=False, widget=forms.HiddenInput)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        # print("__init__", "queryset:", quest_object, "args:", args, "kwargs", kwargs)
        super(AnswerForm, self).__init__(*args, **kwargs)
        self._qid = kwargs.get('initial', None)
        if self._qid is not None:
            self._qid = self._qid.get('qid', None)
        print("__init__", "self._qid:", self._qid, "args:", args, "kwargs", kwargs)
        # self._quest = quest_object

    def clean_text(self):
        text = self.cleaned_data['text']
        return text

    def save(self):
        print("save:", self)
        self.cleaned_data['question'] = get_object_or_404(models.Question, id=self._qid)
        self.cleaned_data['author'], _ = models.User.objects.get_or_create(username='anon')
        answer = models.Answer(**self.cleaned_data)
        answer.save()
        return answer
