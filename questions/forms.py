from django import forms


class AnswerSelectionForm(forms.Form):
    answers = forms.TypedMultipleChoiceField(
        coerce=int,
        error_messages={
            'required': '답안을 선택해 주세요.',
            'invalid_choice': '이 문제에 있는 선택지만 선택해 주세요.',
        },
    )

    def __init__(self, *args, choices, required_count, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answers'].choices = [(choice['id'], choice['text']) for choice in choices]
        self.required_count = required_count

    def clean_answers(self):
        answers = self.cleaned_data['answers']
        if len(answers) != self.required_count or len(set(answers)) != len(answers):
            raise forms.ValidationError(f'서로 다른 답안을 {self.required_count}개 선택해 주세요.')
        return answers
