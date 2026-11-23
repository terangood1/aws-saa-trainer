from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .forms import AnswerSelectionForm
from .models import Question


QUESTION_ORDER = ('-created_at', '-pk')


def question_list(request):
    questions = Question.objects.only('text', 'question_type', 'created_at').order_by(
        *QUESTION_ORDER
    )
    return render(request, 'questions/question_list.html', {'questions': questions})


@require_http_methods(['GET', 'HEAD', 'POST'])
def question_detail(request, pk):
    question = get_object_or_404(
        Question.objects.only('text', 'question_type', 'created_at'), pk=pk
    )
    ordered_choices = list(question.choices.order_by('position').values('id', 'text', 'is_correct'))
    choices = [{'id': choice['id'], 'text': choice['text']} for choice in ordered_choices]
    correct_ids = {choice['id'] for choice in ordered_choices if choice['is_correct']}
    multiple = question.question_type == Question.QuestionType.MULTIPLE
    required_count = len(correct_ids) if multiple else 1
    form = AnswerSelectionForm(
        request.POST if request.method == 'POST' else None,
        choices=choices,
        required_count=required_count,
    )
    if form.is_bound and form.is_valid():
        selected_ids = set(form.cleaned_data['answers'])
        for choice in ordered_choices:
            choice['selected'] = choice['id'] in selected_ids

        following = Q(created_at__lt=question.created_at) | Q(
            created_at=question.created_at, pk__lt=question.pk
        )
        next_question_id = (
            Question.objects.filter(following).order_by(*QUESTION_ORDER)
            .values_list('pk', flat=True).first()
        )
        return render(request, 'questions/question_result.html', {
            'question': question,
            'choices': ordered_choices,
            'is_correct': selected_ids == correct_ids,
            'next_question_id': next_question_id,
        })

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
        'question_number': progress['preceding'] + 1,
        'question_total': progress['total'],
    }, status=400 if form.is_bound else 200)
