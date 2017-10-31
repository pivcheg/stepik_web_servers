from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_questions_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        for question in questions:
            if not question.has_choice():
                questions = questions.exclude(pk=question.id)
        return questions[:5]


class DetailView(generic.DetailView):
    """Display the details of the question"""

    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        question = Question.objects.filter(choice__question=self.kwargs['pk'], pub_date__lte=timezone.now())
        if question:
              question = Question.objects.filter(pk=self.kwargs['pk'])

        return question


class ResultsView(generic.DetailView):
    """Display the results of the voting"""

    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        question = Question.objects.filter(choice__question=self.kwargs['pk'], pub_date__lte=timezone.now())
        if question:
              question = Question.objects.filter(pk=self.kwargs['pk'])

        return question


def vote(request, question_id):
    """
    View for processing of voting.

    :param request: HttpResponse
    :param question_id: int
    :return: HttpResponse
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
