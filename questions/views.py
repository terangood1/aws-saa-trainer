from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .forms import AnswerSelectionForm

from .models import Question


def question_list(request):
    questions = Question.objects.only('text', 'question_type', 'created_at').order_by(
        '-created_at', '-pk'
    )
    return render(request, 'questions/question_list.html', {'questions': questions})


@require_http_methods(['GET', 'HEAD', 'POST'])
def question_detail(request, pk):
    question = get_object_or_404(
        Question.objects.only('text', 'question_type', 'created_at'), pk=pk
    )
    choices = list(question.choices.order_by('position').values('id', 'text'))
    multiple = question.question_type == Question.QuestionType.MULTIPLE
    required_count = question.choices.filter(is_correct=True).count() if multiple else 1
    form = AnswerSelectionForm(
        request.POST if request.method == 'POST' else None,
        choices=choices,
        required_count=required_count,
    )
    selection_valid = form.is_bound and form.is_valid()

    # Match the list's newest-first order, including its primary-key tie breaker.
    preceding = Q(created_at__gt=question.created_at) | Q(
        created_at=question.created_at, pk__gt=question.pk
    )
    progress = Question.objects.aggregate(total=Count('pk'), preceding=Count('pk', filter=preceding))
    return render(request, 'questions/question_detail.html', {
        'question_text': question.text,
        'choices': choices,
        'multiple': multiple,
        'required_count': required_count,
        'form': form,
        'selection_valid': selection_valid,
        'question_number': progress['preceding'] + 1,
        'question_total': progress['total'],
    }, status=400 if form.is_bound and not selection_valid else 200)
