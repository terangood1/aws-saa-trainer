from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse

from .admin import QuestionAdmin
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

    def test_position_outside_one_to_five_fails_full_clean(self):
        for position in (0, 6):
            with self.subTest(position=position):
                choice = Choice(question=self.question, text='예시 선택지', position=position)

                with self.assertRaises(ValidationError) as error:
                    choice.full_clean()

                self.assertIn('position', error.exception.message_dict)

    def test_positions_one_to_five_pass_full_clean(self):
        for position in range(1, 6):
            with self.subTest(position=position):
                choice = Choice(question=self.question, text='예시 선택지', position=position)
                choice.full_clean()


class QuestionAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = get_user_model().objects.create_superuser(username='admin')
        cls.user = get_user_model().objects.create_user(username='user')
        cls.staff = get_user_model().objects.create_user(username='staff', is_staff=True)

    def setUp(self):
        self.client.force_login(self.superuser)
        self.add_url = reverse('admin:questions_question_add')
        self.list_url = reverse('admin:questions_question_changelist')

    def payload(self, count=4, correct=(1,), question_type='SINGLE', positions=None):
        data = {
            'text': 'AWS 서비스 문제', 'explanation': '서비스 해설',
            'question_type': question_type,
            'choices-TOTAL_FORMS': str(count), 'choices-INITIAL_FORMS': '0',
            'choices-MIN_NUM_FORMS': '0', 'choices-MAX_NUM_FORMS': '10',
            '_save': 'Save',
        }
        for index in range(count):
            data[f'choices-{index}-text'] = f'선택지 {index + 1}'
            if positions is not None:
                data[f'choices-{index}-position'] = positions[index]
            if index + 1 in correct:
                data[f'choices-{index}-is_correct'] = 'on'
        return data

    def assert_rejected(self, data, message):
        response = self.client.post(self.add_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, message)
        self.assertFalse(Question.objects.exists())
        self.assertFalse(Choice.objects.exists())

    def test_question_is_registered(self):
        self.assertIsInstance(admin.site._registry[Question], QuestionAdmin)

    def test_admin_access_permissions(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertRedirects(response, f"{reverse('admin:login')}?next={self.list_url}")
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(self.list_url).status_code, 302)
        self.client.force_login(self.staff)
        self.assertEqual(self.client.get(self.list_url).status_code, 403)
        self.client.force_login(self.superuser)
        self.assertEqual(self.client.get(self.list_url).status_code, 200)

    def test_search_by_question_text(self):
        match = Question.objects.create(text='Amazon S3 storage', explanation='S3')
        Question.objects.create(text='Amazon EC2 compute', explanation='EC2')
        response = self.client.get(self.list_url, {'q': 'S3'})
        self.assertEqual(list(response.context['cl'].queryset), [match])

    def test_filter_and_latest_first_ordering(self):
        older = Question.objects.create(text='older', explanation='test')
        newer = Question.objects.create(text='newer', explanation='test', question_type='MULTIPLE')
        response = self.client.get(self.list_url)
        self.assertEqual(list(response.context['cl'].queryset), [newer, older])
        response = self.client.get(self.list_url, {'question_type__exact': 'MULTIPLE'})
        self.assertEqual(list(response.context['cl'].queryset), [newer])

    def test_add_page_has_four_blank_choices(self):
        response = self.client.get(self.add_url)
        self.assertEqual(len(response.context['inline_admin_formsets'][0].formset.forms), 4)

    def test_question_type_is_editable_only_on_add_page(self):
        response = self.client.get(self.add_url)
        self.assertIn('question_type', response.context['adminform'].form.fields)
        self.assertContains(response, '<select name="question_type"')
        for question_type in ('SINGLE', 'MULTIPLE'):
            with self.subTest(question_type=question_type):
                Question.objects.all().delete()
                question, _ = self.saved_question_payload(question_type)
                response = self.client.get(reverse('admin:questions_question_change', args=[question.pk]))
                self.assertNotIn('question_type', response.context['adminform'].form.fields)
                self.assertIn('question_type', response.context['adminform'].readonly_fields)
                self.assertNotContains(response, 'name="question_type"')
                self.assertContains(response, question.get_question_type_display())

    def test_edit_other_fields_without_posting_question_type(self):
        question, data = self.saved_question_payload()
        del data['question_type']
        data.update({'text': '수정 본문', 'explanation': '수정 해설',
                     'choices-0-text': '수정 선택지', 'choices-1-is_correct': 'on'})
        del data['choices-0-is_correct']
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertRedirects(response, self.list_url)
        question.refresh_from_db()
        self.assertEqual(question.question_type, 'SINGLE')
        self.assertEqual(question.text, '수정 본문')
        self.assertEqual(question.explanation, '수정 해설')
        self.assertEqual(question.choices.get(position=1).text, '수정 선택지')
        self.assertEqual(question.choices.get(is_correct=True).position, 2)

    def test_invalid_posted_type_is_ignored(self):
        question, data = self.saved_question_payload('MULTIPLE')
        data['question_type'] = 'INVALID'
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertRedirects(response, self.list_url)
        question.refresh_from_db()
        self.assertEqual(question.question_type, 'MULTIPLE')

    def test_change_page_has_no_extra_blank_choices(self):
        for question_type, count in (('SINGLE', 4), ('MULTIPLE', 5)):
            with self.subTest(question_type=question_type):
                # 각 유형의 실제 수정 화면을 독립적으로 확인한다.
                Question.objects.all().delete()
                question, _ = self.saved_question_payload(question_type)
                response = self.client.get(reverse('admin:questions_question_change', args=[question.pk]))
                inline = response.context['inline_admin_formsets'][0]
                self.assertEqual(len(inline.formset.forms), count)
                self.assertEqual(len(inline.formset.extra_forms), 0)
                self.assertEqual(
                    [form.instance.pk for form in inline.formset.forms],
                    list(question.choices.order_by('position').values_list('pk', flat=True)),
                )

    def test_change_page_keeps_default_add_support(self):
        question, _ = self.saved_question_payload()
        response = self.client.get(reverse('admin:questions_question_change', args=[question.pk]))
        inline = response.context['inline_admin_formsets'][0]
        self.assertTrue(inline.has_add_permission)
        self.assertGreater(inline.formset.max_num, inline.formset.total_form_count())
        self.assertContains(response, 'id="choices-empty"')
        self.assertContains(response, 'name="choices-__prefix__-text"')
        self.assertContains(response, 'admin/js/inlines.js')

    def test_save_valid_single_question(self):
        response = self.client.post(self.add_url, self.payload())
        self.assertRedirects(response, self.list_url)
        question = Question.objects.get()
        self.assertEqual(question.choices.count(), 4)
        self.assertEqual(question.choices.filter(is_correct=True).count(), 1)
        self.assertEqual(question.explanation, '서비스 해설')
        self.assertEqual(list(question.choices.order_by('position').values_list('position', flat=True)), [1, 2, 3, 4])

    def test_reject_fewer_or_more_than_four_choices(self):
        for count in (0, 3, 5):
            with self.subTest(count=count):
                self.assert_rejected(
                    self.payload(count=count, positions=[1, 2, 3, 4, 1][:count]),
                    'SINGLE 유형의 선택지는 정확히 4개여야 합니다.',
                )

    def test_single_requires_exactly_one_correct_answer(self):
        for correct in ((), (1, 2), (1, 2, 3, 4)):
            with self.subTest(correct=correct):
                self.assert_rejected(self.payload(correct=correct), 'SINGLE 유형은 정답이 정확히 1개여야 합니다.')

    def test_multiple_requires_at_least_two_correct_answers(self):
        for correct in ((), (1,)):
            with self.subTest(correct=correct):
                self.assert_rejected(
                    self.payload(count=5, correct=correct, question_type='MULTIPLE'),
                    'MULTIPLE 유형은 정답이 2개 이상이어야 합니다.',
                )

    def test_save_valid_multiple_question(self):
        for count in (2, 3, 4, 5):
            with self.subTest(count=count):
                response = self.client.post(self.add_url, self.payload(
                    count=5, correct=tuple(range(1, count + 1)), question_type='MULTIPLE',
                ))
                self.assertRedirects(response, self.list_url)
                self.assertEqual(Question.objects.latest('pk').choices.filter(is_correct=True).count(), count)
                self.assertEqual(list(Question.objects.latest('pk').choices.order_by('position').values_list('position', flat=True)), [1, 2, 3, 4, 5])

    def test_submitted_duplicate_positions_are_ignored(self):
        response = self.client.post(self.add_url, self.payload(positions=[1, 1, 3, 4]))
        self.assertRedirects(response, self.list_url)
        self.assertEqual(list(Choice.objects.order_by('position').values_list('position', flat=True)), [1, 2, 3, 4])

    def test_submitted_invalid_positions_are_ignored(self):
        response = self.client.post(self.add_url, self.payload(positions=[0, 5, 'invalid', -1]))
        self.assertRedirects(response, self.list_url)
        self.assertEqual(list(Choice.objects.order_by('position').values_list('position', flat=True)), [1, 2, 3, 4])

    def saved_question_payload(self, question_type='SINGLE'):
        count = 5 if question_type == 'MULTIPLE' else 4
        correct = (1, 2) if question_type == 'MULTIPLE' else (1,)
        self.client.post(self.add_url, self.payload(count=count, correct=correct, question_type=question_type))
        question = Question.objects.get()
        data = self.payload(count=count, correct=correct, question_type=question_type)
        data['choices-INITIAL_FORMS'] = str(count)
        for index, choice in enumerate(question.choices.order_by('position')):
            data[f'choices-{index}-id'] = str(choice.pk)
        return question, data

    def test_edit_question_and_inline(self):
        question, data = self.saved_question_payload()
        data['text'] = '수정한 문제'
        data['explanation'] = '수정한 해설'
        data['choices-0-text'] = '수정한 선택지'
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertRedirects(response, self.list_url)
        question.refresh_from_db()
        self.assertEqual(question.text, '수정한 문제')
        self.assertEqual(question.explanation, '수정한 해설')
        self.assertEqual(question.choices.get(position=1).text, '수정한 선택지')

    def test_posted_type_change_is_ignored(self):
        question, data = self.saved_question_payload()
        data['question_type'] = 'MULTIPLE'
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertRedirects(response, self.list_url)
        question.refresh_from_db()
        self.assertEqual(question.question_type, 'SINGLE')

    def test_deleting_choice_is_rejected(self):
        question, data = self.saved_question_payload()
        data['choices-3-DELETE'] = 'on'
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertContains(response, 'SINGLE 유형의 선택지는 정확히 4개여야 합니다.')
        self.assertEqual(question.choices.count(), 4)

    def test_position_is_not_an_editable_form_field(self):
        response = self.client.get(self.add_url)
        formset = response.context['inline_admin_formsets'][0].formset
        self.assertNotIn('position', formset.forms[0].fields)
        self.assertNotContains(response, 'name="choices-0-position"')

    def test_existing_positions_cannot_be_swapped_by_post(self):
        question, data = self.saved_question_payload()
        before = dict(question.choices.values_list('pk', 'position'))
        for index, position in enumerate([2, 1, 4, 3]):
            data[f'choices-{index}-position'] = position
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertRedirects(response, self.list_url)
        self.assertEqual(dict(question.choices.values_list('pk', 'position')), before)

    def replacement_payload(self, indexes):
        question, data = self.saved_question_payload()
        before = dict(question.choices.values_list('pk', 'position'))
        data['choices-TOTAL_FORMS'] = str(4 + len(indexes))
        for offset, index in enumerate(indexes, start=4):
            data[f'choices-{index}-DELETE'] = 'on'
            data[f'choices-{offset}-text'] = f'교체 선택지 {offset}'
            if index == 0:
                data[f'choices-{offset}-is_correct'] = 'on'
        return question, data, before

    def test_deleted_positions_are_reused_by_new_choices(self):
        question, data, before = self.replacement_payload([0, 2])
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertRedirects(response, self.list_url)
        self.assertEqual(list(question.choices.order_by('position').values_list('position', flat=True)), [1, 2, 3, 4])
        self.assertEqual(list(question.choices.filter(text__startswith='교체').order_by('position').values_list('position', flat=True)), [1, 3])
        for pk, position in before.items():
            if position in (2, 4):
                self.assertEqual(question.choices.get(pk=pk).position, position)

    def test_replace_all_four_choices(self):
        question, data, before = self.replacement_payload([0, 1, 2, 3])
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertRedirects(response, self.list_url)
        self.assertFalse(question.choices.filter(pk__in=before).exists())
        self.assertEqual(list(question.choices.order_by('position').values_list('position', flat=True)), [1, 2, 3, 4])

    def test_invalid_replacement_does_not_delete_existing_choices(self):
        question, data, before = self.replacement_payload([0])
        data.pop('choices-4-is_correct')
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertContains(response, 'SINGLE 유형은 정답이 정확히 1개여야 합니다.')
        self.assertEqual(dict(question.choices.values_list('pk', 'position')), before)

    def test_duplicate_existing_choice_ids_are_rejected(self):
        question, data = self.saved_question_payload()
        data['choices-1-id'] = data['choices-0-id']
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertContains(response, '선택지 정보가 변경되었거나 올바르지 않습니다.')
        self.assertEqual(question.choices.count(), 4)

    def test_missing_management_data_returns_form_error(self):
        data = self.payload()
        del data['choices-TOTAL_FORMS']
        response = self.client.post(self.add_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Question.objects.exists())

    def test_multiple_rejects_incorrect_choice_counts(self):
        for count in (0, 4, 6):
            with self.subTest(count=count):
                self.assert_rejected(
                    self.payload(count=count, correct=(1, 2), question_type='MULTIPLE'),
                    'MULTIPLE 유형의 선택지는 정확히 5개여야 합니다.',
                )

    def test_posted_type_cannot_change_required_choice_count(self):
        question, data = self.saved_question_payload()
        before = dict(question.choices.values_list('pk', 'position'))
        data.update({'question_type': 'MULTIPLE', 'choices-TOTAL_FORMS': '5',
                     'choices-4-text': '다섯 번째 선택지', 'choices-4-is_correct': 'on'})
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertContains(response, 'SINGLE 유형의 선택지는 정확히 4개여야 합니다.')
        question.refresh_from_db()
        self.assertEqual(question.question_type, 'SINGLE')
        self.assertEqual(question.choices.count(), 4)
        self.assertEqual(dict(question.choices.filter(pk__in=before).values_list('pk', 'position')), before)

    def test_posted_type_cannot_relax_single_answer_validation(self):
        question, data = self.saved_question_payload()
        data.update({'question_type': 'MULTIPLE', 'choices-1-is_correct': 'on'})
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertContains(response, 'SINGLE 유형은 정답이 정확히 1개여야 합니다.')
        question.refresh_from_db()
        self.assertEqual(question.question_type, 'SINGLE')
        self.assertEqual(question.choices.count(), 4)

    def test_posted_single_type_is_ignored_for_multiple(self):
        question, data = self.saved_question_payload('MULTIPLE')
        url = reverse('admin:questions_question_change', args=[question.pk])
        data['question_type'] = 'SINGLE'
        response = self.client.post(url, data)
        self.assertRedirects(response, self.list_url)
        question.refresh_from_db()
        self.assertEqual(question.question_type, 'MULTIPLE')
        self.assertEqual(question.choices.count(), 5)
        del data['choices-1-is_correct']
        response = self.client.post(url, data)
        self.assertContains(response, 'MULTIPLE 유형은 정답이 2개 이상이어야 합니다.')
        question.refresh_from_db()
        self.assertEqual(question.question_type, 'MULTIPLE')
        self.assertEqual(list(question.choices.order_by('position').values_list('position', flat=True)), [1, 2, 3, 4, 5])

    def test_posted_type_cannot_relax_multiple_choice_count(self):
        question, data = self.saved_question_payload('MULTIPLE')
        before = dict(question.choices.values_list('pk', 'position'))
        data.update({'question_type': 'SINGLE', 'choices-1-DELETE': 'on'})
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertContains(response, 'MULTIPLE 유형의 선택지는 정확히 5개여야 합니다.')
        self.assertEqual(dict(question.choices.values_list('pk', 'position')), before)

    def test_replace_multiple_choices_reuses_deleted_positions(self):
        question, data = self.saved_question_payload('MULTIPLE')
        before = dict(question.choices.values_list('pk', 'position'))
        data.update({'choices-TOTAL_FORMS': '7', 'choices-0-DELETE': 'on',
                     'choices-4-DELETE': 'on', 'choices-5-text': '교체 정답',
                     'choices-5-is_correct': 'on', 'choices-6-text': '교체 오답'})
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertRedirects(response, self.list_url)
        self.assertEqual(question.choices.get(position=1).text, '교체 정답')
        self.assertEqual(question.choices.get(position=5).text, '교체 오답')
        self.assertEqual(question.choices.count(), 5)
        for pk, position in before.items():
            if position in (2, 3, 4):
                self.assertEqual(question.choices.get(pk=pk).position, position)

    def test_replace_all_five_multiple_choices(self):
        question, data = self.saved_question_payload('MULTIPLE')
        data['choices-TOTAL_FORMS'] = '10'
        for index in range(5):
            data[f'choices-{index}-DELETE'] = 'on'
            data[f'choices-{index + 5}-text'] = f'새 선택지 {index}'
            if index < 2:
                data[f'choices-{index + 5}-is_correct'] = 'on'
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertRedirects(response, self.list_url)
        self.assertEqual(list(question.choices.order_by('position').values_list('position', flat=True)), [1, 2, 3, 4, 5])

    def test_legacy_multiple_with_four_choices_is_preserved_until_fixed(self):
        question, data = self.saved_question_payload()
        Question.objects.filter(pk=question.pk).update(question_type='MULTIPLE')
        data['question_type'] = 'MULTIPLE'
        data['choices-1-is_correct'] = 'on'
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertContains(response, 'MULTIPLE 유형의 선택지는 정확히 5개여야 합니다.')
        self.assertEqual(question.choices.count(), 4)
        data.update({'choices-TOTAL_FORMS': '5', 'choices-4-text': '추가 선택지'})
        response = self.client.post(reverse('admin:questions_question_change', args=[question.pk]), data)
        self.assertRedirects(response, self.list_url)
        self.assertEqual(question.choices.count(), 5)
