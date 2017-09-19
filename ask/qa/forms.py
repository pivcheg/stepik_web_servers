from django import forms
from . import models


class AskForm(forms.Form):
    title = forms.CharField(max_length=100, label="Заголовок вопроса")
    text = forms.CharField(widget=forms.Textarea, label="Вопрос")

    def clean_text(self):
        text = self.cleaned_data['text']
        return text

    def save(self):
        question = models.Question(**self.cleaned_data)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.ModelChoiceField(required=True, queryset=None)

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['question'].queryset = models.Answer.objects.filter(question=kwargs['qid'])

    def clean(self):
        pass
