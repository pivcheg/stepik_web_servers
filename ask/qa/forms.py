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
        # question.author = models.User.objects.create_user('anon', 'anon@bay.com', 'anonpassword').save()
        question.save()
        return question

    # def clean(self):
    #     return self.cleaned_data

class AnswerForm(forms.Form):
    # question = forms.ModelChoiceField(required=True, queryset=None, widget=forms.HiddenInput)
    question = forms.IntegerField(required=True, widget=forms.HiddenInput)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        print("__init__", "args:", args, "kwargs", kwargs)
        self._qid = kwargs['initial']['qid']
        #self.fields['question'].qid = kwargs['initial']['qid']
        #print("self.fields['question'].qid:", self.fields['question'].qid)
        # print("self.fields['question']", self.fields['question'])

    def clean_text(self):
        text = self.cleaned_data['text']
        return text

    def clean_quiestion(self):
        print("clean_question:", self.cleaned_data['question'].qid)
        question = self.cleaned_data['question'].qid
        return question

    def save(self):
        print("save:", self)
        self.cleaned_data['question'] = self._qid
        self.cleaned_data['author_id'] = 1
        answer = models.Answer(**self.cleaned_data)
        answer.save()
        return answer

# class AnswerForm(forms.Form):
#     text = forms.CharField(widget=forms.Textarea)
#     question = forms.ModelChoiceField(required=True, queryset=None)
#
#     def __init__(self, *args, **kwargs):
#         super(AnswerForm, self).__init__(*args, **kwargs)
#         #super(AnswerForm, self).__init__()
#         self.fields['question'].queryset = args
#
#     def clean(self):
#         pass
