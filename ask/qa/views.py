from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from . import models

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
    # questions = models.Question.objects.all()
    # return render(request, "main_page.html", {
    #     'question_list': questions,
    # })

def questions_list_on_page(request, questions_queryset=models.Question.objects.order_by('id'), template="questions_paginator.html"):
    """Функция принимает отсортированный queryset (если не указан, тогда сортирует по id),
    а затем разбивает его на страницы используя произвольные шаблоны"""

    # limit = request.GET.get('limit', 10)
    # page = request.GET.get('page', 1)
    # paginator = Paginator(questions, limit)
    paginator, page = paginate(request, questions_queryset)
    #paginator.baseurl = reverse(reverse_url)
    #print("paginator.baseurl:", paginator.baseurl)
    return render(request, template, {
        'questions_on_page': page.object_list,
        'paginator': paginator,
        'page': page
    })

def login(request):
    return HttpResponse(request)

def signup(request):
    return HttpResponse(request)

@require_GET
def question_detail(request, qid):
    question = get_object_or_404(models.Question, id=qid)
    answers = models.Answer.objects.filter(question=qid)
    #likes = question.likes.all()

    return render(request, "question_details.html", {
        'question': question,
        'answers': answers,
    })

def ask(request):
    return HttpResponse(request)

def popular(request):
    questions = models.Question.objects.popular()
    return questions_list_on_page(request, questions, "popular.html")

def new(request):
    questions = models.Question.objects.new()
    return questions_list_on_page(request, questions, "new.html")
