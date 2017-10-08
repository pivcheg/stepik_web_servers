# from django.core.urlresolvers import reverse
# from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth import views
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from . import models
from . import forms


def paginate(request, queryset):
    """Функция будет разбивать queryset на несколько страниц, если превышен заданный лимит на количество записей.
    Возвращает объект пагинатор и текущую страницу. Если страница указана не верно, вернет последнию страницу."""

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
                           template="questions_main.html"):
    """Функция принимает отсортированный queryset (если не указан, тогда сортирует по id),
    вызывает функцию paginate, разбивает вопросы на страницы и возвращает html текст
    используя переданный шаблон."""

    paginator, page = paginate(request, questions_queryset)
    return render(request, template, {
        'questions_on_page': page.object_list,
        'paginator': paginator,
        'page': page,
        'user': request.user,
    })


def change_password(request):
    template_response = views.password_change(request)
    # Do something with `template_response`
    return template_response


def logout(request):
    django_logout(request)
    return HttpResponseRedirect("/")


def login(request):
    if request.method == "POST":
        form = forms.AuthUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            # url = request.POST.get('continue', '/')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    return HttpResponse("Account disabled")
            else:
                return render(request, "user_login.html", {
                    'form': form,
                    'error': True
                })
    else:
        form = forms.AuthUserForm()

    return render(request, "user_login.html", {
        'form': form,
        'error': None
        })


def signup(request):
    if request.method == "POST":
        print("Request POST:", request.POST)
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                return login(request)
                # return HttpResponseRedirect("/")
            else:
                return render(request, "user_new.html", {
                    'form': form,
                    'errors': ["User wasn't created"],
                })
    else:
        form = forms.CreateUserForm()
    return render(request, "user_new.html", {
        'form': form,
        'errors': form.errors,
        })


@login_required
def add_question(request):
    if request.method == "POST":
        # form = forms.AskForm(request.user, request.POST)
        form = forms.AskForm(request.user, request.POST)
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = forms.AskForm(request.user)

    return render(request, "question_add.html", {
        'form': form
    })


def question_detail(request, qid):
    question = get_object_or_404(models.Question, id=qid)
    answers = models.Answer.objects.filter(question=qid)
    if request.method == "POST" and request.user.is_authenticated():
        form = forms.AnswerForm(request.user, request.POST, initial={'qid': question})
        if form.is_valid():
            answer = form.save()
            url = answer.get_url()
            return HttpResponseRedirect(url)
        else:
            print("form.is_valid = FALSE")
    else:
        form = forms.AnswerForm(request.user)

    return render(request, "question_details.html", {
        'question': question,
        'answers': answers,
        'form': form,
    })

def question_rating(request, qid):
    # question = get_object_or_404(models.Question, id=qid)
    if request.method == "POST" and request.user.is_authenticated():
        form = forms.RatingForm(request.user, qid, request.post)
        if form.is_valid():
            rating = form.save()
            url = rating.get_url()
            return HttpResponseRedirect(url)
        else:
            print("form.is_valid = FALSE")
    else:
        form = forms.AnswerForm(request.user, qid)

    return render(request, ".html", {
        'xz': "xz"
    })

def popular_questions(request):
    questions = models.Question.objects.popular()
    return questions_list_on_page(request, questions, "questions_popular.html")


def new_questions(request):
    questions = models.Question.objects.new()
    return questions_list_on_page(request, questions, "questions_new.html")


def comments_list(request):
    qid = request.Get.get('qid')
    question = get_object_or_404(models.Question, qid)
    comments = paginate(request, question.question)
    return render(request, "comments.html", {
        'comments': comments
    })


def allow_cors(origin_view):
    def new_view(request, *args, **kwargs):
        response = origin_view(request, *args, **kwargs)
        origin = request.META.get('HTTP_ORIGIN')
        if not origin:
            return response
        for domain in settings.CORS_WHITE_LIST:
            if origin.endswith('.' + domain):
                response['Access-Control-Allow-Origin'] = origin
        return response
    return new_view