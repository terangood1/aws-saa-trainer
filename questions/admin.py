from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from .models import Choice, Question


class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'question_type', 'explanation')
        labels = {'text': '문제 내용', 'question_type': '문제 유형', 'explanation': '해설'}


class ChoiceAdminForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('text', 'is_correct')
        labels = {'text': '선택지 내용', 'is_correct': '정답 여부'}


class ChoiceInlineFormSet(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return

        # 기존 행 누락이나 중복 ID로 저장 대상이 달라지는 요청을 거부한다.
        existing_ids = set(self.get_queryset().values_list('pk', flat=True))
        submitted_ids = [form.instance.pk for form in self.initial_forms]
        if len(submitted_ids) != len(existing_ids) or set(submitted_ids) != existing_ids:
            raise ValidationError('선택지 정보가 변경되었거나 올바르지 않습니다. 페이지를 새로고침해 주세요.')

        active_forms = [
            form for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
        ]
        question_type = self.instance.question_type
        required_count = 5 if question_type == Question.QuestionType.MULTIPLE else 4
        if len(active_forms) != required_count:
            raise ValidationError(f'{question_type} 유형의 선택지는 정확히 {required_count}개여야 합니다.')

        positions = [form.instance.position for form in active_forms if form.instance.pk]
        allowed_positions = set(range(1, required_count + 1))
        if len(set(positions)) != len(positions) or not set(positions) <= allowed_positions:
            raise ValidationError(
                f'{question_type} 유형의 순서는 1~{required_count}여야 합니다. '
                '범위를 벗어난 기존 선택지를 삭제하고 필요한 선택지를 추가해 주세요.'
            )

        available_positions = iter(sorted(allowed_positions - set(positions)))
        for form in active_forms:
            if not form.instance.pk:
                form.instance.position = next(available_positions)

        super().clean()
        correct_count = sum(form.cleaned_data['is_correct'] for form in active_forms)
        if self.instance.question_type == Question.QuestionType.SINGLE and correct_count != 1:
            raise ValidationError('SINGLE 유형은 정답이 정확히 1개여야 합니다.')
        if self.instance.question_type == Question.QuestionType.MULTIPLE and correct_count < 2:
            raise ValidationError('MULTIPLE 유형은 정답이 2개 이상이어야 합니다.')


class ChoiceInline(admin.TabularInline):
    model = Choice
    form = ChoiceAdminForm
    formset = ChoiceInlineFormSet
    fields = ('fixed_position', 'text', 'is_correct')
    readonly_fields = ('fixed_position',)
    extra = 4
    # 기존 5개를 모두 교체할 수 있도록 추가 행을 허용한다.
    # 저장되는 선택지 수는 Formset에서 문제 유형별로 제한한다.
    max_num = 10
    ordering = ('position',)

    def get_extra(self, request, obj=None, **kwargs):
        return self.extra if obj is None else 0

    @admin.display(description='순서')
    def fixed_position(self, obj):
        return obj.position if obj.pk else '저장 시 자동 할당'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ('text', 'question_type', 'created_at')
    search_fields = ('text',)
    list_filter = ('question_type',)
    ordering = ('-created_at',)
    inlines = (ChoiceInline,)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return (*super().get_readonly_fields(request, obj), 'question_type')
        return super().get_readonly_fields(request, obj)
