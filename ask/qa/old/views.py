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

# def login(request):
#     error = ""
#     if request.method == "POST":
#         login = request.POST.get('login')
#         password = request.POST.get('password')
#         url = request.POST.get('continue', '/')
#         sessid = models.do_login(login, password)
#         if sessid:
#             response = HttpResponseRedirect(url)
#             response.set_cookie('sessid', sessid, domain='', httponly=True,
#                                 expires=datetime.now()+timedelta(days=5)
#                                 )
#             return response
#         else:
#             error = "Неверный логин или пароль"
#     return render(request, "login.html", {
#         'error': error
#     })


def home(request):
    return questions_list_on_page(request)

def questions_list_on_page(request, questions_queryset=models.Question.objects.order_by('id'),
                           template="questions_main.html"):
    """Функция принимает отсортированный queryset (если не указан, тогда сортирует по id),
    а затем разбивает его на страницы используя произвольные шаблоны"""

    paginator, page = paginate(request, questions_queryset)
    # paginator.baseurl = reverse(reverse_url)
    return render(request, template, {
        'questions_on_page': page.object_list,
        'paginator': paginator,
        'page': page
    })

def add_question(request):
    if request.method == "POST":
        form = forms.AskForm(request.POST)
        if form.is_valid():
            post = form.save()
            url = post.get_url()
            return HttpResponseRedirect(url)
    else:
        form = forms.AskForm()
    return render(request, "question_add.html", {
        'form': form
    })

def login(request):
    return HttpResponse(request)

def signup(request):
    return HttpResponse(request)

@require_GET
def question_detail(request, qid):
    question = get_object_or_404(models.Question, id=qid)
    answers = models.Answer.objects.filter(question=qid)
    # answers = models.Answer.question_set.all()
    # likes = question.likes.all()

    return render(request, "question_details.html", {
        'question': question,
        'answers': answers,
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

def popular_questions(request):
    questions = models.Question.objects.popular()
    return questions_list_on_page(request, questions, "questions_popular.html")

def new_questions(request):
    questions = models.Question.objects.new()
    return questions_list_on_page(request, questions, "questions_new.html")
