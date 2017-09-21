from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from . import models
from . import forms

def paginate(request, queryset):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10

    if limit > 100 or limit < 1:
        limit = 10

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    paginator = Paginator(queryset, limit)

    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return paginator, page


def home(request):
    return questions_list_on_page(request)

def questions_list_on_page(request, questions_queryset=models.Question.objects.order_by('id'),
                           template="questions_paginator.html"):
    """Функция принимает отсортированный queryset (если не указан, тогда сортирует по id),
    вызывает функцию paginate, разбивает вопросы на страницы и возвращает html текст
    используя переданный шаблон."""

    paginator, page = paginate(request, questions_queryset)
    return render(request, template, {
        'questions_on_page': page.object_list,
        'paginator': paginator,
        'page': page
    })

def login(request):
    return HttpResponse(request)

def signup(request):
    return HttpResponse(request)

def add_comment(request, qid):
    queryset = get_object_or_404(models.Question, id=qid)
    if request.method == "GET":
        print("GET:", request.GET)

    if request.method == "POST":
        print("POST:", request.POST)
        form = forms.AnswerForm(request.POST, initial={'qid': queryset})
        #if form.is_valid():
        print("form.is_valid = True")
        answer = form.save()
        url = answer.get_url()
        return HttpResponseRedirect(url)
    else:
        form = forms.AnswerForm(initial={'qid': queryset})
        #form = forms.AnswerForm(qid=qid)
    return render(request, "question_add_comment.html", {
        'form': form,
        'qid': qid
    })

#@login_required
def add_question(request):
    if request.method == "POST":
        # form = forms.AskForm(request.user, request.POST)
        form = forms.AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = forms.AskForm()
    return render(request, "question_add.html", {
        'form': form
    })

#@require_GET
def question_detail(request, qid):
    question = get_object_or_404(models.Question, id=qid)
    answers = models.Answer.objects.filter(question=qid)
    if request.method == "POST":
        return add_comment(request, qid)
    # add_comment(request, question)

    return render(request, "question_details.html", {
        'question': question,
        'answers': answers,
    })

def popular_questions(request):
    questions = models.Question.objects.popular()
    return questions_list_on_page(request, questions, "questions_popular.html")

def new_questions(request):
    questions = models.Question.objects.new()
    return questions_list_on_page(request, questions, "questions_new.html")
