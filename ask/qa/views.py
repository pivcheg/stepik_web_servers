from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . import models

def home(request, *args, **kwargs):
    # id = get_object_or_404(models.Question)
    questions = models.Question.objects.all()
    #obj = Post.objects.get(pk=id)
    return render(request, "main_page.html", {
        'question_list': questions,
    })

def login(request):
    return HttpResponse(request)

def signup(request):
    return HttpResponse(request)

def question_detail(request, qid):
    question = get_object_or_404(models.Question, id=qid)
    #answers =  models.Answer.question.filter(question=qid)
    answers = models.Answer.objects.filter(question=qid)
    return render(request, "question_details.html", {
        'question': question,
        'answers': answers,
    })

def ask(request):
    return HttpResponse(request)

def popular(request):
    return HttpResponse(request)

def new(request):
    return HttpResponse(request)
