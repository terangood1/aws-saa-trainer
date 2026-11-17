from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Question(models.Model):
    class QuestionType(models.TextChoices):
        SINGLE = 'SINGLE', '단일 정답'
        MULTIPLE = 'MULTIPLE', '복수 정답'

    text = models.TextField()
    explanation = models.TextField()
    question_type = models.CharField(
        max_length=8,
        choices=QuestionType.choices,
        default=QuestionType.SINGLE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:80]


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
    )
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    position = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'position'],
                name='unique_choice_position_per_question',
            ),
        ]

    def __str__(self):
        return f'{self.position}. {self.text[:80]}'
