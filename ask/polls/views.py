from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from .models import Question


def index(request):
    latest_questions_list = Question.objects.order_by('-pub_date')[:5]
    #context = {'latest_questions_list': latest_questions_list}
    return render(request, "polls/index.html", {
        'latest_questions_list': latest_questions_list,
    })

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    Http404("Question doesn't exist")
    return render(request, "polls/details.html", {
        'question': question,
    })

def results(request, question_id):
    response = "Results of question %s"
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("Voting question %s" % question_id)
