from django.test import TestCase

from app.forms import NewspaperForm, RedactorCreationForm, RedactorForm, TopicForm


class FormTests(TestCase):
    def test_topic_form_contains_expected_fields(self):
        self.assertEqual(list(TopicForm().fields), ["name"])

    def test_newspaper_form_contains_expected_fields(self):
        self.assertEqual(
            list(NewspaperForm().fields),
            ["title", "content", "published_date", "topic", "publishers"],
        )

    def test_redactor_form_contains_expected_fields(self):
        self.assertEqual(
            list(RedactorForm().fields),
            [
                "username",
                "first_name",
                "last_name",
                "email",
                "years_of_experience",
            ],
        )

    def test_redactor_creation_form_assigns_editor_permissions_on_save(self):
        form = RedactorCreationForm(
            data={
                "username": "new-redactor",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()

        self.assertIsNotNone(user.pk)
        self.assertSetEqual(
            set(user.user_permissions.values_list("codename", flat=True)),
            {
                "add_topic",
                "change_topic",
                "delete_topic",
                "add_newspaper",
                "change_newspaper",
                "delete_newspaper",
                "change_redactor",
                "delete_redactor",
            },
        )

    def test_redactor_creation_form_commit_false_skips_permission_assignment(self):
        form = RedactorCreationForm(
            data={
                "username": "draft-redactor",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save(commit=False)

        self.assertIsNone(user.pk)
        user.save()
        self.assertEqual(user.user_permissions.count(), 0)
