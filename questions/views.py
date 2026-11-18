from django.shortcuts import render

from .models import Question


def question_list(request):
    questions = Question.objects.only('text', 'question_type', 'created_at').order_by(
        '-created_at', '-pk'
    )
    return render(request, 'questions/question_list.html', {'questions': questions})
