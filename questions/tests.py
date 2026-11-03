from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Choice, Question


class QuestionModelTests(TestCase):
    def test_create_question_with_default_single_type(self):
        question = Question.objects.create(
            text='객체 저장에 사용하는 AWS 서비스는 무엇인가요?',
            explanation='Amazon S3는 객체 스토리지 서비스입니다.',
        )
        question.refresh_from_db()

        self.assertEqual(question.text, '객체 저장에 사용하는 AWS 서비스는 무엇인가요?')
        self.assertEqual(question.question_type, Question.QuestionType.SINGLE)
        self.assertEqual(str(question), '객체 저장에 사용하는 AWS 서비스는 무엇인가요?')

    def test_create_multiple_answer_question(self):
        question = Question.objects.create(
            text='스토리지 서비스를 모두 선택하세요.',
            explanation='Amazon S3와 Amazon EBS는 스토리지 서비스입니다.',
            question_type=Question.QuestionType.MULTIPLE,
        )
        question.refresh_from_db()

        self.assertEqual(question.question_type, Question.QuestionType.MULTIPLE)


class ChoiceModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question = Question.objects.create(
            text='객체 저장에 사용하는 AWS 서비스는 무엇인가요?',
            explanation='Amazon S3는 객체 스토리지 서비스입니다.',
        )

    def test_question_reverse_relation_returns_four_choices(self):
        choices = [
            Choice.objects.create(
                question=self.question,
                text=text,
                is_correct=(position == 1),
                position=position,
            )
            for position, text in enumerate(
                ['Amazon S3', 'Amazon EC2', 'Amazon RDS', 'Amazon Route 53'],
                start=1,
            )
        ]

        self.assertCountEqual(self.question.choices.all(), choices)
        self.assertEqual(self.question.choices.count(), 4)

    def test_duplicate_position_for_same_question_raises_integrity_error(self):
        Choice.objects.create(question=self.question, text='Amazon S3', position=1)

        # 안쪽 트랜잭션을 롤백하여 TestCase의 트랜잭션을 정상 상태로 유지한다.
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Choice.objects.create(
                    question=self.question, text='Amazon EC2', position=1,
                )

        self.assertEqual(self.question.choices.count(), 1)

    def test_same_position_is_allowed_for_different_questions(self):
        other_question = Question.objects.create(
            text='가상 서버를 제공하는 AWS 서비스는 무엇인가요?',
            explanation='Amazon EC2는 가상 서버를 제공합니다.',
        )
        Choice.objects.create(question=self.question, text='Amazon S3', position=1)
        other_choice = Choice.objects.create(
            question=other_question, text='Amazon EC2', position=1,
        )

        self.assertEqual(other_question.choices.get(), other_choice)

    def test_position_outside_one_to_four_fails_full_clean(self):
        for position in (0, 5):
            with self.subTest(position=position):
                choice = Choice(question=self.question, text='예시 선택지', position=position)

                with self.assertRaises(ValidationError) as error:
                    choice.full_clean()

                self.assertIn('position', error.exception.message_dict)

    def test_positions_one_to_four_pass_full_clean(self):
        for position in range(1, 5):
            with self.subTest(position=position):
                choice = Choice(question=self.question, text='예시 선택지', position=position)
                choice.full_clean()
