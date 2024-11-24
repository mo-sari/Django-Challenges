from django.shortcuts import render, get_object_or_404
# from django.http import Http404
from .models import (
    Question,
)


def index(request):
    recent_questions = Question.objects.filter(title__startswith='wh').\
                                        order_by('id')

    return render(request, 'questions/index.html',
                  context={'recentQuestions': recent_questions})


def detail(request, question_id):
    # first way:
    # try:
    #     question = Question.objects.get(id=question_id)
    #     context = {'question': question}
    #     return render(request, 'questions/detail.html', context)

    # except Question.DoesNotExist:
    #     raise Http404('the reqested question does not exist')

    # second way:
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'questions/detail.html',
                  context={'question': question})
