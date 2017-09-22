from django import forms
from . import models

class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    # def __init__(self, user, **kwargs):
    #     self._user = user
    #     super(AskForm, self).__init__(**kwargs)

    # def clean(self):
    #     if self._user.is_banned:
    #         raise forms.ValidationError("Access denied")

    def clean_text(self):
        text = self.cleaned_data['text']
        # if not is_ethic(text):
        #     raise forms.ValidationError("Сообщение не корректно", code=12)
        return text

    def save(self):
        # self.cleaned_data['author'] = self._user
        question = models.Question(**self.cleaned_data)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.ModelChoiceField(required=True, queryset=None)

    def __init__(self, queryset, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['question'].queryset = models.Answer.objects.filter(question=kwargs['qid'])
        #self.fields['question'].qid = kwargs['initial']['qid']
        #print("self.fields['question'].qid:", self.fields['question'].qid)
        # print("self.fields['question']", self.fields['question'])

    # def clean_quiestion(self):
    #     print("clean_question:", self.cleaned_data['question'].qid)
    #     question = self.cleaned_data['question'].qid
    #     return question


    def clean(self):
        # if is_spam(self.clean_data):
        #     raise forms.ValidationError("Сообщение похоже на спам!", code="spam")
        pass


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
